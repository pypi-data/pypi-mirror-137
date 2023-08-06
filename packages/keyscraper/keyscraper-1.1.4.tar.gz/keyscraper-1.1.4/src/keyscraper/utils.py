import mimetypes # 
import threading #
import datetime #
import requests 
import pandas 
import urllib #
import copy #
import time #
import sys #
import os #

urllib2 = urllib.request
Timer = threading.Timer


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

class TimeName:
    
    month_table = [
        "i", "f", "m", "a", "M", "j", "J", "A", "s", "o", "n", "d"    
    ]
    
    mode_table = {
        "keywind" : 10,
        "datetime" : 20        
    }
    
    MODE_KEYWIND = mode_table["keywind"]
    
    MODE_DATETIME = mode_table["datetime"]
    
    DEFAULT = MODE_KEYWIND
    
    def help():
        
        print("TimeName: ")
        print("\t[1] __init__(self, mode = \"default\")")
        print("\t[2] get_name(self, basename = \"\", appendix = \"\", f_datetime = None)")
        print("\t[3] change_mode(self, mode)\n")
        
    def __check_mode(self, mode):
        
        if (mode in list(self.mode_table.values())):
            
            return mode
        
        if ((type(mode) != str) or (mode.lower() != "default")):
            
            print(f"Warning [TimeName]: using default mode as [ {mode} ] is not a valid mode.\n")
        
        return self.DEFAULT
        
    def __init__(self, mode = "default"):
        
        self.mode = self.__check_mode(mode)
        
    def change_mode(self, mode):
        
        self.mode = self.__check_mode(mode)
        
        return self
    
    def __format_length(self, value, digits = 2):
        
        value = (value if (type(value) == str) else str(value))
        
        return (" " * max(0, digits - len(value)) + value)
    
    def __get_time(self, f_datetime = None):
        
        curTime = datetime.datetime.now()
        
        if (self.mode == self.MODE_DATETIME):
            
            if (f_datetime == None): raise Exception("Error [TimeName]: expected formattable string for datetime but received None.\n")
                
            try: return curTime.strftime(f_datetime)
            
            except: raise Exception("Error [TimeName]: received non-formattable string for datetime.\n")
                
        (year, month, day, hour, minute, second) = (
            curTime.strftime("%y"), curTime.strftime("%m"), 
            curTime.strftime("%d"), curTime.strftime("%H"),
            curTime.strftime("%M"), curTime.strftime("%S")
        )
        
        return "".join([
            "_D-", str(self.month_table[int(month) - 1]), self.__format_length(day), "20",
            self.__format_length(year), "_T-", self.__format_length(hour), 
            self.__format_length(minute), self.__format_length(second)
        ])
    
    def get_name(self, basename = "", appendix = "", f_datetime = None):
        
        basename = basename if (type(basename) == str) else ""
        
        appendix = appendix if (type(basename) == str) else ""
        
        return basename + self.__get_time(f_datetime) + appendix
    
    
