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
NAMESPACE_BECKHOFF = "ns=4;s=GVL."

DB_PARAMETERS = {
    'host'     : "localhost",
    'port'     : "5432",
    'dbname'   : "jules",
    'user'     : "postgres",
    'password' : "sylfenbdd"
}
if 'sylfen' in os.getenv('HOME'):
    baseFolder   = '/home/sylfen/data_ext/'
    ENDPOINTURL  = 'opc.tcp://10.10.38.100'
    PORT_BECKHOFF= 4840
else:
    baseFolder    = '/home/dorian/data/sylfenData/'
    # ENDPOINTURL   = 'localhost'
    ENDPOINTURL  = 'opc.tcp://10.10.38.100'
    PORT_BECKHOFF= 4840
    # PORT_BECKHOFF = 65000
    DB_PARAMETERS['dbname']="juleslocal"

FOLDERPKL = baseFolder + 'smallPower_daily/'
FileSystem = comUtils.FileSystem
fs = FileSystem()
appdir = os.path.dirname(os.path.realpath(__file__))
parentdir = fs.getParentDir(appdir)
CONFFOLDER = parentdir + 'smallPowerDash/confFiles/'
FILECONF_SMALLPOWER=CONFFOLDER + 'smallpower_configfiles.ods'

def _load_material_constants():
    dfConstants = pd.read_excel(FILECONF_SMALLPOWER,sheet_name='constants',index_col=1)
    cst = comUtils.EmptyClass()
    for k in dfConstants.index:
        setattr(cst,k,dfConstants.loc[k].value)
    return cst,dfConstants
######################################
##### INITIALIZATION OF DEVICES ######
######################################

# listFiles = glob.glob(CONFFOLDER + '*devices*.ods')
# file_devices = listFiles[0]
# v_devices  = re.findall('_v\d+',file_devices)[0]
# df_devices = pd.read_excel(file_devices,index_col=0,sheet_name='devices')

FILE_PLC_XLSM = glob.glob(CONFFOLDER+'*ALPHA*.xlsm')[0]
PLC_BECKHOFF  = CONFFOLDER + 'plc_smallpower.pkl'
load_plc_beckhoff = lambda :pd.read_excel(FILE_PLC_XLSM,sheet_name='FichierConf_Jules',index_col=0)

