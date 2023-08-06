from keyscraper.utils import TimeName, requests, copy, pandas, sys, time
import lxml
import bs4

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

class SSFormat:
    
    class __Dictionary:
        
        class __Item:
            
            def __check_list(self, typeList):
                
                if (type(typeList) == list):
                    
                    return typeList
                
                return [ typeList ]
            
            def __init__(self, defaultValue, typeList):
                
                self.value, self.typeList = [ defaultValue ], self.__check_list(typeList)
                
            def __getitem__(self, key):
                
                if (key == "value"):
                    
                    return self.value
                
                elif (key == "type"):
                    
                    return self.typeList
                
                raise Exception(f"Error [SSFormat]: cannot fetch from dictionary with key [ {key} ].\n")
        
        def __init__(self, element_type = None):
            
            self.dictionary = {
                "element_type" : self.__Item(None, [str]),
                "search_type" : self.__Item(None, [str]),
                "search_clue" : self.__Item(None, [str]),
                "multiple" : self.__Item(False, [bool]),
                "extract" : self.__Item(None, [str]),
                "format" : self.__Item(None, [any]),
                "nickname" : self.__Item(None, [str]),
                "filter" : self.__Item(None, [any]),
                "keep" : self.__Item(True, [bool])
            }
            
            if (type(element_type) == str):
                
                self.dictionary["element_type"]["value"][0] = element_type
            
        def __getitem__(self, key):
            
            return self.dictionary[key]
            
        def mod_value(self, key, newVal):
            
            if ((key in self.dictionary) and ((any in self.dictionary[key]["type"]) or (type(newVal) in self.dictionary[key]["type"]))):
                
                self.dictionary[key]["value"][0] = newVal
                
            else:
                
                print(f"Warning [SSFormat]: cannot update [ {key} ] in dictionary with value [ {newVal} ].\n")
    
    def help():
            
        print("SSFormat:")
        print("\t[1] __init__(self, element_type, search_type = None, search_clue = None, multiple = False, \n\t\textract = None, format = None, nickname = None, filter = None, keep = True)")
        print("\t[2] mode_value(self, key, newVal) # key as in kwargs")
        print("\t[3] get_value(self, key) # get copy of value for this key")
        print("\t[4] get_type(self, key) # get list of types for this key\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [SSFormat]: expected type {exp_types} but received [ {type(item)} ].\n")
    
    def __parse_arguments(self, ** kwargs):
        
        for key, value in kwargs.items():
            
            self.dictionary.mod_value(key, value)
    
    def __init__(self, element_type, ** kwargs):
        
        self.dictionary = self.__Dictionary(self.__check_type(element_type, [str]))
        
        self.__parse_arguments(**kwargs)
        
    def __getitem__(self, key):
        
        return self.dictionary[key]["value"][0]
        
    def get_value(self, key):
        
        return self.dictionary[key]["value"][0]
    
    def get_type(self, key):
        
        return self.dictionary[key]["type"]
    
class SSInfo:
    
    def help():
        
        print("SSInfo: ")
        print("\t[1] __init__(self, f_site, f_page, f_item, f_attr)")
        print("\t[2] format_page(self, page)")
        print("\t[3] __getitem__(self, key)\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [SSInfo]: expected type {exp_types} but received [ {type(item)} ].\n")
    
    def __merge_sitepage(self, site, page, formattable):
        
        if (formattable == False):
            
            return site
        
        A, B = (site[-1] == "/"), (page[0] == "/")
        
        if (A and B):
            
            return site[:-1] + page
        
        elif (A or B):
            
            return site + page
        
        else:
            
            return site + "/" + page
    
    def __init__(self, f_site, f_page, f_item, f_attr):
        
        (self.f_site, self.f_page, self.f_item, self.f_attr) = (
            self.__check_type(f_site, [str]), self.__check_type(f_page, [str]),
            self.__check_type(f_item, [SSFormat]), self.__check_type(f_attr, [list])
        )
        
        self.formattable = (self.f_page != "")
        
        self.formatPage = self.__merge_sitepage(self.f_site, self.f_page, self.formattable)
        
    def __getitem__(self, key):
        
        if (key == "f_site"):
            
            return self.f_site
        
        elif (key == "f_page"):
            
            return self.f_page
        
        elif (key == "f_item"):
            
            return self.f_item
        
        elif (key == "f_attr"):
            
            return self.f_attr
        
        raise Exception(f"Error [SSInfo]: cannot fetch item using key [ {key} ].\n")
    
    def format_page(self, page):
        
        return (self.formatPage.format(page) if self.formattable else self.formatPage)
    
