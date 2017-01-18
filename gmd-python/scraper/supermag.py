
class StdQuery:
    def __init__(self,start=None,interval=None):

        self.host = "http://supermag.jhuapl.edu/mag/lib/services/"
        self.proxydict = {'http':'proxyout.lanl.gov:8080', 'https':'proxyout.lanl.gov:8080'}

        self.user = "ambrosiano"

        # self.start = start
        # self.interval = interval
        self.start = "2000-03-25T00:00:00.000Z"
        #self.interval = "23&3A59"
        #self.interval = "01&3A00"
        self.interval = "00:01"

        self.service = "mag"
        self.stations = ["THL", "RES", "MBC", "CBB", "GDH", "BLC",
            "BJN", "BRW", "JAN", "YKC", "FCC", "NAQ", "PBQ",
            "CMO", "ABK", "LRV", "SOD", "MEA", "GLN", "SIT", "LER", "OTT",
            "LOV", "NEW", "VIC", "STJ", "ESK", "BFE", "WNG", "BOU", "FRD",
            "HAD", "BEL", "CLF", "FRN", "BSL", "TUC", "DLR", "MMB", "KAK",
            "SJG", "HTY", "KNY", "HON", "LNP", "MBO", "PPT", "HBK", "HER",
            "AMS", "CZT", "PAF", "SPA", "DVS", "MCM", "DRV", "CSY"]
        self.stations_str = self.stations[0]
        for i in range(1,len(self.stations)):
            self.stations_str+= ","+self.stations[i]

        self.fullstring = "SPA,B23,B21,B22,B19,B20,PG1,B18,PG2,PG3,B17,B16,PG4,B14,B15,B27,SBA,VOS,B12,B13,MCM," +\
        "B11,B10,DMC,B09,B08,B07,B24,NVL,VNA,DVS,PRG,DRV,MAW,B04,B05,B06,B03,CSY,MIR,AIA,B02,PAL," +\
        "GML,LOV,FCC,RAL,FVE,C02,LER,SMI,KAR,TAR,LNN,YAK,MGD,KVI,HOM,C03,T29,T44,AMU,EKP,NUR,UPS,T38," +\
        "GRK,T46,T53,YKC,FSP,MEK,FHB,NAQ,RAN,DOB,SOL,HAN,GAK,FAR,HLM,TLK,TRP,T39,T47,BLC,LRV,GHB,DAW," +\
        "IQA,HLL,S01,T35,T40,SKT,AMK,RVK,LYC,OUJ,EAG,CMO,CGO,PKR,ARK,CDC,CHC,OUL,C07,T34,MCR,CNL,JCK," +\
        "DON,ZYK,KOT,BET,FYU,CWE,ZGN,PGC,RPB,ATU,STF,T41,CBB,ARC,INK,GDH,ABK,LEK,MUO,LOZ,KIR,SOD,PEL," +\
        "CPS,CSC,CKA,LOP,DED,NOK,UMQ,SCO,TAL,TRO,AND,ALT,KEV,MAS,KIL,KAU,IVA,KAV,NOR,JAN,SOR,CPY,AMD," +\
        "GHC,BRW,JCO,TIK,CHD,PBK,IGC,PBC,CY0,UPN,MCE,MCW,MCG,SAH,DIK,RES,KUV,DNB,MCN,BJN,TAB,SVS,KTN," +\
        "MBC,THL,DMH,HOP,HRN,CCS,HOR,NAL,LYR,BBG,VIZ,HIS,EUA,ALE,NRD"

        # "B01,LIV,OHI,ESC,ORC,KEP,MCQ,PNT,PST,ENP,PAF,CZT,EYR,TRW,LEM,HOB,VLD,OSO,PAC,TDC,AMS,CAN," +\
        # "CNB,HER,KAT,ADL,CER,GNA,SUT,PIL,GNG,SER,CUL,IPM,KMH,DAL,HBK,BSV,LMM,ASP,VSS,ANT,LRM,EWA,CTA," +\
        # "TAN,TSU,PUT,A05,TWN,VRE,PPT,SHE,NMP,API,ASA,DRW,WEP,KDU,HUA,CKI,A10,WTK,ASC,WEW,PRP,BIK,A11," +\
        # "PTN,KTB,TND,GAN,MND,BNG,A03,KOU,A06,LKW,ABJ,KOR,A08,A13,AAE,CRP,YAP,A01,A07,CEB,DLT,GUA,MBO,"+\
        # "MUT,A04,A09,A12,PNL,HYB,ABG,SJG,TGG,TEO,HON,PHU,M11,TAM,GZH,SON,LNP,M10,HLN,CBI,M09,JAI,GUI," +\
        # "MID,FIT,AMA,CDP,BSL,DLR,JAX,ELT,MLT,M08,TUC,KAG,YMK,KNY,BGY,HTY,QSB,USC,M07,KUJ,M06,T26,T27," +\
        # "LZH,FRN,SMA,KAK,TUL,DSO,SFS,E05,CYG,A02,FRD,ASH,ONW,PEG,BOU,APL,ESA,MIZ,M05,T16,BMT,SPT,TOL"
        # "BJI,ISK,TKT,EBR,T20,E02,E03,E04,M04,IZN,E01,AQU,DUR,C01,MMB,AAA,PPI,RIK,MSH,GTF,M03,T21,T23"
        # "OTT,SUA,MSR,CLK,GCK,SBL,CNH,WMQ,RNC,ASB,NKK,ODE,M02,STJ,THY,M01,C08,T17,T24,T15,T18,T25,CST"
        # "P01,VIC,NEW,CLF,FUR,HRB,NCK,YSS,BDV,VLO,BFO,C10,C11,T19,PAG,KHB,VYH,WIC,MAB,DOU,PIN,MZH,GLN"
        # "LET,T50,T51,KIV,KGD,LVV,VAL,HAD,BEL,ROT,T03,C04,C12,T30,T32,BRD,ZAG,WHS,T49,NGK,IRT,RED,SAS," +\
        # "MSK,C13,T43,C05,MEA,WNG,ISL,LAN,YOR,EDM,C06,T28,PET,SZC,PBQ,ESK,HLP,MNK,BFE,ROE,NVS,RSV,MOS," +\
        # "C09,T33,T36,T37,SUW,T52,T42,SIT,GIM,FMC,NAN,FSJ,KNZ,SHU,T22,T31,ARS,BRZ,T45,T48,BOX,BOR,CRK," +\

        self.delta = "none"
        self.baseline = "all"
        self.options = "mlt"
        self.format = "csv"

    def createDict(self):
        dict = {}
        dict["user"]=self.user
        if self.start!=None:
            dict["start"]=self.start
        if self.interval!=None:
            dict["interval"]=self.interval
        dict["service"]=self.service
        dict["stations"] =self.fullstring
        #dict["stations"]=self.stations_str
        dict["delta"]=self.delta
        dict["baseline"]=self.baseline
        dict["options"]=self.options
        dict["format"]= self.format
        return dict