class FileName:
    
    MODE_FORWARDSLASH = 10
    
    MODE_BACKWARDSLASH = 20
    
    DEFAULT = 10
    
    def help():
        
        print("FileName: ")
        print("\t[1] __init__(self, filename, mode = \"default\")")
        print("\t[2] __getitem__(self, key = \"all\") # folder, name, extension, all\n")
    
    def __check_mode(self, mode):
        
        if ((mode == self.MODE_FORWARDSLASH) or (mode == self.MODE_BACKWARDSLASH)):
            
            return mode
        
        if ((type(mode) != str) or (mode.lower() != "default")):
            
            print(f"Warning [FileName]: using default mode as [ {mode} ] is not a valid mode.\n")
            
        return self.DEFAULT
    
    def __check_name(self, name):
        
        if (type(name) == str):
            
            return name
        
        raise Exception(f"Error [FileName]: expected a string for filename but received [ {name} ] of type [ {type(name)} ].\n")
    
    def __init__(self, filename, mode = "default"):
        
        self.filename = self.__check_name(filename)
        
        self.mode = self.__check_mode(mode)
        
        self.__parse_name()
        
    def __getitem__(self, key = "all"):
        
        if (key in self.nameParts): return self.nameParts[key]
        
        elif ((type(key) == str) and (key.lower() == "all")): return self.filename
        
        raise Exception(f"Error [FileName]: [ {key} ] is not a valid key.\n\tAvailable Keys: {list(self.nameParts.keys())}\n")
    
    def __parse_name(self):
        
        dirChar = ("/" if (self.mode == self.MODE_FORWARDSLASH) else "\\")
        
        self.nameParts = {
            "folder" : "",
            "name" : "",
            "extension" : ""
        }
        
        if (self.filename != ""):
        
            length, folderIndex, extensionIndex = len(self.filename), None, None
        
            for index in range(length - 1, -1, -1):
                
                if (folderIndex != None): break
                
                if ((extensionIndex == None) and (self.filename[index] == ".")):
                    
                    extensionIndex = index
                    
                elif (self.filename[index] == dirChar):
                    
                    folderIndex = index
                    
            if (extensionIndex != None):
                
                self.nameParts["extension"] = self.filename[ extensionIndex : ]
                
            else:
                
                extensionIndex = length
                
            if (folderIndex != None):
                
                self.nameParts["folder"] = self.filename[ : (folderIndex + 1) ]
                
            else:
                
                folderIndex = -1
                
            self.nameParts["name"] = self.filename[ (folderIndex + 1) : extensionIndex ]
            
        else:
            
            print("Warning [FileName]: received an empty string as filename.\n")
         
class FileRetrieve:
    
    DEFAULT_BUFFER = 16384
    
    DEFAULT_PROGRESS = False
    
    def help():
        
        print("FileRetrieve:")
        print("\t[1] __init__(self, directlink, filename = None, buffer = 4096, progress_bar = False, overwrite = None)")
        print("\t[2] retrieve(self)\n")
    
    def __check_type(self, item, exp_types):
        
        if (type(item) in exp_types):
            
            return item
        
        raise Exception(f"Error [FileRetrieve]: expected type {exp_types} as parameters but received [ {type(item)} ].\n")
    
    def __decide_overwrite(self, filename):
        
        while "Keywind":
            
            print(f"File {filename} already exists. Overwrite? (Y/N)")
            
            userinput = input("> ").lower()
            
            if (userinput[0] == 'y'):
                
                return True
            
            elif (userinput[0] == 'n'):
                
                return False
    
    def __file_name(self, filename, found_type = None):
        
        name = FileName(filename)
                
        extension = (found_type if ((name["extension"] == "") and (found_type != None)) else name["extension"])
        
        filename = name["folder"] + name["name"] + extension
        
        if (os.path.isfile(filename)):
            
            self.overwrite = (self.__decide_overwrite(filename) if (self.overwrite == None) else self.overwrite)
            
            if (self.overwrite == False):
                
                return TimeName().get_name(name["folder"] + name["name"], extension)
            
        return filename
    
    def __init__(self, directlink, filename = None, buffer = 4096, progress_bar = False, overwrite = None):
        
        (self.directlink, self.filename, self.buffer, self.progress_bar, self.overwrite) = (
            self.__check_type(directlink, [str]), self.__check_type(filename, [str, type(None)]),
            self.__check_type(buffer, [int]), self.__check_type(progress_bar, [bool]), 
            self.__check_type(overwrite, [bool, type(None)])
        )
        
        self.filename = (TimeName().get_name("KFR-temp") if (self.filename == None) else self.filename)
        
        self.buffer = (self.buffer if (self.buffer > 0) else self.DEFAULT_BUFFER)
        
    def __show_progress(self, current, total, endline = False):
        
        if (self.progress_bar):
        
            sys.stdout.write(f"\rDownloading [{self.__abbrev(self.directlink)}] -> [{self.__abbrev(self.filename)}] ({round(current/total*100, 1)}%)")
            
            sys.stdout.flush()

        if (endline):
   
            print("\n")
    
    def __abbrev(self, string):
        
        return (string if (len(string) <= 20) else (string[:10] + " ... " + string[-10:]))
    
    def simple_retrieve(self):
        
        try:
            
            rawData = requests.get(self.directlink, stream = True)
            
            (temp, length, foundType) = (
                0, int(rawData.headers.get("content-length")), 
                mimetypes.guess_extension((rawData.headers.get("content-type")))
            )
            
            self.filename = self.__file_name(self.filename, foundType)
            
            with open(self.filename, "wb") as writeFile:
                
                for data in rawData.iter_content(chunk_size = self.buffer):
                    
                    writeFile.write(data)
                    
                    self.__show_progress(temp, length)
                    
                    temp += len(data)
                    
            self.__show_progress(temp, length, endline = True)
            
        except Exception:
            
            print(f"Warning [FileRetrieve]: cannot download file from [ {self.__abbrev(self.directlink)} ]\n")

    def advanced_retrieve(self, guess_image = False):
        
        try:
            
            opener = urllib.request.build_opener()
            
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            
            urllib.request.install_opener(opener)
            
            foundType = None
            
            if (guess_image):
            
                if (self.directlink[:11] == "data:image/"):
                        
                    A, B = self.directlink.split("/")[1][:11].lower(), self.directlink.split("/")[1][:10].lower()
                    
                    foundType = (".jpg" if ((A == "jpeg;base64") or (B == "jpg;base64"))else ".png" if (B == "png;base64") else ".webp")
                
                else:
                    
                    A = self.directlink[-10:].lower()
                    
                    foundType = (".png" if ("png" in A) else ".webp" if ("webp" in A) else ".jpg")
            
            filename = self.__file_name(self.filename, foundType)
            
            urllib.request.urlretrieve(self.directlink, filename)
            
        except Exception:
            
            print(f"Warning [FileRetrieve]: cannot download file from [ {self.__abbrev(self.directlink)} ]\n")


