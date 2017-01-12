import requests
from scraper.supermag import StdQuery


if __name__=="__main__":
    q = StdQuery()

    print("data="+str(q.createDict()))

    #r = requests.post(q.host,proxies=q.proxydict,data=q.testquery,stream=True)
    r = requests.post(q.host,proxies=q.proxydict,data=q.createDict(),stream=True)

    print("Status="+str(r.status_code))
    print(dict(r.headers))

    f = str(r.raw.read())
    print(f)

