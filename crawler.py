#! /usr/bin/env python3.6
import argparse,re,socket,requests,threading
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from random import randint
import urllib.parse

class SITE:
    list_a_same=[]
    list_a_different=[]
    domainName=""
    url=""
    IPList=[]
    # Http Başlıklarındaki bazı alanlar eklenmez ise hatalar alınabiliyor.
    headers = { 'User-Agent': 'Sakarya University - CrawlerPy 1.0.0 - Enes Sanal - For Researching And Development', 'From':'enessanal@hotmail.com.tr'}

################################################################################

# Dizideki tekrar eden elemanları kaldırır.
def removeDuplicates(array):
    return list(set(array))
# End of removeDuplicates

# Crawl işlemini threadlere ayırmaya yarayan sınıf.
class Thread(threading.Thread):
    def __init__(self,urlList):
        threading.Thread.__init__(self)
        self.urlList=urlList

    def run(self):
        for url in self.urlList:
            if(url.find(".ico")==-1 and
            url.find(".gif")==-1 and
            url.find(".jpg")==-1 and
            url.find(".png")==-1 and
            url.find(".pdf")==-1 and
            url.find(".jpeg")==-1 and
            url.find(".doc")==-1 and
            url.find(".docx")==-1 and
            url.find(".xls")==-1 and
            url.find(".xlsx")==-1 and
            url.find(".xlsm")==-1 and
            url.find(".pptx")==-1):
                crawlUrl(url)
# End of Thread Class

