import requests
import re

class Scanner:
    def __init__(self, url):
        self.url = url
        self.scannedLinks = []
        self.unscannedLinks = []
        self.foundImages = []

    def __scanPage(self, page_url, file):
        r = requests.get(page_url)
        html = re.sub(r"\'", "\"", r.text)
        imgElements = re.findall(r"<img [a-zA-Z0-9\=\"\-\/:.;_ \\?]{1,1000}>", html)
        aElements = re.findall(r"<a [a-zA-Z0-9\=\"\-\/:.;_ \\?]{1,1000}>", html)
        
        print("Scanning \"{0}\", found {1} images and {2} links;".format(page_url, len(imgElements), len(aElements)))
        
        for element in imgElements:
            src = re.findall(r"src=\"[a-zA-Z0-9:\=\/.\-_?]{1,500}\"|$", element)
            src = re.sub(r"src=|\"", "", src[0])

            if (src not in self.foundImages):
                file.write("<a href=\"https://yandex.com/images/search?rpt=imageview&url={0}\"><img src=\"{0}\"/></a>".format(src))
                self.foundImages.append(src)
        
        for element in aElements:
            link = re.findall(r"href=\"[a-zA-Z0-9:\=\/.\-_?]{1,500}\"|$", element)
            link = re.sub(r"href=|\"", "", link[0])

            if (link.startswith(self.url) and link not in self.unscannedLinks and link not in self.scannedLinks):
                self.unscannedLinks.append(link)

        self.scannedLinks.append(page_url)
        r.close()

    def scan(self, filePath):
        f = open(filePath, "w+")
        f.write("<html><body>")

        self.unscannedLinks.append(self.url)

        while(len(self.unscannedLinks) > 0):
            link = self.unscannedLinks.pop()
            self.__scanPage(link, f)

        f.write("</body></html>")    
        f.close()

def main():
    scanner = Scanner("") #enter url here
    scanner.scan("images.html")
    print("Finished!")

if __name__ == "__main__":
    main()