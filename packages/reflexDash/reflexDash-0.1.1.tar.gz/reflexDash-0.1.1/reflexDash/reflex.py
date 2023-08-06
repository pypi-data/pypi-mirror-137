#!/bin/python
# #######################
# #   GLOBAL VARIABLES  #
# # COMPUTER DEPENDENT  #
# #######################
import os,sys, time, datetime as dt,importlib,pickle,glob,re
import pandas as pd,numpy as np
from dorianUtils.utilsD import Utils
import dorianUtils.comUtils as comUtils
importlib.reload(comUtils)

import socket
namePC = socket.gethostname()
DATABASE_SIZE_SECONDS = 60*10
PARKING_TIME = 60*5
DB_PARAMETERS = {
    'host'     : "192.168.1.44",
    'port'     : "5434",
    'dbname'   : "Fantasio",
    'user'     : "postgres",
    'password' : "SylfenBDD"
}
if 'sylfen' in os.getenv('HOME'):
    baseFolder   = '/home/sylfen/data_ext/'
else:
    baseFolder    = '/home/dorian/data/sylfenData/'
    # DB_PARAMETERS['dbname']="juleslocal"

FOLDERPKL = baseFolder + 'reflex_daily/'
FileSystem = comUtils.FileSystem
fs = FileSystem()
appdir = os.path.dirname(os.path.realpath(__file__))
parentdir = fs.getParentDir(appdir)
CONFFOLDER = parentdir + 'reflexDash/confFiles/'
FILECONF_REFLEX=CONFFOLDER + 'reflex_configfiles.ods'
######################################
##### INITIALIZATION OF DEVICES ######
######################################
plcfile = CONFFOLDER + 'plc_reflex_v1.ods'
dfplc = pd.read_excel(plcfile,sheet_name='plc',index_col=0)
DEVICES={'reflexBattery':comUtils.Device('reflex_battery','noIP',50000,dfplc)}
# ==============================================================================
#                           CONFIGURATIONS
VisualisationMaster_daily = comUtils.VisualisationMaster_daily
SuperDumper_daily = comUtils.SuperDumper_daily
Configurator = comUtils.Configurator

class Config_extender():
    def __init__(self):
        cfg = Configurator(FOLDERPKL,DB_PARAMETERS,devices=DEVICES,
            dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=PARKING_TIME,
            )
        self.utils   = Utils()
        self.file_conf  = FILECONF_REFLEX
        self.usefulTags = pd.read_excel(self.file_conf,sheet_name='useful_tags',index_col=0)
        self.confFolder = CONFFOLDER

class Reflex_dumper(SuperDumper_daily,Config_extender):
    def __init__(self):
        SuperDumper_daily.__init__(self,FOLDERPKL,DB_PARAMETERS,DEVICES,
                        DATABASE_SIZE_SECONDS,PARKING_TIME)
        Config_extender.__init__(self)

    def insert_calctags_intodb(self):
            data={}
            try :
                connReq = ''.join([k + "=" + v + " " for k,v in self.dbParameters.items()])
                dbconn = psycopg2.connect(connReq)
            except :
                print('problem connecting to database ',self.dbParameters)
                return
            cur  = dbconn.cursor()
            start=time.time()
            try :
                data = self.devices['beckhoff'].compute_calculated_tags()
            except:
                print('souci computing new tags at ' + pd.Timestamp.now().isoformat())
                return
            for tag in data.keys():
                sqlreq = "insert into realtimedata (tag,value,timestampz) values ('"
                value = data[tag][0]
                if value==None:
                    value = 'null'
                value=str(value)
                sqlreq+= tag +"','" + value + "','" + data[tag][1]  + "');"
                sqlreq=sqlreq.replace('nan','null')
                cur.execute(sqlreq)
            dbconn.commit()
            cur.close()
            dbconn.close()

    def start_dumping(self):
        self.calcTags_dumper.start()
        SuperDumper_daily.start_dumping(self)

    def stop_dumping(self):
        self.calcTags_dumper.stop()
        SuperDumper_daily.stop_dumping(self)

