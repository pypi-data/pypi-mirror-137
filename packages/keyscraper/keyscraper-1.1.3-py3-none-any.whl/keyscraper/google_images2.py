from dynamicscraper import * 
import datetime, sys
from utils import *
linkList = []
folder = "./imageset7/"
def callback(link):
    global linkList
    if (link != None):
        linkList.append(link)
    return link
def clear_list():
    global linkList
    linkList = []
def main(page):
    retry = Retry()
    f_site = page
    f_page = ""
    f_item = DSFormat(
        xpath = "(//img[contains(@class, 'rg_i Q4LuWd')])", 
        click = True, multiple = True
    )
    f_attr = [
        DSFormat(
            xpath = "//div[contains(@class, 'tvh9oe BIB1wf')]//img[contains(@class, 'n3VNCb')]",
            extract = "src", nickname = "url", retry = retry.retry, callback = callback
        )    
    ]
    dsinfo = DSInfo(f_site = f_site, f_page = f_page, f_item = f_item, f_attr = f_attr)
    droptions = DriverOptions(mode = DriverOptions.MODE_CHROME, path = "./../../../../chromedriver.exe", window = True)
    dscraper = DynamicScraper(
        info = dsinfo, driveroptions = droptions, 
        mode = DynamicScraper.MODE_FILE,
        buttonPath = "//input[contains(@class, 'mye4qd')][last()]",
        itemWait = 1
    )
    dscraper.scrape(start = 1, pages = 1, perPage = 400)
"""
def download():
    global linkList
    length = len(linkList)
    for index, link in enumerate(linkList):
        sys.stdout.write(f"\r\tDownloading {index + 1} of {length}...")
        try:
            filename = TimeName().get_name(f"{folder}scraped_face_id={index}_", appendix = "")
            FileRetrieve(directlink = link, filename = filename, progress_bar = True, overwrite = False).advanced_retrieve(guess_image = True)
        except Exception as e:
            print(e)
        sys.stdout.flush()
"""
def download():
    global linkList
    length = len(linkList)
    for index, link in enumerate(linkList):
        filename = TimeName().get_name(f"{folder}scraped_face_id={index}_", appendix = "")
        sys.stdout.write(f"[{index + 1}] ")
        ImageGrabber(filename = filename, progressBar = True, url_timeout = 60).retrieve(directlink = link, timeout = 30)
check_folder(folder)
pageList = [
    "https://www.google.com/search?q=japanese%20models&tbm=isch&tbs=isz:l&hl=zh-TW&sa=X&ved=0CAIQpwVqFwoTCIDajcKF2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=korean%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCLC-_vGF2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=chinese%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCMiA8vuF2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=american%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCKCjq4eG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    #"https://www.google.com/search?q=russian%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCID85ZCG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    #"https://www.google.com/search?q=african%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCLDDpZyG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    #"https://www.google.com/search?q=canadian%20models&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCMjuz7KG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=teen%20actors&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCJjN3uqG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=teen%20actress&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCODXiPWG2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
    "https://www.google.com/search?q=middle%20aged%20actors&tbm=isch&hl=zh-TW&tbs=isz:l&sa=X&ved=0CAIQpwVqFwoTCNjthYuH2_QCFQAAAAAdAAAAABAC&biw=1389&bih=655",
]
for index, page in enumerate(pageList):
    print("On: ", index + 1)
    main(page)
    print("Found: ", len(linkList))
    download()
    #print(len(linkList))
    clear_list()
    #print(len(linkList))
    print("\n")





