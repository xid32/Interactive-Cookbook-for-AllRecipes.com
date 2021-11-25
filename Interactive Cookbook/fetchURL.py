import urllib.request

def fetchURL(url):
   try:
      with  urllib.request.urlopen(url) as f:
         saveFile = open("url.txt", "w", encoding="utf-8"   )
         content = f.read().decode("utf-8")
         saveFile.write(content)
         saveFile.close()


   except urllib.error.URLError as e:
      print(e.reason)