from PIL import Image
class ReflexComputer(VisualisationMaster_daily,Config_extender):
    def __init__(self,rebuildConf=True):
        VisualisationMaster_daily.__init__(self,FOLDERPKL,DB_PARAMETERS,devices=DEVICES,
                        dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=PARKING_TIME)
        Config_extender.__init__(self)
        self.sylfenlogo  = Image.open(CONFFOLDER +  '/pictures/logo_sylfen.png')
        self.file_conf_pkls = CONFFOLDER +  'reflex_conffiles.pkl'
        self.colorPalettes   = self._loadcolorPalettes()
        conf_pkls = self.fs.load_confFile(self.file_conf_pkls,self.load_confFiles,rebuildConf)
        self.dftagColorCode,self.unitDefaultColors = conf_pkls
        self.colorshades    = list(self.colorPalettes.keys())

    def load_confFiles(self):
        # cst,dfConstants = _load_material_constants()
        dftagColorCode,unitDefaultColors    = self._buildColorCode()
        return dftagColorCode,unitDefaultColors
    ###########################
    #  GENERATOR CONF FILES   #
    ###########################
    def _loadcolorPalettes(self):
        colPal = pickle.load(open(CONFFOLDER+'palettes.pkl','rb'))
        colPal['reds']     = colPal['reds'].drop(['Misty rose',])
        colPal['greens']   = colPal['greens'].drop(['Honeydew',])
        colPal['blues']    = colPal['blues'].drop(['Blue (Munsell)','Powder Blue','Duck Blue','Teal blue'])
        colPal['magentas'] = colPal['magentas'].drop(['Pale Purple','English Violet'])
        colPal['cyans']    = colPal['cyans'].drop(['Azure (web)',])
        colPal['yellows']  = colPal['yellows'].drop(['Light Yellow',])
        #### shuffle them so that colors attribution is random
        for c in colPal.keys():
            colPal[c]=colPal[c].sample(frac=1)
        return colPal

    def _buildColorCode(self):
        unitDefaultColors = pd.read_excel(self.file_conf,sheet_name='units_colorCode',index_col=0)
        dftagColorCode = pd.read_excel(self.file_conf,sheet_name='tags_color_code',index_col=0,keep_default_na=False)
        from plotly.validators.scatter.marker import SymbolValidator
        raw_symbols = pd.Series(SymbolValidator().values[2::3])
        listLines = pd.Series(["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"])
        allHEXColors=pd.concat([k['hex'] for k in self.colorPalettes.values()])
        ### remove dupplicates index (same colors having different names)
        allHEXColors=allHEXColors[~allHEXColors.index.duplicated()]

        def assignRandomColor2Tag(tag):
            unitTag  = self.getUnitofTag(tag).strip()
            shadeTag = unitDefaultColors.loc[unitTag].squeeze()
            color = self.colorPalettes[shadeTag]['hex'].sample(n=1)
            return color.index[0]

        # generate random color/symbol/line for tags who are not in color_codeTags
        listTags_wo_color = [k for k in self.alltags if k not in list(dftagColorCode.index)]
        d = {tag:assignRandomColor2Tag(tag) for tag in listTags_wo_color}
        dfRandomColorsTag = pd.DataFrame.from_dict(d,orient='index',columns=['colorName'])
        dfRandomColorsTag['symbol'] = pd.DataFrame(raw_symbols.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
        dfRandomColorsTag['line'] = pd.DataFrame(listLines.sample(n=len(dfRandomColorsTag),replace=True)).set_index(dfRandomColorsTag.index)
        # concatenate permanent color_coded tags with color-random-assinged tags
        dftagColorCode = pd.concat([dfRandomColorsTag,dftagColorCode],axis=0)
        # assign HEX color to colorname
        dftagColorCode['colorHEX'] = dftagColorCode.apply(lambda x: allHEXColors.loc[x['colorName']],axis=1)
        return dftagColorCode,unitDefaultColors

    # ==============================================================================
    #                   COMPUTATION FUNCTIONS/INDICATORS
    # ==============================================================================
    # ==============================================================================
    #                   graphic functions
    # ==============================================================================
    def update_lineshape_fig(self,fig,style='default'):
        if style=='default':
            fig.update_traces(line_shape="linear",mode='lines+markers')
            names = [k.name for k in fig.data]
            vanneTags   = [k for k in names if 'ECV' in k]
            commandTags = [k for k in names if '.HR36' in k]
            boolTags = [k for k in names if self.getUnitofTag(k) in ['ETAT','CMD','Courbe']]
            hvTags=vanneTags+commandTags+boolTags
            fig.for_each_trace(
                lambda trace: trace.update(line_shape="hv",mode='lines+markers') if trace.name in hvTags else (),
            )
        elif style in ['markers','lines','lines+markers']:
            fig.update_traces(line_shape="linear",mode=style)
        elif style =='stairs':
            fig.update_traces(line_shape="hv",mode='lines')

    def updatecolortraces(self,fig):
        for tag in fig.data:
            tagcolor = self.dftagColorCode.loc[tag.name,'colorHEX']
            # print(tag.name,colName,tagcolor)
            tag.marker.color = tagcolor
            tag.line.color = tagcolor
            tag.marker.symbol = self.dftagColorCode.loc[tag.name,'symbol']
            tag.line.dash = self.dftagColorCode.loc[tag.name,'line']

    def updatecolorAxes(self,fig):
        for ax in fig.select_yaxes():
            titleAxis = ax.title.text
            if not titleAxis==None:
                unit    = titleAxis.strip()
                axColor = self.unitDefaultColors.loc[unit].squeeze()[:-1]
                # print(axColor)
                # sys.exit()
                ax.title.font.color = axColor
                ax.tickfont.color   = axColor
                ax.gridcolor        = axColor

    def multiUnitGraphSP(self,df,tagMapping=None,**kwargs):
        if not tagMapping:tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        # print(tagMapping)
        fig = self.utils.multiUnitGraph(df,tagMapping,**kwargs)
        self.standardLayout(fig)
        self.updatecolorAxes(fig)
        self.updatecolortraces(fig)
        return fig

    def doubleMultiUnitGraph(self,df,tags1,tags2,*args,**kwargs):
        fig = VisualisationMaster_daily.multiMultiUnitGraph(self,df,tags1,tags2,*args,**kwargs)
        self.updatecolorAxes(fig)
        self.updatecolortraces(fig)
        self.standardLayout(fig,h=None)
        return fig
