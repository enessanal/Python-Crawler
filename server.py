#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib2, re, socket
from urlparse import urlparse
import sys
import argparse


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
    try:
        url=url.replace("\n","")
        domain=getDomainName(url)
        print("Url............: [ %s ] " %url)
        print("Domain.........: [ %s ] " %domain)
        print("Ip Addresses...: [ %s ] " %getIPAddresses(url))
        links=getLinksFromUrl(url)
        print("Found Links....: [ %d ] " %len(links))
        recursiveUrls=[]
        externalUrls=[]
        for link in links:
            if domain==getDomainName(link):
                recursiveUrls.append(link)
            else:
                externalUrls.append(link)

        print("Recursives.....: [ %d ] " %len(recursiveUrls))
        print("Externals......: [ %d ] " %len(externalUrls))
        print("\n")
        i=0
        for link in recursiveUrls:
            i=i+1
            print(str(i)+"-) "+link)

        for link in externalUrls:
            i=i+1
            print(str(i)+"-) "+link)


    except Exception as e:
        print("\033[1;31;1m")
        print("!"+type(e).__name__+" => "+url)
        print("\033[1;37;0m")
        print("\n")


parser = argparse.ArgumentParser()
parser.add_argument("--urls", "-u",action='append',help = "Url Adresleri; Her adres için -u gerekir.")
parser.add_argument("--file","-f",help = "Url Adreslerinin Bulunduğu Dosya Yolu")
# Gelen argümanları ayırıyoruz ve bir değişkene aktarıyoruz
arguments = parser.parse_args()

# İki parametre aynı anda girilirse uyarı verilir.
if(arguments.urls and arguments.file):
    print("Aynı anda dosya ve komut satırından parametre girilemez.")
    print("Tek parametre kullanınız.")


elif(arguments.urls):

    for url in arguments.urls:
        getInfo(url)

elif(arguments.file):
    path=arguments.file;

    try:
        file = open("urls.txt", "r")
        urls = file.readlines()
        file.close()

        for url in urls:
            getInfo(url)
            print("\n\n")

    except Exception as e:
        print("\033[1;31;1m")
        print("!"+type(e).__name__)
        print("\033[1;37;0m")
else:
    print("Parametre Giriniz")
