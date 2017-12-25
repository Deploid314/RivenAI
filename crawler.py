import http.client
from html.parser import HTMLParser
import re
from riven import Riven

class Crawler:
    ITEM_REGX = '.*wiki\\\/([^\\\"]+).*<\\\\\/a>","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)".*\.png[^,]+,"(\d+)'
    URL = "/spmarket.php?dev=null&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=12&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=13&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=true&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=15&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=true&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B16%5D%5Bdata%5D=16&columns%5B16%5D%5Bname%5D=&columns%5B16%5D%5Bsearchable%5D=true&columns%5B16%5D%5Borderable%5D=true&columns%5B16%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B16%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=16&order%5B0%5D%5Bdir%5D%5B%5D=desc&start=__START__&length=__LENGTH__&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1511410440664"

    def getItemsForSale(self):
        """Get Items for sale"""
        start = 0
        length = 1000
        rivens = []
        while True:
            data = self.sendRequest(start,length)
            rivensCurPage = self.parseRequest(data)
            rivens.extend(rivensCurPage)
            start = start + length
            """if True:
                print("Done with scan")
                break;"""

            if len(rivensCurPage) < length:
                print("Done with scan")
                break;

        return rivens

    def sendRequest(self, start, length):
        print(start, length)
        connection = http.client.HTTPSConnection("www.wftrader.com")
        url = self.URL.replace("__START__", str(start))
        url = url.replace("__LENGTH__", str(length))
        connection.request("GET", url)
        r1 = connection.getresponse()
        print(r1.status, r1.reason)
        data = r1.read()
        return data.decode("utf-8")

    def parseRequest(self,html):
        ITEM_REGX_NAME = 'wiki\\\/([^\\\"]+)'
        ITEM_REGX_STATS = '<\\\\\/a>","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)","([^"]*)"'
        ITEM_REGX_PRICE = ' for (\d+) :platinum:'
        startPos = 0
        #html = '{"draw":1,"recordsTotal":10614,"recordsFiltered":10510,"data":[["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Convectrix\" target=\"_blank\">Convectrix Hexacon<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w blinker878 Hey blinker878 I would like to buy your riven Convectrix Hexacon for 50 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=blinker878&dev=PC\">blinker878<\/a>","18.0","9.0","-7.0","0.0","Status Chance","Damage vs Grineer","Fire Rate \/ Attack Speed","","0","0","12","<img src=\".\/img\/p1.png\">&nbsp;Madurai","50","Today","28207"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Fang\" target=\"_blank\">Fang Utiata<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w Moosecraft Hey Moosecraft I would like to buy your riven Fang Utiata for 30 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=Moosecraft&dev=PC\">Moosecraft<\/a>","31.4","17.9","-3.4","0.0","Damage \/ Melee Damage","Channeling Efficiency","Damage vs Grineer","","0","0","14","<img src=\".\/img\/p3.png\">&nbsp;Naramon","30","Today","28206"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Fang\" target=\"_blank\">Fang Utiata<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w Moosecraft Hey Moosecraft I would like to buy your riven Fang Utiata for 30 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=Moosecraft&dev=PC\">Moosecraft<\/a>","31.4","17.9","-3.4","0.0","Damage \/ Melee Damage","Channeling Efficiency","Damage vs Grineer","","0","0","14","<img src=\".\/img\/p3.png\">&nbsp;Naramon","30","Today","28205"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Knell\" target=\"_blank\">Knell Croni-Critatis<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w blinker878 Hey blinker878 I would like to buy your riven Knell Croni-Critatis for 200 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=blinker878&dev=PC\">blinker878<\/a>","67.0","134.0","77.0","-34.0","Fire Rate \/ Attack Speed","Critical Chance","Critical Damage","Magazine Capacity","8","0","11","<img src=\".\/img\/p2.png\">&nbsp;Vazarin","200","Today","28204"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Gorgon\" target=\"_blank\">Gorgon Satilis<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w blinker878 Hey blinker878 I would like to buy your riven Gorgon Satilis for 100 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=blinker878&dev=PC\">blinker878<\/a>","7.0","11.0","0.0","0.0","Zoom","Multishot","","","0","0","15","<img src=\".\/img\/p3.png\">&nbsp;Naramon","100","Today","28203"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Dread\" target=\"_blank\">Dread Toxi-Critaata<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w Fawxco Hey Fawxco I would like to buy your riven Dread Toxi-Critaata for 650 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=Fawxco&dev=PC\">Fawxco<\/a>","122.5","117.7","76.0","-57.4","Damage \/ Melee Damage","Critical Chance","Toxic Damage","Status Chance","8","2","11","<img src=\".\/img\/p3.png\">&nbsp;Naramon","650","Today","28202"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Buzlok\" target=\"_blank\">Buzlok Insi-Gelidex<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w blinker878 Hey blinker878 I would like to buy your riven Buzlok Insi-Gelidex for 40 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=blinker878&dev=PC\">blinker878<\/a>","21.0","14.0","15.0","-7.0","Puncture Damage","Status Chance","Cold Damage","Zoom","0","0","15","<img src=\".\/img\/p2.png\">&nbsp;Vazarin","40","Today","28201"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Rubico\" target=\"_blank\">Rubico Sati-Ampitis<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w akdrag Hey akdrag I would like to buy your riven Rubico Sati-Ampitis for 500 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=akdrag&dev=PC\">akdrag<\/a>","40.1","79.9","95.1","0.0","Ammo Maximum","Multishot","Critical Damage","","8","4","12","<img src=\".\/img\/p1.png\">&nbsp;Madurai","500","Today","28200"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Viper\" target=\"_blank\">Viper Crita-Lexiata<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w HebbHebbaZatZat Hey HebbHebbaZatZat I would like to buy your riven Viper Crita-Lexiata for 25 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=HebbHebbaZatZat&dev=PC\">HebbHebbaZatZat<\/a>","26.1","33.2","0.4","-12.4","Critical Chance","Damage \/ Melee Damage","Punch Through","Critical Damage","0","0","8","<img src=\".\/img\/p1.png\">&nbsp;Madurai","25","Today","28199"],["<a href=\"http:\/\/warframe.wikia.com\/wiki\/Rubico\" target=\"_blank\">Rubico Sati-Puratis<\/a><br><button tooltip=\"Copy\" id=\"copy-button\" class=\"btn btn-xs btn-info\" data-clipboard-text=\"\/w akdrag Hey akdrag I would like to buy your riven Rubico Sati-Puratis for 350 :platinum:.\">Whisper In Game<\/button>","<a href=\"viewuser.php?usr=akdrag&dev=PC\">akdrag<\/a>","121.9","93.4","45.9","-43.6","Critical Damage","Multishot","Damage vs Infested","Reload Speed","8","2","9","<img src=\".\/img\/p1.png\">&nbsp;Madurai","350","Today","28198"]]}'
        patternName = re.findall(ITEM_REGX_NAME, html, re.DOTALL)
        patternStats = re.findall(ITEM_REGX_STATS, html, re.DOTALL)
        patternPrice = re.findall(ITEM_REGX_PRICE, html, re.DOTALL)
        #pattern = re.compile(ITEM_REGX)

        rivens = []
        for i in range(len(patternName)):
            print(patternName[i])
            stats = []
            weapon = self.stripEscapes(patternName[i])
            for j in range(len(patternStats[i])):
                stats.append(self.stripEscapes(patternStats[i][j]))
            price = patternPrice[i]
            riven = Riven(weapon, stats, price)
            rivens.append(riven)

        return rivens

    def stripEscapes(self, string):
        #translator = str.maketrans(dict.fromkeys('\\'))
        #string = string.translate(translator)
        string = string.replace('\\','')
        string = string.replace('/', '')
        if len(string) == 0:
            string = "none"
        return string