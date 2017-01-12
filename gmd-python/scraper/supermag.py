
class StdQuery:
    def __init__(self,start=None,interval=None):

        self.host = "http://supermag.jhuapl.edu/mag/lib/services/"
        self.proxydict = {'http':'proxyout.lanl.gov:8080', 'https':'proxyout.lanl.gov:8080'}

        self.user = "ambrosiano"

        # self.start = start
        # self.interval = interval
        self.start = "1990-03-25T00:00:00.000Z"
        #self.interval = "23&3A59"
        self.interval = "01&3A00"

        self.service = "mag"
        self.stations = ["THL", "2CRES", "2CMBC", "2CCBB", "2CGDH", "2CBLC",
            "2CBJN", "2CBRW", "2CJAN", "2CYKC", "2CFCC", "2CNAQ", "2CPBQ",
            "2CCMO", "2CABK", "2CLRV", "2CSOD", "2CMEA", "2CGLN", "2CSIT", "2CLER", "2COTT",
            "2CLOV", "2CNEW", "2CVIC", "2CSTJ", "2CESK", "2CBFE", "2CWNG", "2CBOU", "2CFRD",
            "2CHAD", "2CBEL", "2CCLF", "2CFRN", "2CBSL", "2CTUC", "2CDLR", "2CMMB", "2CKAK",
            "2CSJG", "2CHTY", "2CKNY", "2CHON", "2CLNP", "2CMBO", "2CPPT", "2CHBK", "2CHER",
            "2CAMS", "2CCZT", "2CPAF", "2CSPA", "2CDVS", "2CMCM", "2CDRV", "2CCSY"]
        self.delta = "none"
        self.baseline = "all"
        self.options = "mlt"
        self.format = "csv"
        self.testquery = "user=ambrosiano&start=1990-03-25T00:00:00.000Z&interval=01%3A00&service=mag&stations=THL&delta=none&baseline=all&options=+mlt&format=csv"

    def createDict(self):
        dict = {}
        dict["user"]=self.user
        if self.start!=None:
            dict["start"]=self.start
        if self.interval!=None:
            dict["interval"]=self.interval
        dict["service"]=self.service
        dict["stations"]=self.stations
        dict["delta"]=self.delta
        dict["baseline"]=self.baseline
        dict["options"]=self.options
        dict["format"]= self.format
        return dict