class Beckhoff_client(comUtils.Opcua_Client):
    def __init__(self):
        comUtils.Opcua_Client.__init__(self,
                    device_name = 'beckhoff',
                    endpointUrl = ENDPOINTURL,
                    port        = PORT_BECKHOFF,
                    dfplc       = fs.load_confFile(PLC_BECKHOFF,load_plc_beckhoff,False),
                    nameSpace   = NAMESPACE_BECKHOFF)
        if '10.10.38.100' in self.endpointUrl:
            certif_path = CONFFOLDER + 'my_cert.pem'
            key_path    = CONFFOLDER + 'my_private_key.pem'
            sslString = 'Basic256Sha256,Sign,' + certif_path + ',' + key_path
            self.client.set_security_string(sslString)
            self.client.set_user("Alpha")
            self.client.set_password("Alpha$01")
            print('security check succeeded!')

        self.calculatedTags={
            'SEH1.Itotal.HCX00':self._get_tags_Istacks(),
            'SEH1.coefFuitesAir.HCX00':self._get_tags_fuiteair(),
            'SEH1.modeFuel.HCX00':self.get_tags_modeFuel(),
            'SEH1.FuitesFuel.HCX00':self._get_tags_fuitefuel(),
            'SEH1.L032-L303-L025.HCX00':self.get_tags_verifdebitmetres(),
        }
        self.listCalculatedTags = list(self.calculatedTags.keys())
        self.cst,_ = _load_material_constants()

    def _get_tags_Istacks(self):
        return {
            'Istacks' : self.getTagsTU('STK.*IT.*HM05'),
            }
    def _get_tags_fuiteair(self):
        return {
            'airAval' : self.getTagsTU('l118.*FT'),
            'airAmont' : self.getTagsTU('l138.*FT'),
            # 'Tfour' : self.getTagsTU('STB_TT_02'),
            # 'pressionCollecteur' : self.getTagsTU('GFC_02.*PT'),
            'pressionDiffuseur' : self.getTagsTU('GFD_02.*PT')
        }
    def _get_tags_fuitefuel(self):
        return {
        'L025'    : self.getTagsTU('l025.*FT.*HM05'),
        'L032'    : self.getTagsTU('l032.*FT.*HM05'),
        'L041'    : self.getTagsTU('l041.*FT.*HM05'),
        'L303'    : self.getTagsTU('l303.*FT.*HM05'),
        }
    def get_tags_modeFuel(self):
        return {
                'vanne26' : self.getTagsTU('l026.*ECV'),#NO
                'vanne27' : self.getTagsTU('l027.*ECV'),#NO
                'vanne29' : self.getTagsTU('l029.*ECV'),#NF
                'vanne35' : self.getTagsTU('l035.*ECV'),#NF
                'vanne39' : self.getTagsTU('l039.*ECV'),#NF
                'vanne40' : self.getTagsTU('l040.*ECV'),#NF
        }
    def get_tags_verifdebitmetres(self):
        return {
                'L032' : self.getTagsTU('l032.*FT'),#NO
                'L303' : self.getTagsTU('l303.*FT'),#NO
                'L025' : self.getTagsTU('l025.*FT'),#NF
        }

    def compute_calculated_tags(self):
        ### gather first all values
        alltags     = self.fs.flatten([list(d.values()) for d in self.calculatedTags.values()])
        dictvalues  = self.collectData(alltags)
        # return dictvalues
        cal_tags = {}
        def get_dictvalues(x):
            d_tags=self.calculatedTags[x]
            return {var:[dictvalues[t][0] for t in tags] for var,tags in d_tags.items()}

        #### courant total stacks
        now = pd.Timestamp.now(tz='UTC')
        d_itotal = get_dictvalues('SEH1.Itotal.HCX00')
        itotal=self.i_total(**d_itotal)
        cal_tags['SEH1.Itotal.HCX00']=[itotal,now.isoformat()]

        #### coefficient de fuite air
        now = pd.Timestamp.now(tz='UTC')
        d_fuitesair = {t:v[0] for t,v in get_dictvalues('SEH1.coefFuitesAir.HCX00').items()}
        cal_tags['SEH1.coefFuitesAir.HCX00']=[self.coefFuitesAir(itotal,**d_fuitesair),now.isoformat()]

        #### fuel mode
        now=pd.Timestamp.now(tz='UTC')
        d_modefuel = {t:v[0] for t,v in get_dictvalues('SEH1.modeFuel.HCX00').items()}
        modefuel=self.fuelmode(d_modefuel)
        # if not len(modefuel)==1:print('several pile modes simultaneously : ',modefuel)
        modefuel=modefuel[0]
        cal_tags['SEH1.modeFuel.HCX00']=[modefuel,now.isoformat()]

        #### coefficient de fuite fuel
        now=pd.Timestamp.now(tz='UTC')
        d_fuitesfuel = {t:v[0] for t,v in get_dictvalues('SEH1.FuitesFuel.HCX00').items()}
        cal_tags['SEH1.FuitesFuel.HCX00']=[self.coefFuitesFuel(itotal,modefuel,**d_fuitesfuel),
                                            now.isoformat()]
        #### verif debitmetre
        now=pd.Timestamp.now(tz='UTC')
        d_verifdebits = {t:v[0] for t,v in get_dictvalues('SEH1.L032-L303-L025.HCX00').items()}
        cal_tags['SEH1.L032-L303-L025.HCX00']=[self.verifDebitmetre(**d_verifdebits),now.isoformat()]
        return cal_tags

    def i_total(self,Istacks):
        return sum(Istacks)

    def coefFuitesAir(self,Itotal,airAval,airAmont,pressionDiffuseur):
        # production O2
        Po2mols = Itotal*25/(4*self.cst.FAR) ##25 cells
        Po2Nlmin = Po2mols*self.cst.vlm*60
        # fuite air
        # QairAval = df[airAval] + Po2Nlmin
        QairAval = airAval - Po2Nlmin
        fuiteAir = airAmont - QairAval
        coefFuiteAir = fuiteAir/pressionDiffuseur
        return coefFuiteAir

    def fuelmode(self,dvvv):
        # NF: False<==>fermé ; NO: False<==>ouvert
        # NF: False<==>ouvert ; NO True<==>fermé
        modeFuel = []
        # Gonflage :
        # L035 ou L040 fermées et L039 fermée et L027(NO) fermée
        if (not dvvv['vanne35'] or not dvvv['vanne40']) and (not dvvv['vanne39']) and (dvvv['vanne27']):
            modeFuel.append('gonflage')

        # Boucle fermée recirculation à froid (mode pile):
        # L026(NO) et L029 fermées, L027(NO) ouverte, L035 OU L040 fermées
        if (dvvv['vanne26']) and (not dvvv['vanne29']) and (not dvvv['vanne27']) and (not dvvv['vanne35']) or (not dvvv['vanne40']):
            modeFuel.append('recircuFroidPile')

        # Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        # (L035 ET L040 ouvertes) ou L026(NO) ouverte ou L029 ouverte
        if (dvvv['vanne35'] and dvvv['vanne40']) or (not dvvv['vanne26']) or (dvvv['vanne29']):
            modeFuel.append('bo_electrolyse')

        # Fonctionnement mode gaz naturel :
        # - L027(NO) fermée, L039 ouverte
        if (dvvv['vanne27'] and dvvv['vanne39']):
            modeFuel.append('gaz_nat')
        return modeFuel

    def coefFuitesFuel(self,Itotal,modefuel,L303,L041,L032,L025):
        '''
        Gonflage :
        - L035 ou L040 fermées et L039 fermée et L027 fermée
        - fuites fuel BF = L303 + L041 (+ Somme i x 25 / 2F)  note : normalement dans ce mode le courant est nul.
        Boucle fermée recirculation à froid (mode pile)
        - L026 et L029 fermées, L027 ouverte, L035 OU L040 fermées
        - fuites fuel BF = L303 + L041 + Somme i x 25 / 2F
        Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        - (L035 ET L040 ouvertes) ou L026 ouverte ou L029 ouverte
        - fuite ligne fuel BO = L303 + L041 + Somme i x 25 / 2F – L025
        Fonctionnement mode gaz naturel :
        - L027 fermée, L039 ouverte
        - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025
        En résumé : trois calculs possibles du débit de fuite fuel
        Le même calcul pour les cas 1 et 2 qui sont « fermés »
        Un calcul pour le mode ouvert électrolyse ou boucle ouverte pendant les transitions
        Un calcul pour le mode gaz naturel.
        '''
        #############################
        # compute Hydrogen production
        #############################
        PH2mols = Itotal*25/(2*self.cst.FAR) ##25 cells
        PH2Nlmin = PH2mols*self.cst.vlm*60
        #############################
        # mode fuel
        #############################
        if modefuel=='gonflage' or modefuel=='recircuFroidPile':
            fuitesFuel = L303 + L041 + PH2Nlmin
        elif modefuel=='bo_electrolyse':
            fuitesFuel = L303 + L041 + PH2Nlmin - L025
        elif modefuel=='gaz_nat':
            fuitesFuel = (L032 - L303)*4 + L303 + L041 + PH2Nlmin - L025
        return fuitesFuel

    def verifDebitmetre(self,L032,L303,L025):
        # Vérif débitmètres ligne fuel BF = L032 FT – L303 – L025
        return L032-L303-L025

DEVICES={'beckhoff':Beckhoff_client()}
# ==============================================================================
#                           CONFIGURATIONS
VisualisationMaster_daily = comUtils.VisualisationMaster_daily
Configurator = comUtils.Configurator
SuperDumper_daily = comUtils.SuperDumper_daily
VersionManager_daily = comUtils.VersionManager_daily
# sys.exit()

