
class SupermagParams:
    def __init__(self,start=None,interval=None,stationString=None):

        self.host = "http://supermag.jhuapl.edu/mag/lib/services/"
        self.proxydict = {'http':'proxyout.lanl.gov:8080', 'https':'proxyout.lanl.gov:8080'}

        self.start = start
        self.interval = interval
        self.stationString = stationString
        self.user = "ambrosiano"
        self.service = "mag"
        self.delta = "none"
        self.baseline = "all"
        self.options = "mlt"
        self.format = "csv"


    def createParamsDict(self):
        dict = {}
        dict["user"]=self.user
        dict["start"]=self.start
        dict["interval"]=self.interval
        dict["service"]=self.service
        dict["stations"] = self.stationString
        dict["delta"]=self.delta
        dict["baseline"]=self.baseline
        dict["options"]=self.options
        dict["format"]= self.format
        return dict

