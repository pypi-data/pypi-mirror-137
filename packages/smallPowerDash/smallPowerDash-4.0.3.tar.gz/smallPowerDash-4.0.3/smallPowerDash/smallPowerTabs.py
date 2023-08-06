import datetime as dt, pickle, time, os,re,pandas as pd
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px, plotly.graph_objects as go
from dorianUtils.utilsD import Utils
from dorianUtils.dccExtendedD import DccExtended
import dorianUtils.dashTabsD as tabsD

class SmallPowerTab():
    def __init__(self):
        self.listIndicators = [
            # 'repartitions puissances(groups)','repartitions puissances(tags)',
            'fuites air','fuites fuel',
            'rendement GV','rendement blowers',
            'bilan valo','bilan condenseur','pertes stack','cosphi',
            'repartitions puissances(tags)','repartitions puissances(groups)']

    def selectIndicator(self,indicator,*args):
        print(indicator)
        if indicator == 'rendement GV':
            df_tuple = self.cfg.rendement_GV(*args)
        elif indicator == 'rendement blowers':
            df_tuple = self.cfg.rendement_blower(*args)
        elif indicator == 'bilan valo':
            df_tuple = self.cfg.bilan_valo(*args)
        elif indicator == 'pertes stack':
            df_tuple = self.cfg.pertes_thermiques_stack(*args)
        elif indicator == 'cosphi':
            df_tuple = self.cfg.cosphi(*args)
        elif indicator == 'repartitions puissances(groups)':
            df_tuple = self.cfg.repartitionPower(*args,expand='groups',groupnorm=None)
        elif indicator == 'repartitions puissances(tags)':
            df_tuple = self.cfg.repartitionPower(*args,expand='tags',groupnorm='percent')
        elif indicator == 'fuites air':
            df_tuple = self.cfg.fuitesAir(*args)
        elif indicator == 'fuites fuel':
            df_tuple = self.cfg.fuitesFuel(*args)
        else:
            print()
            print('indicator selector should be one of :' + '; '.join(self.listIndicators))
            print('============================================')
        return df_tuple

    def addWidgets(self,dicWidgets):
        widgetLayout,dicLayouts = [],{}
        for wid_key,wid_val in dicWidgets.items():
            if 'dd_indicator'==wid_key:
                widgetObj = self.dccE.dropDownFromList(
                    self.baseId + wid_key, self.listIndicators, 'indicator : ',value=wid_val)
            else:
                print('component :' + wid_key +' not found')
                sys.exit()

            for widObj in widgetObj:widgetLayout.append(widObj)
        return widgetLayout

class ModuleTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='tmo0_',widthGraph=86):
        super().__init__(app,baseId)
        self.cfg = cfs.AnalysisPerModule(folderPkl)
        self.widthGraph = widthGraph
        self.tabLayout = self._buildModuleLayout()
        self.tabname = 'modules'
        self._define_callbacks()

    def _buildModuleLayout(self):
        dicWidgets = {
                    'pdr_time' : {'tmin':self.cfg.listFilesPkl[0],'tmax':self.cfg.listFilesPkl[-1]},
                    'in_timeRes':'auto','dd_resampleMethod':'mean',
                    'dd_style':'lines','dd_cmap':'prism',
                    'btn_export':0,
                    'block_multiAxisSettings':None
                    }
        basicWidgets = self.dccE.basicComponents(dicWidgets,self.baseId)

        dd_modules = self.dccE.dropDownFromList(self.baseId+'dd_modules',
                        list(self.cfg.modules.keys()),'Select your module: ',value = 'GV')

        dd_moduleGroup = self.dccE.dropDownFromList(self.baseId+'dd_moduleGroup',[],
                            'Select the graphs to display: ',value = 0,multi=True)

        cl_units = [dcc.Checklist(id=self.baseId+'check_unit',
                        options=[{'label': 'unit', 'value':'unit'}],value= 'unit')]

        widgetLayout = basicWidgets + dd_modules+dd_moduleGroup+cl_units
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=self.widthGraph)

    def _define_callbacks(self):
        @self.app.callback(
        Output(self.baseId + 'dd_moduleGroup', 'options'),
        Input(self.baseId + 'dd_modules','value'),
        Input(self.baseId + 'check_unit','value'),
        )
        def updateGraph(module,unitGroup):
            if not unitGroup : l = self.cfg.listTagsAllModules(module)[1]
            else : l= list(self.cfg._categorizeTagsPerUnit(module).keys())
            options = [{'label':t,'value':t} for t in l]
            return options

        listInputsGraph = {
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_cmap':'value',
            'dd_style':'value',
            'in_heightGraph':'value',
            'in_axisSp':'value',
            'in_hspace':'value',
            'in_vspace':'value',
            }
        listStatesGraph = {
            'graph':'figure',
            'dd_modules':'value',
            'check_unit':'value',
            'dd_moduleGroup':'value',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
        }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        Output(self.baseId + 'pdr_timeBtn', 'n_clicks'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date'))
        def updateGraph(timeBtn,rsmethod,colmap,style,hg,axsp,hs,vs,fig,module,unitGroup,listGroups,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # triggerList = ['dd_modules','dd_moduleGroup','pdr_timeBtn','dd_resampleMethod']
            triggerList = ['pdr_timeBtn','dd_resampleMethod']
            if not timeBtn or trigId in [self.baseId+k for k in triggerList] :
                timeRange = [date0+' '+t0,date1+' '+t1]
                if not unitGroup :
                    fig = self.cfg.figureModule(module,timeRange,groupsOfModule=listGroups,rs=rs,rsMethod=rsmethod)
                else :
                    fig = self.cfg.figureModuleUnits(module,timeRange,listUnits=listGroups,rs=rs,rsMethod=rsmethod)
            else :fig = go.Figure(fig)
            if not unitGroup :fig = self.cfg.updateFigureModule(fig,module,listGroups,hg,hs,vs,axsp)
            else : fig = fig.update_layout(height=hg)
            # fig = self.updateLegend(fig,lgd)
            return fig,timeBtn

        @self.app.callback(
        Output(self.baseId + 'btn_export','children'),
        Input(self.baseId + 'btn_export', 'n_clicks'),
        State(self.baseId + 'graph','figure'))
        def exportClick(btn,fig):
            fig = go.Figure(fig)
            if btn>0:self.utils.exportDataOnClick(fig,baseName='proof')
            return 'export Data'

class IndicatorTab(SmallPowerTab,tabsD.TabMaster):
    def __init__(self,app,cfg,realtime,baseId='it_'):
        SmallPowerTab.__init__(self)
        tabsD.TabMaster.__init__(self,app,cfg,
            self.selectIndicator,
            cfg.plotIndicator,
            tabname='indicators',baseId=baseId,
            update_fig=self.update_IndicatorFig,
        )
        dicSpecialWidgets = {'dd_indicator':'fuites air'}
        self._buildLayout(dicSpecialWidgets,realTime=realtime)
        if realtime:
            self._define_basicCallbacks(['export','ts_freeze','refreshWindow'])
        else:
            self._define_basicCallbacks(['export','datePickerRange'])

        dicInputs = [
            ('dd_indicator','value')
            ]
        def prepareIndicator(indicator):return indicator

        self._defineCallbackGraph(realtime,dicInputs,prepareIndicator,['dd_indicator'],[],['dd_style'])

    def update_IndicatorFig(self,fig,style):
        print('ok')
        # self.cfg.updateLayoutStandard(fig)

# ==============================================================================
#                        FROM DORIANUTILS.DASHTABSD
# ==============================================================================

class TabSelectedTags_SP(tabsD.TabSelectedTags):
    def __init__(self,app,cfg,realtime):
        tabsD.TabSelectedTags.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.plotTabSelectedData,
            realtime=realtime,
            baseId = 'stt_sp_',
            defaultCat='températures du GV1a'
        )

class TabMultiUnit_SP(tabsD.TabMultiUnits):
    def __init__(self,app,cfg,realtime):
        tabsD.TabMultiUnits.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.multiUnitGraphSP,
            realtime=realtime,
            baseId = 'mut_sp_',
            defaultTags = cfg.getTagsTU('GFC')
            )

class TabMultiUnitSelectedTags_SP(tabsD.TabMultiUnitSelectedTags):
    def __init__(self,app,cfg,realtime):
        tabsD.TabMultiUnitSelectedTags.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.multiUnitGraphSP,
            realtime=realtime,
            defaultCat = 'températures du GV1a',
            baseId = 'must_sp_',
        )

class TabDoubleMultiUnits_SP(tabsD.TabDoubleMultiUnits):
    def __init__(self,app,cfg,realtime):
        tabsD.TabDoubleMultiUnits.__init__(self,app,cfg,
            cfg.loadtags_period,
            realtime = realtime,
            defaultTags1 = cfg.getTagsTU('GFC_01'),
            baseId = 'rtdmu_sp_',
        )

class TabUnitSelector_SP(tabsD.TabUnitSelector):
    def __init__(self,app,cfg,realtime):
        tabsD.TabUnitSelector.__init__(self,app,cfg,
            cfg.loadtags_period,
            cfg.plotTabSelectedData,
            realtime=realtime,
            baseId = 'ust_sp_',
        )
