#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2, re, socket
from urlparse import urlparse
import sys

# Parametre olarak verilen Url'e ait olan Domain Name'i geriye döndürür.
def getDomainName(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result[(result.find("//")+2):].replace("/","").replace("www.","")

# Parametre olarak verilen Url'in ait olduğu Domain'in IP adreslerini geriye döndürür.
def getIPAddresses(url):
    IPList=socket.gethostbyname_ex(getDomainName(url))
    return IPList[2]

# Parametre olarak verilen Url'deki linkleri geriye döndüren fonksiyon.
def getLinksFromUrl(url):
    # Sayfa kaynak kodu değişkene aktarılıyor.
    website = urllib2.urlopen(url)
    html = website.read()
    links = []
    # Linkler değişkene atılıyor.
    for link in re.findall('"((http|ftp)s?://.*?)"', html):
        links.append(link[0])
    # Tekrar eden linkler kaldırılıyor.
    links=list(set(links))
    return links

# Performans değerlendirme kriteri
def getInfo(url):
    domain=getDomainName(url)
    links=getLinksFromUrl(url)
    recursiveUrls=[]
    externalUrls=[]
    for link in links:
        if domain==getDomainName(link):
            recursiveUrls.append(link)
        else:
            externalUrls.append(link)

    print("Url............: [ %s ] " %url)
    print("Domain.........: [ %s ] " %domain)
    print("Found Links....: [ %d ] " %len(links))
    print("Recursives.....: [ %d ] " %len(recursiveUrls))
    print("Externals......: [ %d ] " %len(externalUrls))
    print("Ip Addresses...: [ %s ] " %getIPAddresses(url))
    print("\n")
    return links

try:
    program_name = sys.argv[0]
    arguments = sys.argv[1:]
    count = len(arguments)
    url = arguments[0]

    for url in arguments:
        getInfo(url)


    file = open("testfile.txt", "r")
    urls = file.readlines()

    for url in urls:
        print(url)

    file.close()

except Exception as e:
    print(str(e))