class SSData:
    
    def help():
        
        print("SSData: # This class is not meant for user to use")
        print("\t[1] __init__(self, info, filename = None, buffer = 100)")
        print("\t[2] empty_data(self) # empties data and returns empty list")
        print("\t[3] add_data(self, newData) # adds a list of data")
        print("\t[4] buffer_exceeded(self)")
        print("\t[5] save_data(self) # saves dataframe to a csv file\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [SSData]: expected type {exp_types} but received [ {type(item)} ].\n")
    
    def __check_filename(self, name):
        
        if (name == None):
            
            return TimeName().get_name("KSD-scraped", ".csv")
        
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
            self.__check_type(info, [SSInfo]), self.__check_type(filename, [str, type(None)]),
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
        
class StaticScraper:
    
    MODE_FILE = 10
    
    MODE_READ = 20
    
    DEFAULT = MODE_FILE
    
    def help():
        
        print("StaticScraper:")
        print("\t[1] __init__(self, info, filename = None, mode = \"default\", timesleep = 0, buffer = 100)")
        print("\t[2] scrape(start = 1, pages = 1)\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [StaticScraper]: expected type {exp_types} but received [ {type(item)} ].\n")
    
    def __check_mode(self, mode):
        
        if ((mode == self.MODE_FILE) or (mode == self.MODE_READ)):
            
            return mode
        
        elif (mode.lower() != "default"):
            
            print(f"Warning [StaticScraper]: using default mode as [ {mode} ] is not supported.\n")
            
        return self.DEFAULT
    
    def __init__(self, info, filename = None, mode = "default", timesleep = 0, ** kwargs):
        
        (self.info, self.filename, self.mode, self.timesleep) = (
            copy.deepcopy(self.__check_type(info, [SSInfo])), self.__check_type(filename, [str, type(None)]), 
            self.__check_type(mode, [str, int]), max(0, self.__check_type(timesleep, [int, float]))
        )
        
        self.mode = self.__check_mode(self.mode)
        
        if (self.mode == self.MODE_FILE):
            
            self.data = SSData(self.info, self.filename, ** kwargs)
            
    def __show_progress(self, start, current, pages, finish = False):
        
        if (finish):
            
            sys.stdout.flush()
            
        else:
            
            sys.stdout.write(f"\r\tScraping page {current} ({current - start + 1}/{pages})")
        
    def __find_attributes(self, source, attr):
        
        data = (source.find_all if attr["multiple"] else source.find)
        
        data = data(
            attr["element_type"], ** (
                {} if ((attr["search_type"] == None) or (attr["search_clue"] == None)) else \
                    { attr["search_type"] : attr["search_clue"] }
            )
        )
            
        data = data if (attr["extract"] == None) else (
            data.text if (attr["extract"] == "text") else (
                data[attr["extract"]]    
            )    
        )
        
        if (attr["format"] != None):
            
            data = attr["format"](data)
            
        return data
        
    def __scrape_page(self, page):
        
        page = self.info.format_page(page)
        
        items = self.__find_attributes(
            bs4.BeautifulSoup(requests.get(page).text, "lxml"),
            self.info["f_item"]
        )
        
        itemList = []
        
        for item in items:
        
            attrList = []    
        
            for attr in self.info["f_attr"]:
                
                attrList.append(self.__find_attributes(item, attr))
                
            itemList.append(attrList)
            
        return itemList
        
    def scrape(self, start = 1, pages = 1):
        
        _start = True
        
        print(f"Scraping {self.info['f_site']}")
        
        for page in range(start, start + pages):
            
            self.__show_progress(start, page, pages)
            
            scrapeData = self.__scrape_page(page)
            
            if (self.mode == self.MODE_FILE):
                
                self.data.add_data(scrapeData)
                
                if (self.data.buffer_exceeded()):
                    
                    self.data.save_data(_start)
                    
                    self.data.empty_data()
                    
                    _start = False
                    
            self.__show_progress(start, page, pages, True)
            
            time.sleep(self.timesleep)
            
        print("")
        
        if ((self.mode == self.MODE_FILE) and (len(self.data.data))):
            
            self.data.save_data(_start)
            
            self.data.empty_data()
        