class Config_extender():
    def __init__(self):
        cfg = Configurator(FOLDERPKL,DB_PARAMETERS,devices=DEVICES,
            dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=PARKING_TIME,
            )
        self.utils   = Utils()
        self.devices = cfg.devices
        self.devices['beckhoff'].file_plc_xlsm = FILE_PLC_XLSM
        self.file_plc_xlsm = FILE_PLC_XLSM
        self.file_conf  = FILECONF_SMALLPOWER
        self.usefulTags = pd.read_excel(self.file_conf,sheet_name='useful_tags',index_col=0)
        self.confFolder  = CONFFOLDER
        self.freqCalctags = 1
        self.typesCalculatedTags = {
            'SEH1.Itotal.HCX00':['REAL','courant total stacks','A'],
            # 'SEH1.coefFuitesAir.HCX00':['REAL','coefficient de fuites air','Nl/min/mbarg'],
            'SEH1.coefFuitesAir.HCX00':['REAL','coefficient de fuites air','u.a.'],
            'SEH1.modeFuel.HCX00':['STRING(40)','mode fuel','u.a.'],
            'SEH1.FuitesFuel.HCX00':['REAL','coefficient de fuite fuel','Nl/min'],
            'SEH1.L032-L303-L025.HCX00':['REAL','vérification des débits mètres','Nl/min'],
        }
        plcCalctags = pd.DataFrame.from_dict(self.typesCalculatedTags,orient='index',columns=['DATATYPE','DESCRIPTION','UNITE'])
        plcCalctags['DATASCIENTISM']=True
        plcCalctags['FREQUENCE_ECHANTILLONNAGE']=self.freqCalctags
        plcCalctags['PRECISION'] = 0.01
        # self.plcCalctags=plcCalctags
        self.dfplc  = pd.concat([cfg.dfplc,plcCalctags],axis=0)
        self.alltags  = list(self.dfplc.index)
        self.listUnits = self.dfplc.UNITE.dropna().unique().tolist()


import psycopg2
class SmallPower_dumper(SuperDumper_daily,Config_extender):
    def __init__(self):
        SuperDumper_daily.__init__(self,FOLDERPKL,DB_PARAMETERS,DEVICES,
                        DATABASE_SIZE_SECONDS,PARKING_TIME)
        Config_extender.__init__(self)
        self.devices['beckhoff'].client.connect() #====>cause problem with multiprocessing
        ### interval for calculated tags
        self.calcTags_dumper = comUtils.SetInterval(self.freqCalctags,self.insert_calctags_intodb)

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

