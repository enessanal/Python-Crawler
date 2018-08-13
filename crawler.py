import requests,re,socket, os.path
from bs4 import BeautifulSoup
from urlparse import urlparse

def getDomainName(url):
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result[(result.find("//")+2):].replace("/","").replace("www.","")

def getIPAddresses(url):
    IPList=socket.gethostbyname_ex(getDomainName(url))
    return IPList[2]

def getRootUrl(url):
    parsed_uri = urlparse(url)
    # print(parsed_uri)
    # print(os.path.split(urlparse(url).path))
    #
    # raw_input("Press enter...")
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result

def getLinks(url,tag,attr):
    links=[]
    source = BeautifulSoup(requests.get(url).content,"lxml")
    for item in source.find_all(tag):
        appendUrl=item.get(attr)
        if appendUrl != None and appendUrl!='#':
            appendUrl=appendUrl.strip()
            appendUrl=appendUrl.replace("\n","")
            appendUrl=appendUrl.replace(" ","")

            if re.match('((http|ftp)s?://.*?)', appendUrl):
                links.append(appendUrl)
            else:
                appendUrl=appendUrl.replace("../","")
                if(appendUrl[0]=="/"):
                    appendUrl=appendUrl[1:]

                if (appendUrl.find(";")==-1 and appendUrl.find(":")==-1 and appendUrl.find("{")==-1 and appendUrl!=""):
                    appendUrl=getRootUrl(url)+appendUrl
                    links.append(appendUrl)
    temp_list=[]
    for link in links:
        if(link[-1]=='/'):
            temp_list.append(link[0:len(link)-1])
        else:
            temp_list.append(link)

    links=list(set(temp_list))
    links.sort(key=getDomainName)
    return links

def printList(list):
    i=0
    for item in list:
        i+=1
        print str(i)+" "+item

def getInfo(url):
    domainName=getDomainName(url)
    rootUrl=getRootUrl(url)
    list_img=getLinks(url,'img','src')
    list_a=getLinks(url,'a','href')
    list_style=getLinks(url,'link','href')
    list_script=getLinks(url,'script','src')

    print("Url............: [ %s ] " %url)
    print("Domain.........: [ %s ] " %domainName)
    print("Root URL.......: [ %s ] " %rootUrl)
    print("Ip Addresses...:  %s  " %getIPAddresses(url))
    print("Hyper Links....: [ %d ]  " %len(list_a))
    print("Image Links....: [ %d ]  " %len(list_img))
    print("Style Links....: [ %d ]  " %len(list_style))
    print("Script Links...: [ %d ]  " %len(list_script))
    print

    printList(list_a)
    print
    printList(list_img)
    print
    printList(list_style)
    print
    printList(list_script)
    print


################################################################################

url='https://www.youtube.com'
getInfo(url)
