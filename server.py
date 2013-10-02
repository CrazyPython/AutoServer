import os
import web
import traceback
import datetime
from functools import wraps

### Url mappings

urls = [
    '/', 'index',
    
]
for root, dirs, files in os.walk("C:/Users/James/Desktop/server"):
    if "web" in dirs:
        dirs.remove("web")
    for f in files:
        if "server.py" in f:
            continue
        elif "maintence.py" in f:
            continue
        elif "log.txt" in f:
            continue
        u = os.path.join(root,f)
        u=u.strip("/").strip("\\")
        ident=u.lstrip("C:/Users/James/Desktop/server").replace("/","slash").replace("\\","SLASH").replace(".","DOT") #replace invalid python expressions with valid ones
        globals()[ident] = open(u,mode='rb').read()
        exec("""
class %(classname)s:
    def GET(self):
        global %(data)s
        return %(data)s
        """%{"classname":ident+"server","data":ident}, globals(), globals())  #create a class as if were created in the global scope by passing in globals() as locals
        urls.extend((u.lstrip("C:/Users/James/Desktop/server").replace("\\","/"),ident+"server")) #use u not ident because ident has stuff like SLASH and DOT
urls = tuple(urls)
class index:
    def GET(self):
        web.setcookie('time',datetime.datetime.today(),9999999999999)
        return "<!DOCTYPE html><html><link rel=\"icon\" href=\"favicon.ico\" type=\"image/x-icon\"/>hi</html>"
class favicon:
    def GET(self):
        return open('favicon.ico',mode='rb').read()
def notfound():
    return web.notfound("<!DOCTYPE html><html><link rel=\"icon\" href=\"favicon.ico\" type=\"image/x-icon\"/><b><h1>404 Not Found</h1></b><hr/>Python Server</html>")
app = web.application(urls, globals())
app.notfound = notfound
if __name__ == '__main__':
    app.run()
