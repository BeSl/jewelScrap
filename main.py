# pip install requests2
# pip install beautifulsoup4
# pip install lxml
import requests
from bs4 import BeautifulSoup
import json
# cl js-cl-root m-mobile
URL = "https://sunlight.net/catalog/"
HEADERS= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
}

def get_datafile(mUrl, mHeaders, isOnline):
    r = requests.get(url = mUrl, headers = mHeaders)
    
    if isOnline:
        with open("index.html", "w", encoding='utf-8') as file:
            file.write(r.text)
    else:
        with open("index.html", encoding='utf-8') as file:
            file.read()

    return r.text

def get_IzdelsSmallInfo(textHtml, baseUrl):

    src = BeautifulSoup(textHtml, "lxml")
    items = src.find_all("div", class_="js-cl-item")

    linkIzdel = ""
    artIzdel = ""
    itemName = ""
 
    listIzdel = []    
    for item in items:
        linkIzdel = baseUrl + item.find("a", class_="js-cl-item-root-link").get("href")
       
        try:
            itemName = item.find("span", class_="cl-item-txt").text
        except Exception:
            itemName = "-"
        
        listIzdel.append(
            {
                "Url_cart": linkIzdel,
                "prevName": artIzdel,
                "itemName": itemName

            }
        )
    
    return listIzdel

def save_toJson(dataList, pathDataFile):
    with open(pathDataFile + ".json", "a", encoding="utf-8") as file:
        json.dump(dataList, file, indent=4, ensure_ascii= False)

def getNumPages(adressCatalog):
    r = requests.get(adressCatalog)
    soup = BeautifulSoup(r.text, 'lxml')
    rr = soup.findAll('div', class_='js-cl-item')  
    tagCountPages = "catalog-title__pagination"
    textPage = soup.find('div', class_=tagCountPages).get_text()
    cPage = int(textPage.replace("Страница 1 из", "", 1).strip())
    return cPage

def getAllPages(baseUrl):
    page_count = getNumPages(baseUrl+'/catalog/')
    for currentNumberPage in range(page_count):
        if currentNumberPage in(0,1):
            continue   
        listIzdelUrl = get_IzdelsSmallInfo(textHtml, baseUrl)
        save_toJson(listIzdelUrl, f"data/{currentNumberPage}_page")

def main():
    textHtml = get_datafile(mUrl=URL, mHeaders=HEADERS, isOnline=False)
    # print(items)
    baseUrl = "https://sunlight.net"
    print(f"Start scrap {baseUrl}")
    getAllPages(baseUrl)
    print(f"Stop scrap {baseUrl}")
# page-60/

if __name__ == "__main__":
    main()
