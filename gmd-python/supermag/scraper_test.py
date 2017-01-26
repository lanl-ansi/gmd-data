import requests
from scraper.supermag import StdQuery


if __name__=="__main__":
    q = StdQuery()

    print("data=" + str(q.createParamsDict()))

    r = requests.get(q.host, proxies=q.proxydict, params=q.createParamsDict(), stream=True)

    print("Status="+str(r.status_code))
    print(dict(r.headers))

    filename = './supermag_test.csv'

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)

    fd.close()