def check_folder(folder):
    
    if (os.path.exists(folder)):
        
        return True
    
    os.mkdir(folder)
    
    return False

class Retry:
    
    PATIENCE = 15
    
    def __init__(self): self.reset_SOT()
        
    def reset_SOT(self): self.SOT = datetime.datetime.now()
        
    def retry(self, link):
        
        if (((type(link) != str) or (link[:11] == "data:image/") or (link[:17] == "https://encrypted")) and \
            ((datetime.datetime.now() - self.SOT).total_seconds() < self.PATIENCE)):
            return False
        
        self.reset_SOT()
        
        return True
    
    
class BaseUtils:
    
    DEF_NAME = "BaseUtils"
    
    LENGTH = 20
    
    _LENGTH = int(LENGTH / 2)
    
    def help():
        
        print("BaseUtils: # this class is not meant for user to use")
        print("\t[1] __init__(self, className)")
        print("\t[2] check_type(self, item, exp_types)")
        print("\t[3] abbrev(self, string)\n")
    
    def check_type(self, item, exp_types):
        
        if (type(item) in exp_types): return item
        
        raise Exception(f"TypeError [{self.className}]: expected {exp_types} but received [ {type(item)} ] \n")
    
    def __init__(self, className):
        
        self.className = self.DEF_NAME
        
        self.className = self.check_type(className, [str])
        
    def abbrev(self, string):
        
        if (len(string) <= self.LENGTH): return string
            
        return string[:self._LENGTH] + " ... " + string[-self._LENGTH:] 
        
    
