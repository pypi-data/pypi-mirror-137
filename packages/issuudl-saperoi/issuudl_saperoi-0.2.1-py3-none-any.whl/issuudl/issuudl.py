import os
import requests
import xml.etree.ElementTree as ET

def getSWF(page: int, id: str, folder: str ="./"):
    response = requests.get("http://page.isu.pub/" + id + "/swf/page_" + str(page) + ".swf")
    file = open(folder + str(page) + ".swf", "wb")
    file.write(response.content)
    file.close()
    print('Downloaded ' + str(page) + '.swf')

def getJPG(page: int, id: str, folder: str ="./"):
    response = requests.get("http://image.isu.pub/" + id + "/jpg/page_" + str(page) + ".jpg")
    file = open(folder + str(page) + ".jpg", "wb")
    file.write(response.content)
    file.close()
    print('Downloaded ' + str(page) + '.jpg')

def getId(url: str):
    url = "https://issuu.com/oembed?url=" + url + "&format=xml"
    r = requests.get(url)
    doc = open('page.xml', 'wb')
    doc.write(r.content)
    doc.close()
    ximmy = open('page.xml')
    tree = ET.parse(ximmy)
    ximmy.close()
    os.remove('page.xml')
    root = tree.getroot()
    imgu = root.find("./thumbnail_url")
    id = imgu.text
    id = id.split("/")
    return id[3]

def download(url: str, end: int, ext: str, folder: str ="./", start: int = 1):
    id = getId(url)
    for page in range(start, end + 1):
        if ext == "jpg" or "both":
            getJPG(page, id, folder)
        if ext == "swf" or "both":
            getSWF(page, id, folder)
        else:
            print("Please choose between \"jpg\", \"swf\" or \"both\"")

def downloadPage(url: str, page: int, ext: str, folder: str ="./"):
    id = getId(url)
    if ext == "jpg" or "both":
        getJPG(page, id, folder)
    if ext == "swf" or "both":
        getSWF(page, id, folder)
    else:
        print("Please choose between \"jpg\", \"swf\" or \"both\"")

def downloadWithId(id: str, end: int, ext: str, folder: str ="./", start: int = 1):
    for page in range(start, end + 1):
        if ext == "jpg" or "both":
            getJPG(page, id, folder)
        if ext == "swf" or "both":
            getSWF(page, id, folder)
        else:
            print("Please choose between \"jpg\", \"swf\" or \"both\"")

def downloadPageWithId(id: str, page: int, ext: str, folder: str ="./"):
    if ext == "jpg" or "both":
        getJPG(page, id, folder)
    if ext == "swf" or "both":
        getSWF(page, id, folder)
    else:
        print("Please choose between \"jpg\", \"swf\" or \"both\"")