import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
class SmallPowerComputer(VisualisationMaster_daily,Config_extender):
    def __init__(self,rebuildConf=True):
        VisualisationMaster_daily.__init__(self,FOLDERPKL,DB_PARAMETERS,devices=DEVICES,
                        dbTimeWindow=DATABASE_SIZE_SECONDS,parkingTime=PARKING_TIME)
        Config_extender.__init__(self)
        self.imgpeintre  = Image.open(CONFFOLDER + '/pictures/peintrepalette.jpeg')
        self.sylfenlogo  = Image.open(CONFFOLDER +  '/pictures/logo_sylfen.png')
        self.file_conf_pkls = CONFFOLDER +  'smallpower_conffiles.pkl'
        self.colorPalettes   = self._loadcolorPalettes()
        conf_pkls = self.fs.load_confFile(self.file_conf_pkls,self.load_confFiles,rebuildConf)
        self.cst,self.dfConstants,self.enumModeHUB,self.dftagColorCode,self.unitDefaultColors = conf_pkls
        self.colorshades    = list(self.colorPalettes.keys())

    def load_confFiles(self):
        cst,dfConstants = _load_material_constants()
        enumModeHUB     = self._load_enum_hubmodes()
        dftagColorCode,unitDefaultColors    = self._buildColorCode()
        return cst,dfConstants,enumModeHUB,dftagColorCode,unitDefaultColors
    ###########################
    #  GENERATOR CONF FILES   #
    ###########################
    def _load_enum_hubmodes(self):
        enumModeHUB = pd.read_excel(self.file_plc_xlsm,sheet_name='Enumérations',skiprows=1).iloc[:,1:3].dropna()
        enumModeHUB=enumModeHUB.set_index(enumModeHUB.columns[0]).iloc[:,0]
        enumModeHUB.index=[int(k) for k in enumModeHUB.index]
        for k in range(100):
            if k not in enumModeHUB.index:
                enumModeHUB.loc[k]='undefined'
        enumModeHUB = enumModeHUB.sort_index()
        enumModeHUB = enumModeHUB.to_dict()
        return enumModeHUB

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
        listTags_wo_color=[k for k in self.alltags if k not in list(dftagColorCode.index)]
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
    def getModeHub(self,t0,t1,*args,**kwargs):
        modeSystem = 'SEH1.Etat.HP41'
        dfmodeHUB = self.loadtags_period(t0,t1,[modeSystem],*args,**kwargs)
        # dfmodeHUB = dfmodeHUB.dropna().astype(int)
        dfmodeHUB.columns=['value']
        dfmodeHUB['mode hub']=dfmodeHUB.applymap(lambda x:self.enumModeHUB[x])
        return dfmodeHUB

    def repartitionPower(self,t0,t1,*args,expand='groups',groupnorm='percent',**kwargs):
        dfs=[]
        armoireTotal = self.getTagsTU('SEH0\.JT.*JTW_')
        dfPtotal = self.loadtags_period(armoireTotal,timeRange,*args,**kwargs)

        if expand=='tags':
            puissancesTotales = self.getTagsTU('JTW_00')
            powertags = self.getTagsTU('JTW')
            powertags = [t for t in powertags if t not in armoireTotal+puissancesTotales]
            df = self.loadtags_period(powertags,timeRange,*args,**kwargs)
            # fig = px.area(df,x='timestamp',y='value',color='tag',groupnorm=groupnorm)
            fig = px.area(df,groupnorm=groupnorm)
        elif expand=='groups':
            pg = {}
            pg['armoire'] = self.getTagsTU('EPB.*JTW')
            pg['enceinte thermique'] = self.getTagsTU('STB_HER.*JTW.*HC20')
            pg['chauffant stack'] = self.getTagsTU('STB_STK.*JTW.*HC20')
            pg['alim stack'] = self.getTagsTU('STK_ALIM.*JTW')
            pg['chauffant GV'] = self.getTagsTU('STG.*JTW')
            pg['blowers'] = self.getTagsTU('BLR.*JTW')
            pg['pompes'] = self.getTagsTU('PMP.*JTW')
            d = pd.DataFrame.from_dict(pg,orient='index').melt(ignore_index=False).dropna()['value']
            d = d.reset_index().set_index('value')
            allTags = list(d.index)

            df = self.loadtags_period(allTags,timeRange,*args,**kwargs)
            df = df.melt(value_name='value',var_name='tag',ignore_index=False)
            df['group']=df.tag.apply(lambda x:d.loc[x])
            fig=px.area(df,x=df.index,y='value',color='group',groupnorm=groupnorm,line_group='tag')
            fig.update_layout(legend=dict(orientation="h"))
            try:
                for k in dfPtotal.columns:
                    fig.add_traces(go.Scatter(x=dfPtotal.index,y=dfPtotal[k],name=k,
                        mode='lines+markers',marker=dict(color='blue')))
            except:
                print('total power not available')
            fig.update_layout(yaxis_title='power in W')
            self.standardLayout(fig)
        return fig,None

    def bilan_echangeur(self,t0,t1,tagDebit='L400',echangeur='CND_03',**kwargs):
        cdn1_tt = self.getTagsTU(echangeur + '.*TT')
        debitEau = self.getTagsTU(tagDebit + '.*FT')
        listTags = cdn1_tt + debit
        if isinstance(timeRange,list) :
            df   = self.loadtags_period(listTags,timeRange,**kwargs)
        if df.empty:
            return df
        debitEau_gs = df[debitEau]*1000/3600
        deltaT = df[cdn3_tt[3]]-df[cdn3_tt[1]]
        puissance_echangee = debitEau_gs*self.cst.Cp_eau_liq*deltaT
        varUnitsCalculated = {
            'debit eau(g/s)':{'unit':'g/s','var':debitEau_gs},
            'delta température ' + echangeur:{'unit':'°C','var':deltaT},
            'puissance echangée ' + echangeur:{'unit':'W','var':puissance_echangee},
        }
        return df, varUnitsCalculated

    def bilan_valo(self,t0,t1,*args,**kwargs):
        '''
        - timeRange : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''
        debit_eau = self.getTagsTU('L400.*FT')#kg/h
        cdn1_tt = self.getTagsTU('CND_01.*TT')
        cdn3_tt = self.getTagsTU('CND_03.*TT')
        hex1_tt = self.getTagsTU('HPB_HEX_01')
        hex2_tt = self.getTagsTU('HPB_HEX_02')
        vannes  = self.getTagsTU('40[2468].*TV')
        vanne_hex1, vanne_hex2, vanne_cdn3, vanne_cdn1 = vannes

        t_entree_valo='_TT_02.HM05'
        t_sortie_valo='_TT_04.HM05'
        listTags = debit_eau + cdn1_tt + cdn3_tt + hex1_tt + hex2_tt + vannes

        if isinstance(timeRange,list) :
            df   = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if df.empty:
            return df

        debitEau_gs = df[debit_eau].squeeze()*1000/3600
        nbVannes = df[vannes].sum(axis=1)##vannes NF 0=fermée
        debitUnitaire = debitEau_gs/nbVannes

        deltaT = df[cdn3_tt[3]]-df[cdn3_tt[1]]
        echange_cnd3 = debitUnitaire*self.cst.Cp_eau_liq*deltaT

        varUnitsCalculated = {
            'debit eau(g/s)':{'unit':'g/s','var':debitEau_gs},
            'nombres vannes ouvertes':{'unit':'#','var':nbVannes},
            'debit eau unitaire':{'unit':'g/s','var':debitUnitaire},
            'delta température':{'unit':'°C','var':deltaT},
            'puissance echange condenseur 3':{'unit':'W','var':echange_cnd3},
        }
        return df, varUnitsCalculated

    def rendement_GV(self,t0,t1,*args,activePower=True,wholeDF=False,**kwargs):
        '''
        - activePower : active or apparente power
        - timeRange : int if realTime==True --> ex : 60*30*2
        [str,str] if not realtime --> ex : ['2021-08-12 9:00','2020-08-13 18:00']'''

        debit_eau = self.getTagsTU('L213_H2OPa.*FT')#g/min
        if activePower:p_chauffants = self.getTagsTU('STG_01a.*JTW')
        else: p_chauffants = self.getTagsTU('STG_01a.*JTVA')
        t_entree_GV = self.getTagsTU('GWPBH_TT')
        t_sortie_GV = self.getTagsTU('L036.*TT')
        TT07 = self.getTagsTU('STG_01a.*TT_02')

        listTags = debit_eau+p_chauffants+t_entree_GV + t_sortie_GV+TT07
        df = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        debitEau_gs = df[debit_eau].squeeze()/60

        #calcul
        power_chauffe_eau_liq = debitEau_gs*self.cst.Cp_eau_liq*(100-df[t_entree_GV].squeeze())
        power_chauffe_eau_liq = power_chauffe_eau_liq.apply(lambda x :max(0,x))
        power_vapo_eau = debitEau_gs*self.cst.Cl_H2O
        power_chauffe_vap = debitEau_gs*self.cst.Cp_eau_vap*(df[t_sortie_GV].squeeze()-100)
        power_chauffe_vap = power_chauffe_vap.apply(lambda x :max(0,x))
        power_total_chauffe = power_chauffe_eau_liq + power_vapo_eau +  power_chauffe_vap
        power_elec_chauffe = df[p_chauffants].sum(axis=1)
        rendement_GV = power_total_chauffe/power_elec_chauffe*100
        rendement_GV_rollmean= rendement_GV.rolling('3600s').mean()
        varUnitsCalculated = {
            'puissance chauffe eau liquide':{'unit':'W','var':power_chauffe_eau_liq},
            'puissance vaporisation eau':{'unit':'W','var':power_vapo_eau},
            'puissance chauffe vaporisation':{'unit':'W','var':power_chauffe_vap},
            'puissance totale de chauffe':{'unit':'W','var':power_total_chauffe},
            'puissance electrique de chauffe':{'unit':'W','var':power_elec_chauffe},
            'rendement GV':{'unit':'%','var':rendement_GV},
            'rendement GV (moyennes)':{'unit':'%','var':rendement_GV},
        }
        return df,varUnitsCalculated

    def pertes_thermiques_stack(self,t0,t1,*args,fuel='N2',activePower=True,**kwargs):
        air_entreeStack = self.getTagsTU('HTBA.*HEX_02.*TT.*01')[0]
        air_balayage = self.getTagsTU('HPB.*HEX_02.*TT.*02')[0]
        fuel_entreeStack = self.getTagsTU('HTBF.*HEX_01.*TT.*01')[0]
        TstackAir = self.getTagsTU('GFC_02.*TT')[0]
        TstackFuel = self.getTagsTU('GFC_01.*TT')[0]
        debitAir = self.getTagsTU('l138.*FT')[0]
        debitFuel = self.getTagsTU('l032.*FT')[0]
        p_chauffants = self.getTagsTU('STK_HER.*JTW')

        listTags = [air_entreeStack,air_balayage,fuel_entreeStack,TstackAir,TstackFuel,debitAir,debitFuel]+p_chauffants

        if isinstance(timeRange,list) :
            df   = self.loadtags_period(listTags,timeRange,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        cp_fuel,M_fuel = self.dfConstants.loc['Cp_' + fuel,'value'],self.dfConstants.loc['Mmol_' + fuel,'value']
        cp_air,M_air = self.cst.Cp_air,self.cst.Mmol_Air
        debitAir_mols = df[debitAir].squeeze()/22.4/60
        debitAirBalayage_mols = df[debitAir].squeeze()/22.4/60
        debitFuel_mols = df[debitFuel].squeeze()/22.4/60
        surchauffe_Air  = (df[TstackAir]-df[air_entreeStack])*cp_air*M_air*debitAir_mols
        surchauffe_Fuel = (df[TstackFuel]-df[fuel_entreeStack])*cp_fuel*M_fuel*debitFuel_mols
        surchauffe_AirBalayage = (df[TstackAir]-df[air_entreeStack])*cp_air*M_air*debitAirBalayage_mols
        total_puissance_surchauffe_gaz = surchauffe_Air + surchauffe_Fuel + surchauffe_AirBalayage
        puissance_four = df[p_chauffants].sum(axis=1)
        pertes_stack = puissance_four/total_puissance_surchauffe_gaz

        varUnitsCalculated = {
            'debit air(mol/s)':{'unit':'mol/s','var':debitAir_mols},
            'debit fuel(mol/s)':{'unit':'mol/s','var':debitFuel_mols},
            'surchauffe air':{'unit':'W','var':surchauffe_Air},
            'surchauffe fuel':{'unit':'W','var':surchauffe_Fuel},
            'surchauffe air balayage':{'unit':'W','var':surchauffe_AirBalayage},
            'total puissance surchauffe gaz':{'unit':'W','var':total_puissance_surchauffe_gaz},
            'puissance four':{'unit':'W','var':puissance_four},
            'pertes stack':{'unit':'W','var':pertes_stack},
        }
        return df,varUnitsCalculated

    def rendement_blower(self,t0,t1,*args,activePower=True,**kwargs):
        debitAir = self.getTagsTU('138.*FT')
        pressionAmont_a,pressionAmont_b = self.getTagsTU('131.*PT')
        pressionAval = self.getTagsTU('138.*PT')[0]
        puissanceBlowers = self.getTagsTU('blr.*02.*JT')
        t_aval = self.getTagsTU('l126')
        listTags = debitAir+[pressionAmont_a,pressionAmont_b]+[pressionAval]+t_aval+puissanceBlowers

        df   = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if not df.empty:
            df = df[listTags]
            debitAirNm3 = df[debitAir]/1000/60
            deltaP2a_Pa = (df[pressionAval]-df[pressionAmont_a])*100
            deltaP2b_Pa = (df[pressionAval]-df[pressionAmont_b])*100
            deltaP_moyen = (deltaP2a_Pa + deltaP2b_Pa)/2
            p_hydraulique = debitAirNm3.squeeze()*deltaP_moyen
            p_elec = df[puissanceBlowers].sum(axis=1)
            rendement_blower = p_hydraulique/p_elec

        varUnitsCalculated = {
            'debit air(Nm3/s)':{'unit':'Nm3/s','var':debitAirNm3},
            'deltap blower a':{'unit':'Pa','var':deltaP2a_Pa},
            'deltap blower b':{'unit':'Pa','var':deltaP2b_Pa},
            'deltap moyen':{'unit':'mbarg','var':deltaP_moyen},
            'puissance hydraulique':{'unit':'W','var':deltaP_moyen},
            'puissance electrique':{'unit':'W','var':p_elec},
            'rendement blower':{'unit':'%','var':rendement_blower},
            }
        return df,varUnitsCalculated

    def rendement_pumpRecircuFroid(self,t0,t1,*args,activePower=True,**kwargs):
        ### compliqué débit amont
        debitAmont   = self.getTagsTU('303.*FT')+''#???
        debitAval = self.getTagsTU('L032.*FT')
        t_aval = self.getTagsTU('L032.*TT')
        pressionAval = ''#???
        puissancePump = self.getTagsTU('gwpbh.*pmp_01.*JTW')
        listTags = debitAmont + debitAval +t_aval + pressionAval + puissancePump
        df   = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if df.empty:
            return df
        df = df[listTags]
        dfPump = pd.DataFrame()
        dfPump['debit eau total(Nm3/s)'] = (df['debit eau1(g/min)']+df['debit eau2(g/min)'])/1000000/60
        Pout = df['pressionAval(mbarg)']*100
        dfPump['puissance hydraulique(W)'] = dfPump['debit eau total(Nm3/s)']*dfPump['pression sortie(Pa)']
        dfPump['rendement pompe'] = dfPump['puissance hydraulique(W)']/df['puissance pump(W)']*100
        dfPump['cosphiPmp'] = df['puissance pump(W)']/(df['puissance pump(W)']+df['puissance pump reactive (VAR)'])
        varUnitsCalculated = {

        }
        df.columns=[k + ' : ' + l  for k,l in zip(df.columns,listTags)]
        df = pd.concat([df,dfPump],axis=1)
        return df,varUnitsCalculated

    def cosphi(self,t0,t1,*args,**kwargs):
        extVA = 'JTVA_HC20'
        extVAR ='JTVAR_HC20'
        extW ='JTW'
        tagsVA = self.getTagsTU(extVA)
        tagsVAR = self.getTagsTU(extVAR)
        tagsJTW = self.getTagsTU(extW)
        racineVA = [tag.split(extVA)[0] for tag in tagsVA]
        racineVAR = [tag.split(extVAR)[0] for tag in tagsVAR]
        racineW = [tag.split(extW)[0] for tag in tagsJTW]
        tags4Cosphi = list(set(racineVA)&set(racineW))

        jtvas,jtws=[],[]
        for t in tags4Cosphi:
            jtvas.append([tag for tag in tagsVA if t in tag][0])
            jtws.append([tag for tag in tagsJTW if t in tag][0])

        listTags = jtvas + jtws
        if isinstance(timeRange,list):
            df = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if df.empty:
            return df
        cosphi = {t:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw,t in zip(jtvas,jtws,tags4Cosphi)}
        # cosphi = {jtva+'/'+jtw:{'unit':'cosphi','var':df[jtva].squeeze()/df[jtw].squeeze()} for jtva,jtw in zip(jtvas,jtws)}
        return df,cosphi

    def fuitesAir(self,t0,t1,*args,**kwargs):
        airAmont = self.getTagsTU('l138.*FT')[0]
        airAval = self.getTagsTU('l118.*FT')[0]
        Istacks = self.getTagsTU('STK.*IT.*HM05')
        Tfour = self.getTagsTU('STB_TT_02')[0]
        pressionCollecteur = self.getTagsTU('GFC_02.*PT')[0]
        pressionDiffuseur = self.getTagsTU('GFD_02.*PT')[0]

        listTags =[airAmont,airAval]+Istacks+[Tfour]+[pressionCollecteur,pressionDiffuseur]
        df = self.loadtags_period(t0,t1,listTags,*args,**kwargs)

        if df.empty:
            return pd.DataFrame()
        df = df[listTags]

        # sum courant stacks
        Itotal = df[Istacks].sum(axis=1)
        # production O2
        F = self.dfConstants.loc['FAR'].value
        Po2mols = Itotal*25/(4*F) ##25 cells
        Po2Nlmin = Po2mols*22.4*60
        # fuite air
        # QairAval = df[airAval] + Po2Nlmin
        QairAval = df[airAval] - Po2Nlmin
        fuiteAir = df[airAmont]-(QairAval)
        txFuite = fuiteAir/df[airAmont]*100
        coefficientDeFuite = fuiteAir/df[pressionDiffuseur]

        dfmodeHUB=self.getModeHub(t0,t1,*args,**kwargs)
        # dfmodeHUB=self.getModeHub(timeRange,rs=rs)

        varUnitsCalculated = {
            'courrant stacks total':{'unit':'A','var':Itotal},
            'production O2(mol/s)':{'unit':'mol/s','var':Po2mols},
            'production O2(Nl/min)':{'unit':'Nl/min','var':Po2Nlmin},
            'flux air aval(aval + production O2)':{'unit':'Nl/min','var':QairAval},
            'fuite air':{'unit':'Nl/min','var':fuiteAir},
            'taux de fuite air':{'unit':'%','var':txFuite},
            'coefficient de fuite':{'unit':'N/min/mbar','var':coefficientDeFuite},
            'mode hub':{'unit':'mode hub','var':dfmodeHUB['value']}
        }
        # update mode and hovers
        listTexts={'mode hub':dfmodeHUB['mode hub']}
        return df,varUnitsCalculated,listTexts

    def fuitesFuel(self,t0,t1,*args,**kwargs):
        '''
        Gonflage :
        - L035 ou L040 fermées et L039 fermée et L027 fermée
        - fuites fuel BF = L303 + L041 (+ Somme i x 25 / 2F)  note : normalement dans ce mode le courant est nul.
        Boucle fermée recirculation à froid (mode pile)
        - L026 et L029 fermées, L027 ouverte, L035 OU L040 fermées
        - fuites fuel BF = L303 + L041 + Somme i x 25 / 2F
        Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        - (L035 ET L040 ouvertes) ou L026 ouverte ou L029 ouverte
        - fuite ligne fuel BO = L303 + L041 + Somme i x 25 / 2F – L025
        Fonctionnement mode gaz naturel :
        - L027 fermée, L039 ouverte
        - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025
        En résumé : trois calculs possibles du débit de fuite fuel
        Le même calcul pour les cas 1 et 2 qui sont « fermés »
        Un calcul pour le mode ouvert électrolyse ou boucle ouverte pendant les transitions
        Un calcul pour le mode gaz naturel.
        '''

        vanne26 = self.getTagsTU('l026.*ECV')[0]#NO
        vanne27 = self.getTagsTU('l027.*ECV')[0]#NO
        vanne29 = self.getTagsTU('l029.*ECV')[0]#NF
        vanne35 = self.getTagsTU('l035.*ECV')[0]#NF
        vanne39 = self.getTagsTU('l039.*ECV')[0]#NF
        vanne40 = self.getTagsTU('l040.*ECV')[0]#NF
        vannes = [vanne26,vanne27,vanne29,vanne35,vanne39,vanne40]
        Istacks = self.getTagsTU('STK.*IT.*HM05')

        L025=self.getTagsTU('l025.*FT')[0]
        L032=self.getTagsTU('l032.*FT')[0]
        L041=self.getTagsTU('l041.*FT')[0]
        L303=self.getTagsTU('l303.*FT')[0]
        Tfour = self.getTagsTU('STB_TT_02')
        pressionStacks = self.getTagsTU('GF[CD]_01.*PT')

        debits =[L303,L041,L032,L025]
        listTags = vannes+Istacks+debits+pressionStacks+Tfour

        start = time.time()
        df = self.loadtags_period(listTags,timeRange,*args,**kwargs)
        if df.empty:
            print('no data could be loaded')
            return pd.DataFrame()

        print('loading data in {:.2f} milliseconds'.format((time.time()-start)*1000))
        #############################
        # compute Hydrogen production
        #############################

        Itotal = df[Istacks].sum(axis=1)
        F = self.dfConstants.loc['FAR'].value
        PH2mols = Itotal*25/(2*F) ##25 cells
        PH2Nlmin = PH2mols*22.4*60

        #############################
        # dtermine mode fuel
        #############################

        # convert vannes to bool
        for v in vannes:df[v]=df[v].astype(bool)
        dfModes={}
        # ~df[vanne]==>fermé si NF mais df[vanne]==>ouvert si NO
        # Gonflage :
        # L035 ou L040 fermées et L039 fermée et L027(NO==>0:ouvert) fermée
        dfModes['gonflage'] = (~df[vanne35] | ~df[vanne40]) & (~df[vanne39]) & (df[vanne27])
        # fuites fuel BF = L303 + L041 (+ Somme i x 25 / 2F)  note : normalement dans ce mode le courant est nul.

        # Boucle fermée recirculation à froid (mode pile):
        # L026(NO) et L029 fermées, L027(NO) ouverte, L035 OU L040 fermées
        dfModes['recircuFroidPile']=(df[vanne26]) & (~df[vanne29]) & (~df[vanne27]) & (~df[vanne35]) | (~df[vanne40])
        # fuites fuel BF = L303 + L041 + Somme i x 25 / 2F
        fuitesFuelBF = df[L303] + df[L041] + PH2Nlmin

        # Boucle ouverte (fonctionnement électrolyse ou boucle ouverte pendant les transitions) :
        # (L035 ET L040 ouvertes) ou L026(NO) ouverte ou L029 ouverte
        dfModes['bo_electrolyse']=(df[vanne35] & df[vanne40]) | (~df[vanne26]) | (df[vanne29])
        # - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025
        fuitesFuelBO = df[L303] + df[L041] + PH2Nlmin - df[L025]
        # Fonctionnement mode gaz naturel :
        # - L027(NO) fermée, L039 ouverte
        dfModes['gaz_nat']=(df[vanne27] & df[vanne39])
        fuitesFuelBO_GN = (df[L032] - df[L303])*4 + df[L303] + df[L041] + PH2Nlmin - df[L025]
        # - fuites fuel BO = (L032 – L303) x 4 + L303 + L041 + Somme i x 25 / 2F – L025

        # check wether they are multiple modes or exclusive modes
        dfModeFuel= [v.apply(lambda x: k+'/' if x==True else '') for k,v in dfModes.items()]
        dfModeFuel = pd.concat(dfModeFuel,axis=1).sum(axis=1).apply(lambda x : x[:-1])
        modesFuel = {v:k for k,v in enumerate(dfModeFuel.unique())}
        modeFuelInt = dfModeFuel.apply(lambda x:modesFuel[x])

        #determine if pileBF or pileBO
        pileBF = [k for k in modesFuel.keys() if 'recircuFroidPile' in k or 'gonflage' in k]
        pileBF = dfModeFuel.apply(lambda x: True if x in pileBF else False)
        dfs=pd.concat([fuitesFuelBO,fuitesFuelBF],axis=1)
        dfs.columns=['BO','BF']
        dfs['pileBF'] = pileBF

        #get fuel fuites in either mode
        fuitesFuel =dfs.apply(lambda x: x['BO'] if x['pileBF'] else x['BF'],axis=1)

        # Vérif débitmètres ligne fuel BF = L032 FT – L303 – L025
        verifDebitmetre = df[L032]-df[L303]-df[L025]

        # get mode Hub
        dfmodeHUB=self.getModeHub(timeRange,**kwargs)

        # define names and scales
        varUnitsCalculated ={
            'courrant stacks total':{'unit':'A','var':Itotal},
            'production H2(mol/s)':{'unit':'mol/s','var':PH2mols},
            'production H2(Nl/min)':{'unit':'Nl/min','var':PH2Nlmin},
            'fuites fuel BF':{'unit':'Nl/min','var':fuitesFuelBF},
            'fuites fuel BO':{'unit':'Nl/min','var':fuitesFuelBO},
            'fuites fuel':{'unit':'Nl/min','var':fuitesFuel},
            'debit 32 - 303 - 25':{'unit':'Nl/min','var':verifDebitmetre},
            'pile BF':{'unit':'etat Pile BF','var':pileBF.astype(int)},
            'mode_Fuel':{'unit':'etat mode Fuel','var':modeFuelInt},
            'mode hub':{'unit':'mode hub','var':dfmodeHUB['value']}
            }

        listTexts={'mode_Fuel':dfModeFuel,'mode hub':dfmodeHUB['mode hub']}
        print('figure computed in in {:.2f} milliseconds'.format((time.time()-start)*1000))
        return df,varUnitsCalculated,listTexts

    def compute_continuousMode_hours(df,modus=10):
        '''10:soec,20:sofc'''
        # df_modes= pd.DataFrame.from_dict(cfg.enumModeHUB,orient='index',columns=['mode'])
        # df_modes[df_modes['mode']==modus]
        ## fill the data every 1 minute
        dfmode=df.resample('60s',closed='right').ffill()
        ## keep only data for the corresponding mode
        dfmode=dfmode[dfmode['value']==modus]
        ## compute delta times
        deltas=dfmode.reset_index()['timestampUTC'].diff().fillna(pd.Timedelta('0 minutes'))
        ## sum the delta only if they are smaller than 1minute and 1 second
        return deltas[deltas<pd.Timedelta('1 minute,1 second')].sum()

    def compute_H2_produced(df,modus=10):
        tag_mode=['SEH1.Etat.HP41']
        tagDebitH2 = cfg.getTagsTU('L025.*FT.*HM05')
        tagsCurrent = cfg.getTagsTU('alim.*IT_HM05')

        df_etathp41=self.loadtags_period(t0,t1,tag_mode)
        dfmode = df_etathp41.resample('10s',closed='right').ffill()
        dfmode = dfmode[dfmode['value']==10]
        df_debitH2 = self.loadtags_period(t0,t1,tagDebitH2)[['value']]
        I_stacks = self.loadtags_period(t0,t1,tagsCurrent)
        Itotal = I_stacks.sum(axis=1).drop_duplicates()
        Itotal = Itotal.resample('10s').ffill().loc[dfmode.index]
        PH2mol_s = Itotal*25/(2*cfg.cst.FAR) ##25 cells
        PH2Nlmin = PH2mol_s*22.4*60
        df_debit = df_debitH2.resample('10s').ffill().loc[dfmode.index] ##Nl/min
        H2_produit =(df_debit/60).sum()*10/1000 #Nm3
        H2_produit_I =(PH2Nlmin/60).sum()*10/1000 #Nm3

    def get_I_V_cara():
        tag_mode=['SEH1.Etat.HP41']
        tagsCurrent=cfg.getTagsTU('alim.*IT_HM05')
        tagsVoltage=cfg.getTagsTU('alim.*ET_HM05')
        df_etathp41=readbourinparkedtags(folderpkl,tag_mode,t0,t1)
        df_stack_sn=readbourinparkedtags(folderpkl,tagsStack_sn,t0,t1)
        h_soec,h_sofc=[compute_continuousMode_hours(df_etathp41,m) for m in [10,20]]
        df_cara = df_cara.reset_index().drop_duplicates().set_index('timestampUTC')
        df_cara = processdf(cfg,df_cara,rs = '60s')
        df_cara.to_pickle('df_cara.pkl')

    def plot_I_V_cara():
        ### filter time electrolysis
        tagsCurrent=cfg.getTagsTU('alim.*IT_HM05')
        tagsVoltage=cfg.getTagsTU('alim.*ET_HM05')
        df_cara=pickle.load(open('df_cara.pkl','rb'))
        df2 = df_cara.resample('300s').mean()
        fig=go.Figure()
        for i,v in zip(tagsCurrent,tagsVoltage):
            x=df2[i]
            y=df2[v]
            x=-x[x.abs()>0.1]
            x=x[x<24]
            x=x[x>-60]
            y=y[x.index]
            fig.add_trace(go.Scatter(x=x,y=y,name=i))

        fig.update_traces(mode='markers')
        fig.update_xaxes(title_text='Current (A)')
        fig.update_yaxes(range=[-5,50],title_text='Voltage (V DC)')
        fig.show()

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

    def plotIndicator(self,df,varUnitsCalculated,listTexts={}):
        if isinstance(df,type(go.Figure())):
            return df

        dfCalc = pd.concat([pd.DataFrame(s['var']) for s in varUnitsCalculated.values()],axis=1)
        dfCalc.columns = list(varUnitsCalculated.keys())
        unitGroups={}
        unitGroups.update({k:v['unit'] for k,v in varUnitsCalculated.items()})
        df2_plot=pd.concat([dfCalc,df])
        unitGroups.update({t:self.getUnitofTag(t) for t in df.columns})

        fig = self.utils.multiUnitGraph(df2_plot,unitGroups)
        # fig = self.multiUnitGraphSP(df2_plot,unitGroups)
        fig = self.standardLayout(fig)
        # update mode and hovers
        vanneTags=[k for k in df.columns if 'ECV' in k]
        fig.for_each_trace(
            lambda trace: trace.update(line_shape="hv") if trace.name in vanneTags else (),
        )
        hovertemplatemode='<b>%{y:.2f}' + '<br>     mode:%{text}'
        for k,v in listTexts.items():
            fig.update_traces(selector={'name':k},
                    hovertemplate=hovertemplatemode,
                    text=v,line_shape='hv')
        return fig

    def multiUnitGraphShades(self,df):
        tagMapping = {t:self.getUnitofTag(t) for t in df.columns}
        fig = self.utils.multiUnitGraph(df,tagMapping)
        dfGroups = self.utils.getLayoutMultiUnit(tagMapping)[1]
        listCols = dfGroups.color.unique()
        for k1,g in enumerate(listCols):
            colname = self.colorshades[k1]
            shades = self.colorPalettes[colname]['hex']
            names2change = dfGroups[dfGroups.color==g].index
            fig.update_yaxes(selector={'gridcolor':g},
                        title_font_color=colname[:-1],gridcolor=colname[:-1],tickfont_color=colname[:-1])
            shade=0
            for d in fig.data:
                if d.name in names2change:
                    d['marker']['color'] = shades[shade]
                    d['line']['color']   = shades[shade]
                    shade+=1
            fig.update_yaxes(showgrid=False)
            fig.update_xaxes(showgrid=False)

        # fig.add_layout_image(dict(source=self.imgpeintre,xref="paper",yref="paper",x=0.05,y=1,
        #                             sizex=0.9,sizey=1,sizing="stretch",opacity=0.5,layer="below"))
        # fig.update_layout(template="plotly_white")
        fig.add_layout_image(
            dict(
                source=self.sylfenlogo,
                xref="paper", yref="paper",
                x=0., y=1.02,
                sizex=0.12, sizey=0.12,
                xanchor="left", yanchor="bottom"
            )
        )
        return fig

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

class SmallPower_VM(VersionManager_daily,Config_extender):
    def __init__(self,**kwargs):
        Config_extender.__init__(self)
        VersionManager_daily.__init__(self,FOLDERPKL,CONFFOLDER + "/PLC_config/",pattern_plcFiles='*ALPHA*.xlsm',**kwargs)
        self.all_not_ds_history = list(pd.concat([pd.Series(dfplc.index[~dfplc.DATASCIENTISM]) for dfplc in self.df_plcs.values()]).unique())
        self.versionsStart = {
            '2.10':'2021-05-27',
            '2.13':'2021-06-21',
            '2.14':'2021-06-23',
            '2.15':'2021-06-29',
            '2.16':'2021-07-01',
            '2.18':'2021-07-07',
            '2.20':'2021-08-02',
            '2.21':'2021-08-03',
            '2.22':'2021-08-05',
            '2.24':'2021-09-23',
            '2.26':'2021-09-30',
            '2.27':'2021-10-07',
            '2.28':'2021-10-12',
            '2.29':'2021-10-18',
            '2.30':'2021-11-02',
            '2.31':'2021-11-08',
            '2.32':'2021-11-24',
            '2.32':'2021-11-24',
            '2.34':'2021-11-25',
            '2.35':'2021-11-25',
            '2.36':'2021-11-29',
            '2.37':'2021-12-09',
            '2.40':'2021-12-14',
            '2.42':'2022-01-10',
        }

    def load_PLC_versions(self):
        print('Start reading all .xlsm files....')
        df_plcs = {}
        for f,v in self.dicVersions.items():
            print(f)
            df_plcs[v] = pd.read_excel(f,sheet_name='FichierConf_Jules',index_col=0)
        print('')
        print('concatenate tags of all dfplc verion')
        all_tags_history = list(pd.concat([pd.Series(dfplc.index[dfplc.DATASCIENTISM]) for dfplc in df_plcs.values()]).unique())
        return df_plcs,all_tags_history

    def remove_notds_tags(self,*args,**kwargs):
        self.streamer.remove_tags_daily(self.all_not_ds_history,self.folderData,*args,**kwargs)