class ImageGrabber(BaseUtils):
    
    DEFAULT_EXTENSION = ".jpg"
    
    CHUNK_SIZE = 4096
    
    DEF_TIMEOUT = 600
    
    IMAGE_LIST = {
        "image/jpeg" : ".jpg",
        "image/png" : ".png",
        "image/jpg" : ".jpg",
        "image/webp" : ".webp",
        "image/gif" : ".gif",
        "image/tiff" : ".tiff"
    }
    
    def help():
        
        print("ImageGrabber:")
        print("\t[1] __init__(self, filename, progressBar = False)")
        print("\t[2] retrieve(self, directlink, overwrite = None, timeout = None)\n")
    
    def __check_to(self, timeout): return (self.DEF_TIMEOUT if (timeout == None) else timeout)
    
    def __init__(self, filename, progressBar = False, url_timeout = None):
        
        super(ImageGrabber, self).__init__("ImageGrabber")
        
        self.filename = FileName(
            filename = self.check_type(filename, [str]),
            mode = "default"
        )
        
        self.progressBar = self.check_type(progressBar, [bool])
        
        self.url_timeout = self.__check_to(self.check_type(url_timeout, [type(None), float, int]))
    
    def __decide_overwrite(self, filename):
        
        while "keywind":
            
            print(f"{self.abbrev(filename)} already exists. Overwrite? (Y/N)")
            
            userInput = input("> ").lower()
            
            if (userInput == "y"): return True
            
            elif (userInput == "n"): return False
    
    def __mod_filename(self, filename, extension):
        
        _filename = filename["all"]
        
        if ((filename["extension"] == "") and (extension != None)):
            
            _filename = filename["folder"] + filename["name"] + extension
        
        if (os.path.isfile(_filename)):
            
            if ((self.overwrite == False) or ((self.overwrite == None) and (not self.__decide_overwrite(_filename)))):
                
                __filename = FileName(_filename)
                
                return TimeName().get_name(basename = (__filename["folder"] + __filename["name"]), appendix = __filename["extension"])
            
        return _filename
    
    def __check_image_type(self, imageType): return (self.IMAGE_LIST[imageType] if (imageType in self.IMAGE_LIST) else self.DEFAULT_EXTENSION)
    
    def __progress(self, current, total, finish = False):
        
        if (self.progressBar == False): return
        
        if (finish): sys.stdout.write("\n")
        
        else: 
            
            sys.stdout.write(f"\rDownloading [{self.abbrev(self.directlink)}] ({round((100 * current / total), 1)}%)")
            
            sys.stdout.flush()
    
    def __retrieve(self, filename):
        
        opener = urllib2.build_opener()
        
        opener.add_headers = [ ('User-agent', 'Mozilla/5.0') ]
        
        urllib2.install_opener(opener)
        
        try:
        
            remote = urllib2.urlopen(
                self.directlink,
                timeout = self.url_timeout
            )
            
            (length, extension) = (
                int(remote.info().get("content-length").strip()),
                self.__check_image_type(remote.info().get("content-type"))
            )
            
            #print(type(length), length)
        
            pointer = 0
            
            if (self.timeout != None):
                
                timer = Timer(self.timeout, remote.close)
                
                timer.start()
            
            filename = self.__mod_filename(filename, extension)
            
            self.__progress(pointer, length)
            
            with open(filename, "wb") as WFILE:
            
                while "keywind":
                    
                    read = remote.read(self.CHUNK_SIZE)
                    
                    if not (read): break
                
                    WFILE.write(read)
                    
                    pointer += len(read)
                    
                    self.__progress(pointer, length)
                    
            self.__progress(pointer, length, True)
            
            if (self.timeout != None): timer.cancel()
                    
        except Exception as e:
            
            #print(e)
            pass
                
    def retrieve(self, directlink, overwrite = None, timeout = None):
        
        (self.directlink, self.overwrite, self.timeout) = (
            self.check_type(directlink, [str]),
            self.check_type(overwrite, [bool, type(None)]),
            self.check_type(timeout, [type(None), int, float])
        )
        
        self.__retrieve(self.filename)