# Verilen bir diziyi aldığı parametreye göre parçalara bölen ve geriye döndüren metot.
def splitArray(array,slices):
    arrayList=[]
    rest=[]
    if(slices>len(array)):
        return splitArray(array,len(array))
    for i in range(slices):
        first=(i)*(len(array)//slices)
        last=(i+1)*(len(array)//slices)
        if(i+1 == slices):
            rest=array[last:len(array)]
        arrayList.append(array[first:last])
    while len(rest)>0:
        arrayList[randint(0,len(arrayList)-1)].append(rest.pop())
    return arrayList
# End of splitArray

# Linkleri global diziye ekler.
def appendLinks(url,urlList):
        for item in urlList:
            joinedUrl=urljoin(url,item.get("href").replace(" ","").replace("\n","").replace("\r",""))

            if(getDomainName(joinedUrl) == SITE.domainName):
                SITE.list_a_same.append(joinedUrl)
            else:
                SITE.list_a_different.append(joinedUrl)
# End of appendLinks

# Color Print: Renkli yazı yazmayı sağlayan metot.
def cprint(msg,color="black"):
    colors={
    "gray":"30",
    "red":"31",
    "green":"32",
    "yellow":"33",
    "blue":"34",
    "magenta":"35",
    "cyan":"36",
    "black":"37",
    }
    m=1

    if colors.get(color) is None:
        color="black"

    if color=="black":m=0
    print("\033[1;{};{}m".format(colors[color],m),end="")
    print(msg)
    print("\033[1;37;0m",end="")
# End of cprint

# Verbose seviyesine göre çıktı devreye girer.
def verbose_print(msg):
    if args.verbose:
        cprint("--> "+msg,"gray")
# End of verbose_print

# Hata mesajlarını ayrı bir formatta yazdırmayı sağlayan metot.
def error_print(msg):
    cprint("--> "+msg,"red")
# End of error_print

# İlgili Url'in Domain Name'ini Geriye Döndürür.
def getDomainName(url):
    UrlParseObject = urlparse(url)
    return UrlParseObject.netloc.replace("/","").replace(" ","").replace("\n","").replace("\r","").replace("www.","")
# End of getDomainName

# Url doğrulaması yapan metot.
def verifyUrl(url):
    try:
        response=requests.get(url,timeout=3,headers=SITE.headers)
        if response.status_code==404:
            return False
        else:
            # return True
            return response

    except requests.exceptions.Timeout as e:
        return False

    except requests.exceptions.RequestException as e:
        return False

    except Exception as e:
        return False
# End of verifyUrl

# Parametre olarak alınan Url içerisindeki linkleri getiren metot.
def getLinks(response,url):
    list_a=[]
    source=BeautifulSoup(response.content,'lxml')

    # for lnk in re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",str(source)):
    for lnk in re.findall('"((http|ftp)s?://.*?)"',str(source)):
        if(lnk[0][len(lnk[0])-1]!="."):
            new_tag =source.new_tag('a',href=lnk[0])
            list_a.append(new_tag)


    for item in source.find_all('a'):
        appendUrl=item.get("href")
        if(appendUrl!=None and appendUrl!="#" and
        appendUrl.find("javascript:")==-1 and
        appendUrl.find("javascript:void(0)")==-1 and
        appendUrl.find("mailto:")==-1 and
        appendUrl.find("tel:")==-1):
            list_a.append(item)
    return list(set(list_a))
# End of getLinks

def crawlUrl(url):
    # Url içinde (varsa) gereksiz karakterler kaldırılır.
    crawl_url=url.replace(" ","").replace("\n","").replace("\r","")
    # scheme://netloc/path;parameters?query#fragment
    UrlParseObject = urlparse(crawl_url)
    if(UrlParseObject.scheme==""):
        crawl_url="http://"+crawl_url
        UrlParseObject = urlparse(crawl_url)
    response = verifyUrl(crawl_url)
    if response:
        appendLinks(crawl_url,getLinks(response,crawl_url))

################################################################################

# Help mesajını manipüle edebilmek için add_help=False seçeneğini ekledik.
parser=argparse.ArgumentParser(description='CrawlerPy - Target Spesific Crawler',add_help=False)
parser.add_argument("url",help="Url adresi")
parser.add_argument("-d","--depth",help="Crawl İşleminin Derinliği (Varsayılan=0)",type=int,default=0)
parser.add_argument('-v',"--verbose", help="Ayrıntılı çıktı modu.", action="store_true")
parser.add_argument('--version', action='version',version='%(prog)s 1.0', help="Programın versiyonunu yazdır ve çık.")
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,help='Yardım mesajını göster ve çık.')
parser.add_argument('-t', '--threads',help='Programın Çalışırken Kullanacağı Thread Sayısı (Varsayılan=50)',type=int,default=50)
args=parser.parse_args()

# Url içinde (varsa) gereksiz karakterler kaldırılır.
SITE.url=args.url.replace(" ","").replace("\n","").replace("\r","").lower()

# scheme://netloc/path;parameters?query#fragment
UrlParseObject = urlparse(SITE.url)
if(UrlParseObject.scheme==""):
    SITE.url="http://"+SITE.url
    UrlParseObject = urlparse(SITE.url)

verbose_print("Ayrıntılı çıktı modu aktif.")
verbose_print("Program Başlatılıyor...")

response=""

# Verilen URL'e ait olan alan adını doğrular ve hata yoksa devam eder, hata varsa programdan çıkar.
try:
    verbose_print("[ {} ] Alan adı doğrulanıyor...".format(UrlParseObject.netloc))
    for ip in socket.gethostbyname_ex(UrlParseObject.netloc)[2]: SITE.IPList.append(ip)
    verbose_print("Alan adı bulundu [ {} ]".format(UrlParseObject.netloc))
    SITE.domainName=UrlParseObject.netloc.replace("/","").replace(" ","").replace("\n","").replace("\r","")
except socket.gaierror as e:
    error_print("Geçersiz Alan Adı X [{}] X".format(UrlParseObject.netloc))
    verbose_print("Programdan çıkılıyor.")
    exit()
except Exception as e:
    error_print("Bilinmeyen Hata")
    verbose_print("Programdan çıkılıyor.")
    exit()
# End of Alan adı doğrulama

# Verilen Url in var olup olmadığını kontrol eder. Eğer hata varsa programı sonlandırır, yoksa devam eder.
try:
    verbose_print("[ {} ] Url adresi doğrulanıyor...".format(SITE.url))

    response=requests.get(SITE.url,timeout=3,headers=SITE.headers)
    if response.status_code==404:
        error_print("Geçersiz Url Adresi (404) X [{}] X".format(SITE.url))
        exit()
    else:
        verbose_print("Url adresi bulundu [ {} ]".format(SITE.url))
except requests.exceptions.Timeout as e:
    error_print("Bağlantı sorunu X [{}] X".format(SITE.url))
    verbose_print("Programdan çıkılıyor.")
    exit()
except requests.exceptions.RequestException as e:
    cprint(e,"cyan")
    error_print("Geçersiz Url X [{}] X".format(SITE.url))
    verbose_print("Programdan çıkılıyor.")
    exit()
except Exception as e:
    error_print("Bilinmeyen Hata")
    print(e)
    verbose_print("Programdan çıkılıyor.")
    exit()
# End of Url doğrulama
appendLinks(SITE.url,getLinks(response,SITE.url))

arrayList=splitArray(SITE.list_a_same,args.threads)

SITE.list_a_same=removeDuplicates(SITE.list_a_same)
SITE.list_a_different=removeDuplicates(SITE.list_a_different)

for j in range(0,args.depth):

    arrayList=splitArray(SITE.list_a_same,args.threads)
    threads=[]
    for array in arrayList:
        thread=Thread(array)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    SITE.list_a_same=removeDuplicates(SITE.list_a_same)
    SITE.list_a_different=removeDuplicates(SITE.list_a_different)

# Elde edilen bilgilerin ekrana basılması
print("Link Sayısı....: [ %d ] " %(len(SITE.list_a_same)+len(SITE.list_a_different)))
print("Url............: [ %s ] " %SITE.url)
print("Domain.........: [ %s ] " %SITE.domainName)

if len(SITE.IPList) > 1:
    print("IP Adresleri...: %s  " %SITE.IPList)
else:
    print("IP Adresi......: %s  " %SITE.IPList)

if len(SITE.list_a_same) > 0 or len(SITE.list_a_different) > 0 :
    print("\nLinkler:")


    SITE.list_a_different.sort(key=len)
    SITE.list_a_same.sort(key=len)

    i=0

    for link in SITE.list_a_different:
        i+=1
        print("{} -) {}".format(i,link))

    for link in SITE.list_a_same:
        i+=1
        print("{} -) {}".format(i,link))
# End of ekrana basma








#
