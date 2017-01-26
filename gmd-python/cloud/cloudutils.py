import os

def setproxy(proxy):
    os.environ["HTTP_PROXY"]=proxy
    os.environ["http_proxy"]=proxy
    os.environ["HTTPS_PROXY"]=proxy
    os.environ["https_proxy"]=proxy