from dorianUtils.utilsD import Utils
import dorianUtils.dashTabsD as tabsD
# ==============================================================================
#                        FROM DORIANUTILS.DASHTABSD
# ==============================================================================

class TabSelectedTags(tabsD.TabSelectedTags):
    def __init__(self,app,cfg,realtime):
        tabsD.TabSelectedTags.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.plotTabSelectedData,
            realtime=realtime,
            baseId = 'stt_ref_',
            defaultCat='puissances'
        )

class TabMultiUnit(tabsD.TabMultiUnits):
    def __init__(self,app,cfg,realtime):
        tabsD.TabMultiUnits.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.multiUnitGraphSP,
            realtime=realtime,
            baseId = 'mut_ref_',
            defaultTags = cfg.getTagsTU('01')
            )

class TabMultiUnitSelectedTags(tabsD.TabMultiUnitSelectedTags):
    def __init__(self,app,cfg,realtime):
        tabsD.TabMultiUnitSelectedTags.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.multiUnitGraphSP,
            realtime=realtime,
            defaultCat = 'puissances',
            baseId = 'must_ref_',
        )

class TabDoubleMultiUnits(tabsD.TabDoubleMultiUnits):
    def __init__(self,app,cfg,realtime):
        tabsD.TabDoubleMultiUnits.__init__(self,app,cfg,
            cfg.loadtags_period,
            realtime = realtime,
            defaultTags1 = cfg.getTagsTU('JTW'),
            defaultTags2 = cfg.getTagsTU('TT'),
            baseId = 'rtdmu_ref_',
        )

class TabUnitSelector(tabsD.TabUnitSelector):
    def __init__(self,app,cfg,realtime):
        tabsD.TabUnitSelector.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.plotTabSelectedData,
            realtime=realtime,
            baseId = 'ust_ref_',
        )
