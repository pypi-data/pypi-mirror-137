from keyscraper.utils import TimeName, datetime, pandas, copy, time, sys, os
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium import webdriver

"""
    Copyright (c) 2021 keyywind
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

class DSBase:
    
    def help():
        
        print("DSBase: # This class is not meant to be used by user ")
        print("\t[1] __init__(self, className)")
        print("\t[2] check_types(self, item, exp_types)")
        print("\t[3] raise_exception(self, message)\n")
    
    def __init__(self, className):
        
        self.className = className
        
    def check_types(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"ERROR B: [ {self.className} ]")
        
    def raise_exception(self, message):
        
        raise Exception(message)
    
        
class DSFormat:
    
    class __Dictionary:
        
        class __Item:
            
            def __init__(self, typeList, defValue):
                
                self.dataList = {
                    "value" : [ defValue ],
                    "types" : copy.deepcopy(typeList)
                }
                
            def get_value(self): return self.dataList["value"][0]
            
            def get_types(self): return self.dataList["types"]
            
            def mod_value(self, newVal):
                
                if ((any in self.dataList["types"]) or (type(newVal) in self.dataList["types"])):
                    
                    self.dataList["value"][0] = newVal
                    
                    return True
                
                print("ERROR 1")
                
                return False
            
        def __init__(self, xpath, ** kwargs):
            
            self.dictionary = {
                "xpath" : self.__Item([str], xpath),
                "relative" : self.__Item([bool], False),
                "multiple" : self.__Item([bool], False),
                "extract" : self.__Item([any], None),
                "format" : self.__Item([any], None),
                "filter" : self.__Item([any], None),
                "retry" : self.__Item([any], None),
                "callback" : self.__Item([any], None),
                "nickname" : self.__Item([str], None),
                "keep" : self.__Item([bool], True),
                "click" : self.__Item([bool], False)
            }
            
            for key, value in kwargs.items():
                
                if (key in self.dictionary):
                    
                    self.dictionary[key].mod_value(value)
                    
                    continue
                    
                print("ERROR 2")
                
        def __getitem__(self, key):
            
            if (key in self.dictionary):
                
                return self.dictionary[key].get_value()
            
            print("ERROR 3")
    
    def __init__(self, xpath, ** kwargs):
        
        self.dataList = self.__Dictionary(xpath, ** kwargs)
        
    def __getitem__(self, key):
        
        return self.dataList[key]
    
    def help():
        
        print("DSFormat: ")
        print("\t[1] __init__(self, xpath, relative = False, multiple = False, extract = None,\n\t\tformat = None, filter = None, retry = None, callback = None,\n\t\t\tnickname = None, keep = True, click = False)")
        print("\t[2] __getitem__(self, key)\n")
    
        
class DSInfo(DSBase):
    
    def help():
        
        print("DSInfo: ")
        print("\t[1] __init__(self, f_site, f_page, f_item, f_attr)")
        print("\t[2] format_page(self, page) # page is preferrably an integer\n")
    
    def __init__(self, f_site, f_page, f_item, f_attr):
        super(DSInfo, self).__init__(className = "DSBase")
        
        self.elements = {
            "f_site" : self.check_types(f_site, [str]), 
            "f_page" : self.check_types(f_page, [str]),
            "f_item" : self.check_types(f_item, [DSFormat]),
            "f_attr" : self.check_types(f_attr, [list])
        }
        
        self.formattable, self.pageformat = \
            self.__check_formattable(self.elements["f_site"], self.elements["f_page"])
        
    def __check_formattable(self, f_site, f_page):
        
        if (f_page == ""): return False, f_site
            
        A, B = (f_site[-1] == "/"), (f_page[0] == "/")
        
        return True, (
            (f_site[:-1] + f_page) if (A and B) else \
                (f_site + f_page) if (A or B) else \
                    (f_site + "/" + f_page)
        )
    
    def __getitem__(self, key):
        
        if (key in self.elements): return self.elements[key]
        
        print("ERROR 3")
        
    def format_page(self, page):
        
        return (
            self.pageformat.format(page) if (self.formattable) else \
                self.pageformat
        )
         
            
class DriverOptions(DSBase):
    
    MODE_CHROME = 10
    
    MODE_FIREFOX = 20
    
    DEFAULT = MODE_CHROME
    
    BROWSER_LIST = {
        MODE_CHROME : webdriver.Chrome,
        MODE_FIREFOX : webdriver.Firefox
    }
    
    PATH_INDEX = {
        MODE_CHROME : "service",
        MODE_FIREFOX : "executable_path"
    }
    
    PATH_LIST = {
        MODE_CHROME : ChromeService,
        MODE_FIREFOX : None
    }
    
    def __add_path_list(self, mode, path): return (path if (self.PATH_LIST[mode] == None) else self.PATH_LIST[mode](path))
    
    def __check_mode(self, mode):
        
        if ((mode == self.MODE_CHROME) or (mode == self.MODE_FIREFOX)): return mode
        
        elif (mode.lower() != "default"): print("ERROR 4")
        
        return self.DEFAULT
    
    def __check_path(self, path): return (path if (os.path.isfile(path) or os.path.exists(path)) else None)
    
    def __init__(self, mode = "default", path = None, window = True):
        super(DriverOptions, self).__init__("DriverOptions")
        
        (self.mode, self.path, self.window) = (
            self.__check_mode(self.check_types(mode, [str, int])),
            self.__check_path(self.check_types(path, [type(None), str])),
            self.check_types(window, [bool])
        )
        
    def __parse_arguments(self, mode, path, window):
        
        options = {}
        
        if (path != None): options[self.PATH_INDEX[mode]] = self.__add_path_list(mode, path)
        
        if (window == False): 
            
            if (mode == self.MODE_CHROME):
                
                headless = webdriver.ChromeOptions()
                
                headless.add_argument("headless")
                
            elif (mode == self.MODE_FIREFOX):
                
                headless = FirefoxOptions()
                
                headless.headless = True
                
            options["options"] = headless
            
        return options
    
    def get_driver(self):
        
        self.driver = self.BROWSER_LIST[self.mode](**self.__parse_arguments(self.mode, self.path, self.window))
        
        return self.driver
    
    def help():
        
        print("DriverOptions:")
        print("\t[1] __init__(self, mode = \"default\", path = None, window = True)")
        print("\t[2] get_driver(self)")
        print("\t[3] modes: self.MODE_CHROME, self.MODE_FIREFOX\n")
    
    
class DynamicData(DSBase):
    
    MODE_PATIENCE = 10
    
    MODE_ATTEMPTS = 20
    
    DEFAULT = MODE_PATIENCE
    
    PATIENCE_LIMIT = 5
    
    ATTEMPTS_LIMIT = 3
    
    LIMIT = PATIENCE_LIMIT
    
    QUANTUM = 0.01
    
    def help():
        
        print("DynamicData:")
        print("\t[1] __init__(self, driver)")
        print("\t[2] get_page(self, page) # page is preferrably a url")
        print("\t[3] find_element_by_xpath(self, xpath, multiple, mode)")
        print("\t[4] click_element_by_xpath(self, xpath, mode)")
        print("\t[5] modes: self.MODE_PATIENCE, self.MODE_ATTEMPTS\n")
    
    def __init__(self, driver):
        super(DynamicData, self).__init__("DynamicData")
        
        self.driver = self.check_types(driver, list(DriverOptions.BROWSER_LIST.values()))
    
    def __check_mode(self, mode):
        
        if ((mode == self.MODE_PATIENCE) or (mode == self.MODE_ATTEMPTS)): return mode
        
        elif ((type(mode) != str) or (mode.lower() != "default")): print("ERROR C")
        
        return self.DEFAULT
    
    def get_page(self, page):
        
        self.dyData = self.driver
        
        self.dyData.get(self.check_types(page, [str]))
        
        return self
    
    def find_element_by_xpath(self, xpath, multiple, mode):
        
        mode = self.__check_mode(mode)
        
        SOT = (datetime.datetime.now() if (mode == self.MODE_PATIENCE) else self.ATTEMPTS_LIMIT)
        
        while (((datetime.datetime.now() - SOT).total_seconds() <= self.PATIENCE_LIMIT) if (mode == self.MODE_PATIENCE) else (SOT)):
            
            try:
                
                found = (self.dyData.find_elements(By.XPATH, xpath) if (multiple) else self.dyData.find_element(By.XPATH, xpath))
                
                return found
            
            except:
                
                if (mode == self.MODE_ATTEMPTS): SOT = max(0, SOT - 1)
                
                time.sleep(self.QUANTUM)
    
    def click_element_by_xpath(self, xpath, mode):
        
        mode = self.__check_mode(mode)
        
        SOT = (datetime.datetime.now() if (mode == self.MODE_PATIENCE) else self.ATTEMPTS_LIMIT)
        
        while (((datetime.datetime.now() - SOT).total_seconds() <= self.PATIENCE_LIMIT) if (mode == self.MODE_PATIENCE) else (SOT)):
            
            try:
                
                found = self.dyData.find_element(By.XPATH, xpath) 
                
                found.click()
                
                return True
            
            except:
                
                if (mode == self.MODE_ATTEMPTS): SOT = max(0, SOT - 1)
                
                time.sleep(self.QUANTUM)
                
        return False
    
    
class DSData:
    
    def help():
        
        print("DSData: # This class is not intended for user to use")
        print("\t[1] __init__(self, info, filename = None, buffer = 100)")
        print("\t[2] empty_data(self) # empties data and returns empty list")
        print("\t[3] add_data(self, newData) # adds a list of data")
        print("\t[4] buffer_exceeded(self)")
        print("\t[5] save_data(self) # saves dataframe to a csv file\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [DSData]: expected type {exp_types} but received [ {type(item)} ].\n")
    
    def __check_filename(self, name):
        
        if (name == None):
            
            return TimeName().get_name("KDD-scraped", ".csv")
        
        return (name + (".csv" if (name[-4].lower() != ".csv") else ""))
    
    def __find_columns(self, info):
        
        return [
            attr["nickname"] if (attr["nickname"] != None) else str(index) \
                for index, attr in enumerate(info["f_attr"])
        ]
    
    def empty_data(self):
        
        self.data = []
        
        return []
    
    def __init__(self, info, filename = None, buffer = 100):
        
        (self.info, self.filename, self.buffer) = (
            self.__check_type(info, [DSInfo]), self.__check_type(filename, [str, type(None)]),
            max(1, self.__check_type(buffer, [int]))
        )
        
        (self.filename, self.columns, self.data) = (
            self.__check_filename(self.filename), self.__find_columns(self.info),
            self.empty_data()
        )
        
    def __collapse_filter(self, data):
        
        for index in range(len(data) - 1, -1, -1):
            
            keep = True
            
            for _index, attr in enumerate(self.info["f_attr"]):
                
                if (self.info["f_attr"][_index]["filter"] != None):
                
                    if not (attr["filter"])(data[self.columns[_index]][index]):
                        
                        keep = False
                
            if not (keep):
                
                data = data.drop(index)
                
        for index in range(len(self.info["f_attr"]) - 1, -1, -1):
            
            if not (self.info["f_attr"][index]["keep"]):
            
                column = self.columns[index]
                
                data.pop(column)
            
        return data
    
    def add_data(self, newData):
        
        self.data += newData
    
    def buffer_exceeded(self):
        
        return (len(self.data) >= self.buffer)
    
    def save_data(self, start = False):
        
        self.__collapse_filter(
            pandas.DataFrame(self.data, columns = self.columns)
        ).to_csv(
            self.filename, 
            index = False,
            header = start,
            mode = ("w" if start else "a"),
            encoding = "utf-8"
        )    

            
class DynamicScraper(DSBase):
    
    MODE_FILE = 10
    
    MODE_READ = 20
    
    DEFAULT = MODE_READ
    
    PER_PAGE = 20
    
    def help():
        
        print("DynamicScraper:")
        print("\t[1] __init__(self, info, driveroptions, mode = \"default\", filename = None, \n\t\ttimesleep = 0, buttonPath = None, itemWait = 1, buffer = 100)")
        print("\t[2] scrape(self, start = 1, pages = 1, perPage = None)")
        print("\t[3] modes: self.MODE_READ, self.MODE_FILE\n")
    
    def __check_mode(self, mode):
        
        if ((mode == self.MODE_FILE) or (mode == self.MODE_READ)): return mode
        
        elif ((type(mode) != str) or (mode.lower() != "default")): print("ERROR 6")
        
        return self.DEFAULT
    
    def __check_limit(self, limit):
        
        return (self.PER_PAGE if (limit == None) else limit)
    
    def __init__(self, info, driveroptions, mode = "default", filename = None, timesleep = 0, buttonPath = None, itemWait = 1, ** kwargs):
        super(DynamicScraper, self).__init__("DynamicScraper")
        
        (self.info, self.driveroptions, self.mode, self.filename, self.timesleep, self.buttonPath, self.itemWait) = (
            copy.deepcopy(self.check_types(info, [DSInfo])),
            self.check_types(driveroptions, [DriverOptions]),
            self.__check_mode(self.check_types(mode, [str, int])),
            self.check_types(filename, [type(None), str]),
            max(0, self.check_types(timesleep, [int, float])),
            self.check_types(buttonPath, [type(None), str]),
            max(0, self.check_types(itemWait, [int, float]))
        )
        
        self.driver = self.driveroptions.get_driver()
        
        self.dyData = DynamicData(driver = self.driver)
        
        if (self.mode == self.MODE_FILE):
            
            self.data = DSData(info = self.info, filename = self.filename, ** kwargs)
            
    def scrape(self, start = 1, pages = 1, perPage = None):
        
        _start, self.perPage = True, max(1, self.__check_limit(self.check_types(perPage, [type(None), float, int])))
        
        for page in range(start, start + pages):
            
            scrapeData = self.__scrape_page(start, page, pages)
            
            if (self.mode == self.MODE_FILE):
                
                self.data.add_data(scrapeData)
                
                if (self.data.buffer_exceeded()):
                    
                    self.data.save_data(_start)
                    
                    self.data.empty_data()
                    
                    _start = False
                    
            time.sleep(self.timesleep)
            
        print("")
        
        if ((self.mode == self.MODE_FILE) and (len(self.data.data))):
            
            self.data.save_data(_start)
            
            self.data.empty_data()
            
            _start = False
    
    def __find_attribute(self, source, attr):
        
        data = (source.get_attribute(attr["extract"]) if (attr["extract"] != None) else attr["extract"])
        
        return (data if (attr["format"] == None) else attr["format"](data))
    
    def __show_progress(self, start, current, pages, pointer, total1, total2, finish = False):
        
        if (finish): sys.stdout.flush()
            
        else: sys.stdout.write(f"\r\tScraping item {pointer} ({(pointer)} / {(min(total1, total2))}) from page {current} ({current - start + 1}/{pages})")
      
    def __scrape_page(self, start, page, pages):
        
        self.dyData.get_page(self.info.format_page(page))
        
        pointer, clickable = 1, True
        
        itemList = []
        
        while (pointer <= self.perPage):
            
            if (self.buttonPath != None): self.dyData.click_element_by_xpath(
                xpath = self.buttonPath,
                mode = DynamicData.MODE_ATTEMPTS
            )
            
            tree = len(self.dyData.find_element_by_xpath(
                xpath = self.info["f_item"]["xpath"], 
                multiple = self.info["f_item"]["multiple"], 
                mode = DynamicData.MODE_PATIENCE
            ))
            
            if (pointer > tree): break
        
            self.__show_progress(start, page, pages, pointer, tree, self.perPage)
            
            xpath = self.info["f_item"]["xpath"] + f"[{pointer}]"
            
            if ((clickable) and (self.info["f_item"]["click"])): self.dyData.click_element_by_xpath(
                xpath = xpath,
                mode = DynamicData.MODE_PATIENCE
            )
            
            time.sleep(self.itemWait)
            
            attrList, success, clickable = [], True, True
            
            for attr in self.info["f_attr"]:
                
                axPath = ((xpath + attr["xpath"]) if attr["relative"] else attr["xpath"])
                
                found = self.dyData.find_element_by_xpath(xpath = axPath, multiple = attr["multiple"], mode = DynamicData.MODE_PATIENCE)
                
                if (found == None):
                    
                    success, clickable = True, True
                    
                    break
                
                attrList.append(self.__find_attribute(found, attr))
                
                if ((attr["callback"] != None) and (attr["retry"] != None)):
                    
                    if not (attr["retry"](attrList[-1])):
                        
                        success, clickable = False, False
                        
                        break
                        
                    else: attr["callback"](attrList[-1])
                        
            if not (success): continue
                
            pointer += 1
            
            if (success): itemList.append(attrList)
            
        self.__show_progress(start, page, pages, pointer, tree, self.perPage, True)
             
        return itemList
                