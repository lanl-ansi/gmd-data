
class StdQuery:
    def __init__(self,start=None,interval=None):

        self.host = "http://supermag.jhuapl.edu/mag/lib/services/"
        self.proxydict = {'http':'proxyout.lanl.gov:8080', 'https':'proxyout.lanl.gov:8080'}

        self.user = "ambrosiano"

        # self.start = start
        # self.interval = interval
        self.start = "1990-03-25T00:00:00.000Z"
        #self.interval = "23&3A59"
        #self.interval = "01&3A00"
        self.interval = "23:59"

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
        #dict["stations"] =["FRN"]
        dict["stations"]=self.stations_str
        dict["delta"]=self.delta
        dict["baseline"]=self.baseline
        dict["options"]=self.options
        dict["format"]= self.format
        return dict

