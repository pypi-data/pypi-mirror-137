from dynamicscraper import * 
import datetime, sys
from utils import *
linkList = []
folder = "./imageset4/"
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
        mode = DynamicScraper.MODE_READ,
        buttonPath = "//input[contains(@class, 'mye4qd')][last()]",
        clickWait = 0.3
    )
    dscraper.scrape(start = 1, pages = 1, perPage = 600)
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
        ImageGrabber(filename = filename, progressBar = True).retrieve(directlink = link, timeout = 30)
check_folder(folder)
pageList = [
    #"https://www.google.com/search?q=high+school+students&tbm=isch&sxsrf=AOaemvJ4hWdkwVJP2hRErugAhRVTVlmbcg%3A1638975384376&source=hp&biw=1536&bih=739&ei=mMewYfu3FIm2mAXZkoSQBg&iflsig=ALs-wAMAAAAAYbDVqLqoHjdRzbUktdH1sczLs04TavjH&ved=0ahUKEwj749CMu9T0AhUJG6YKHVkJAWIQ4dUDCAU&uact=5&oq=high+school+students&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CggjEO8DEOoCECc6BwgjEO8DECc6CwgAEIAEELEDEIMBOggIABCABBCxAzoICAAQsQMQgwE6BAgAEANQ7gVYn1JglFNoCXAAeACAAUOIAbYLkgECMjiYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCg&sclient=img",
    #"https://www.google.com/search?q=college+students&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj3z_nN5NP0AhVNzmEKHb19CJcQ_AUoAXoECAIQAw",
    #"https://www.google.com/search?q=middle+school+students&tbm=isch&ved=2ahUKEwit8YTywNT0AhUTAt4KHQyoBbsQ2-cCegQIABAA&oq=middle+school+students&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46BwgjEO8DECc6BAgAEBM6CAgAEAUQHhATOggIABCABBCxAzoICAAQsQMQgwE6BggAEAoQGFCbE1jdMmDFM2gBcAB4AIABVIgB3QuSAQIyNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=q82wYe3vCpOE-AaM0JbYCw&bih=352&biw=1519&hl=zh-TW",    
    #"https://www.google.com/search?q=indian+people&tbm=isch&ved=2ahUKEwiep8OS9Nj0AhXQUvUHHYiYBR8Q2-cCegQIABAA&oq=indian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOggIABCABBCxA1CuQliBUGCGUmgAcAB4AIABmAOIAYQNkgEJOS4zLjEuMC4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=SByzYZ7jHNCl1e8PiLGW-AE&bih=595&biw=1280",
    #"https://www.google.com/search?q=japanese+people&tbm=isch&ved=2ahUKEwj6gND49tj0AhVDEHAKHTcKARMQ2-cCegQIABAA&oq=japanese+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOggIABCABBCxAzoECAAQA1D3E1i6H2C2IGgAcAB4AYABjwGIAaQKkgEEMTMuM5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=Nx-zYbqJHMOgwAO3lISYAQ&bih=595&biw=1280",
    #"https://www.google.com/search?q=chinese+people&tbm=isch&ved=2ahUKEwje6vqE99j0AhWuS_UHHfHADHEQ2-cCegQIABAA&oq=chinese+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CwgAEIAEELEDEIMBOggIABCABBCxAzoICAAQsQMQgwE6BAgAEBNQsA5YvC1grC5oB3AAeAGAAbsBiAHaDpIBBDE4LjSYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=UR-zYZ7-E66X1e8P8YGziAc&bih=595&biw=1280",
    #"https://www.google.com/search?q=side+profile+&tbm=isch&ved=2ahUKEwjUjOWW99j0AhUTAt4KHSlRDtoQ2-cCegQIABAA&oq=side+profile+&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDOgsIABCABBCxAxCDAVC0FVi7HmDeIWgAcAB4AIABhgGIAfYIkgEEMTIuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=dh-zYdT5K5OE-AapornQDQ&bih=595&biw=1280",
    #"https://www.google.com/search?q=looking+downward&tbm=isch&ved=2ahUKEwjN35uu99j0AhWLAN4KHal7Ax4Q2-cCegQIABAA&oq=looking+downward&gs_lcp=CgNpbWcQAzIECAAQEzIECAAQEzIECAAQEzIICAAQBRAeEBMyCAgAEAUQHhATMggIABAFEB4QEzIICAAQBRAeEBMyCAgAEAUQHhATMggIABAFEB4QEzIICAAQBRAeEBM6BQgAEIAEOgQIABAeUOEYWMgbYK0caABwAHgAgAFpiAGOA5IBAzQuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=px-zYY3wM4uB-Aap943wAQ&bih=595&biw=1280",
    #"https://www.google.com/search?q=looking+upward&tbm=isch&ved=2ahUKEwiS3ouz99j0AhVIet4KHQk_CgYQ2-cCegQIABAA&oq=looking+upward&gs_lcp=CgNpbWcQAzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzoICAAQBRAeEBM6CAgAEIAEELEDOgUIABCABDoECAAQHlCiBVjPG2CsHGgAcAB4AIABwAGIAaIKkgEEMTEuNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=sh-zYZK9BMj0-QaJ_qgw&bih=595&biw=1280",
    #"https://www.google.com/search?q=todler+faces&tbm=isch&ved=2ahUKEwjvkMzN99j0AhXqQ_UHHYNxAPoQ2-cCegQIABAA&oq=todler+faces&gs_lcp=CgNpbWcQAzIECAAQEzoICAAQgAQQsQM6BQgAEIAEOggIABAIEB4QE1DgC1ikWGCUWWgNcAB4AIABmAGIAboLkgEEMTMuNJgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=6R-zYa_4J-qH1e8Pg-OB0A8&bih=595&biw=1280",
    #"https://www.google.com/search?q=old+faces&tbm=isch&ved=2ahUKEwjh8cTV99j0AhVATPUHHcsmBdMQ2-cCegQIABAA&oq=old+faces&gs_lcp=CgNpbWcQAzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIICAAQBRAeEBMyCAgAEAUQHhATMggIABAFEB4QEzoICAAQgAQQsQM6BQgAEIAEOgQIABAeUKObAVjWpAFg46UBaABwAHgBgAGgBYgB_gqSAQc1LjMuNS0xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=-h-zYeGME8CY1e8Py82UmA0&bih=595&biw=1280",
    #"https://www.google.com/search?q=indigenous+people+&tbm=isch&ved=2ahUKEwj-goTk99j0AhXXQfUHHcBVCvkQ2-cCegQIABAA&oq=indigenous+people+&gs_lcp=CgNpbWcQAzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzoICAAQBRAeEBM6CAgAEIAEELEDOgUIABCABDoECAAQHjoICAAQCBAeEBNQvwRYwixgnC5oBHAAeAGAAbIDiAGYGZIBCjkuMTIuMy4wLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=GCCzYf6WK9eD1e8PwKupyA8&bih=595&biw=1280",
    #"https://www.google.com/search?q=tribal+people&tbm=isch&ved=2ahUKEwj89Z3799j0AhWGAt4KHXiNBGYQ2-cCegQIABAA&oq=tribal+people&gs_lcp=CgNpbWcQAzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzIECAAQEzoFCAAQgAQ6CAgAEIAEELEDUMoMWIsZYPgZaABwAHgAgAGJA4gBlw6SAQcwLjMuMi4ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=SSCzYbytFoaF-Ab4mpKwBg&bih=595&biw=1280",
    #"https://www.google.com/search?q=movie+stars&tbm=isch&ved=2ahUKEwjauKz_99j0AhUYAYgKHYhRAR8Q2-cCegQIABAA&oq=movie+stars&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOgQIABATOggIABCABBCxAzoICAAQsQMQgwE6CwgAEIAEELEDEIMBUJUFWJniAWDI4wFoBHAAeAOAAewEiAGcIZIBCzUuNy41LjIuMC4ymAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=USCzYZrMPJiCoASIo4X4AQ&bih=595&biw=1280",
    "https://www.google.com/search?q=models&tbm=isch&ved=2ahUKEwik4__E-Nj0AhUQDJQKHStnAxUQ2-cCegQIABAA&oq=models&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDOggIABCxAxCDAToLCAAQgAQQsQMQgwFQ1gdYsA1g0A5oAHAAeACAAWKIAZgEkgEBN5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=5CCzYaThA5CY0ASrzo2oAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=doctors&tbm=isch&ved=2ahUKEwjUzJzg-Nj0AhUKBaYKHQWXBDcQ2-cCegQIABAA&oq=doctors&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgAEB46CAgAEIAEELEDUNQhWJsoYPooaABwAHgAgAFNiAH4A5IBATiYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=HSGzYZTKCYqKmAWFrpK4Aw&bih=595&biw=1280",
    "https://www.google.com/search?q=mexican+people&tbm=isch&ved=2ahUKEwjV_r7k-Nj0AhUjEqYKHVPmCj8Q2-cCegQIABAA&oq=mexican+people&gs_lcp=CgNpbWcQAzoFCAAQgAQ6CAgAEIAEELEDOggIABCxAxCDAToECAAQHlCqB1iXf2CkgwFoA3AAeAKAAccEiAHLGZIBCzUuMS4yLjQuMS4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=JiGzYdXTBqOkmAXTzKv4Aw&bih=595&biw=1280",
    "https://www.google.com/search?q=korean+people&tbm=isch&ved=2ahUKEwi--N6U-dj0AhUJ7JQKHYUNBR4Q2-cCegQIABAA&oq=korean+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOggIABCABBCxA1AAWKIrYNIsaABwAHgBgAGLAYgB4AiSAQQxMC4zmAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=iyGzYf6GEonY0wSFm5TwAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=taiwanese+people&tbm=isch&ved=2ahUKEwjUzseZ-dj0AhUM35QKHbzYCzMQ2-cCegQIABAA&oq=taiwanese+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46CAgAEIAEELEDUOcEWOkQYIkSaABwAHgBgAGiA4gB3xSSAQk1LjcuMi4xLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=lSGzYZSwGIy-0wS8sa-YAw&bih=595&biw=1280",
    "https://www.google.com/search?q=english+people&tbm=isch&ved=2ahUKEwj_tPGk-dj0AhUJ6ZQKHaBBARUQ2-cCegQIABAA&oq=english+people&gs_lcp=CgNpbWcQAzoFCAAQgAQ6BAgAEB46BggAEAUQHlDGBVirSmD4S2gAcAB4AIABcYgBcZIBAzAuMZgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=rSGzYb-qCYnS0wSgg4WoAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=german+people&tbm=isch&ved=2ahUKEwjA-oGw-dj0AhUOe5QKHf-LDQ0Q2-cCegQIABAA&oq=german+people&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgAEB5QzSpY2Dlg6DloAHAAeACAAesEiAH4CZIBBzMtMi4wLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=xCGzYcCIHo720QT_l7Zo&bih=595&biw=1280",
    "https://www.google.com/search?q=italian+people&tbm=isch&ved=2ahUKEwjcnKa7-dj0AhUD9pQKHQBrCooQ2-cCegQIABAA&oq=italian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDUNUFWKkQYJwRaABwAHgBgAGVAogBkQuSAQU5LjIuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=3CGzYdy-CYPs0wSA1qnQCA&bih=595&biw=1280",
    "https://www.google.com/search?q=spanish+people&tbm=isch&ved=2ahUKEwi0v4zB-dj0AhUB15QKHaX6DbwQ2-cCegQIABAA&oq=spanish+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDUJYEWM4PYLcQaABwAHgAgAHhAogB2wySAQc4LjEuMS4ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=6CGzYbSrE4Gu0wSl9bfgCw&bih=595&biw=1280",
    "https://www.google.com/search?q=russian+people&tbm=isch&ved=2ahUKEwiR-tHH-dj0AhWkw4sBHQHGAH8Q2-cCegQIABAA&oq=russian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDULsEWN8QYMIRaABwAHgAgAGqAYgB-QmSAQQxMi4zmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=9iGzYZGnAqSHr7wPgYyD-Ac&bih=595&biw=1280",
    "https://www.google.com/search?q=arabian+people&tbm=isch&ved=2ahUKEwjZ6e3N-dj0AhWXAaYKHbrpDuYQ2-cCegQIABAA&oq=arabian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDUKWPAVjvmwFgwpwBaABwAHgAgAGUAogBqA-SAQU0LjcuM5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=AyKzYZncBJeDmAW607uwDg&bih=595&biw=1280",
    "https://www.google.com/search?q=indonesian+people&tbm=isch&ved=2ahUKEwiC36bl-dj0AhVQCaYKHZhxD4oQ2-cCegQIABAA&oq=indonesian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB5QygNYhghg7QhoAHAAeACAAf8CiAHSB5IBBzYuMS4wLjGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=NCKzYYL1DtCSmAWY473QCA&bih=595&biw=1280",
    "https://www.google.com/search?q=congo+people&tbm=isch&ved=2ahUKEwiymfXm-dj0AhUFUJQKHdicAR4Q2-cCegQIABAA&oq=congo+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CwgAEIAEELEDEIMBOggIABCABBCxAzoICAAQsQMQgwE6BAgAEANQ9gZY-3JgrnRoAHAAeAGAAaMDiAGmDpIBCTEuMy4xLjIuMZgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=NyKzYfKhJoWg0QTYuYbwAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=egyptian+people&tbm=isch&ved=2ahUKEwi2qLaY-tj0AhUBHKYKHT27BRYQ2-cCegQIABAA&oq=egyptian+people&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDOgsIABCABBCxAxCDAVCnB1j2RGDiRWgBcAB4A4ABzQKIAcATkgEHOC41LjQuMZgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=nyKzYfbcG4G4mAW99pawAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=professors&tbm=isch&ved=2ahUKEwj5xruv-tj0AhXnGKYKHZ3bDTQQ2-cCegQIABAA&oq=professors&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDOggIABCxAxCDAVCnBljUEmDuE2gAcAB4AoABzQKIAbALkgEHNS41LjAuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=zyKzYbmjL-exmAWdt7egAw&bih=595&biw=1280",
    "https://www.google.com/search?q=famous+people+&tbm=isch&ved=2ahUKEwiyi7Wx-tj0AhX1JqYKHYtrBIYQ2-cCegQIABAA&oq=famous+people+&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDOgQIABADOgQIABATUN4DWLgYYJ4baAJwAHgAgAHCAYgBrguSAQM4LjaYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=0yKzYfLVNPXNmAWL15GwCA&bih=595&biw=1280",
    "https://www.google.com/search?q=teenagers&tbm=isch&ved=2ahUKEwi-ubW4-tj0AhUzJaYKHTj1BxIQ2-cCegQIABAA&oq=teenagers&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOggIABCABBCxAzoLCAAQgAQQsQMQgwFQAFjpPGDhPmgAcAB4AoAB9wSIAccWkgELNS4zLjIuMS4wLjKYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABAMABAQ&sclient=img&ei=4iKzYb7AIbPKmAW46p-QAQ&bih=595&biw=1280",
    "https://www.google.com/search?q=students+in+classrooms&tbm=isch&ved=2ahUKEwjlhc_I-tj0AhUyy4sBHQHkCDwQ2-cCegQIABAA&oq=students+in+classrooms&gs_lcp=CgNpbWcQAzIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46CAgAEIAEELEDUI1MWOxeYNBfaABwAHgAgAHhA4gB_hqSAQkzLjUuNS4xLjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=BCOzYeXzH7KWr7wPgcij4AM&bih=595&biw=1280",
    "https://www.google.com/search?q=people+looking+aside&tbm=isch&ved=2ahUKEwjY3IHj-tj0AhVn0IsBHf4lCh4Q2-cCegQIABAA&oq=people+looking+aside&gs_lcp=CgNpbWcQAzoECAAQEzoICAAQCBAeEBM6BQgAEIAEOgQIABAeOgYIABAIEB5Q6A1Y_htg0BxoAHAAeACAAZQBiAHCBZIBAzkuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=OyOzYZjTNeegr7wP_suo8AE&bih=595&biw=1280"    
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





