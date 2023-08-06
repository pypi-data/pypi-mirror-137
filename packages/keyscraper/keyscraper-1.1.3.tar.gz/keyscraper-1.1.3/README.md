# keyscraper Package Documentation
***
##### This library provides various functions which simplifies webpage scraping.

##### There are three modules in this package.

1. **utils** - _basic utilities_
2. **staticscraper** - _used to scrape raw html data_
3. **dynamicscraper** - _used to scrape html data rendered by **JavaScript**

##### To install this package, type in command prompt, "_pip install keyscraper_".

***
## [1] Basic Utilities

#### (1-A) _TimeName_ - Generating a file name composed of the current time:

###### TimeName(mode = "default")

|argument|optional|default|available|
|---|---|---|---|
|mode| _yes_ |"keywind"|"keywind", "datetime", "default"

###### self.get_name(basename = "", extension = "", f_datetime = None)

|argument|optional|default|available|
|---|---|---|---|
|basename|_yes_|""| [ string type ] |
|extension|_yes_|""| [ string type ] |
|f_datetime| _no_ | | [ string type ] |

There are two available modes: "_**keywind**_" and "_**datetime**_". By default, "_**keywind**_" is used.

In mode "_**keywind**_", the date is formatted as **D-{month}{day}{year}** where **{month}** consists of a **single character**, **{day}** is a **2-digit** number ranging from _**01 to 31**_ and **{year}** is a **4-digit** number such as _**2000**_.

|Jan.|Feb.|Mar.|Apr.|May|Jun.|Jul.|Aug.|Sep.|Oct.|Nov.|Dec.|
|--|--|--|--|--|--|--|--|--|--|--|--|
|i|f|m|a|M|j|J|A|s|o|n|d|

For example, on _**December 7th of 2000**_, **D-d072000** will be the resulting date string.

In mode "_**keywind**_", the time is formatted as **T-{hour}{minute}{second}** where **{hour}** consists of a **2-digit** number ranging from _**00 to 23**_, both **{minute}** and **{second}** are a **2-digit** number ranging from _**00 to 59**_.

For example, at _**05:43:07 PM.**_, the resulting time string will be **T-174307**.

For example, at _**01:23:45 AM.**_ on _**April 26th, 1986**_, the resulting string will be **{basename}_D-a261986_T-012345{extension}**.

In mode "_**datetime**_", the programmer must pass a _**strftime**_ string. The complete documentation to datetime formatting is linked [_here_](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).

##### (1-A-1) Example of using TimeName (mode: _keywind_).

1. _**from keyscraper.utils import TimeName**_
2. _**mode = "keywind" # "keywind" or "datetime"**_
3. _**name = "images"**_
4. _**extension = ".jpg"**_
5. _**timename = TimeName(mode).get_name(name, extension)**_
6. _**print(timename) # "images_D-d072000_T-012345.jpg"**_

##### (1-A-2) Example of using TimeName (mode: _datetime_).

1. _**from keyscraper.utils import TimeName**_
2. _**mode = "datetime" # "keywind" or "datetime"**_
3. _**format_string = "%y%m%d-%H%M%S"**_
4. _**name = "images"**_
5. _**extension = ".jpg"**_
6. _**timename = TimeName(mode).get_name(name, extension, format_string)**_
7. _**print(timename) # "images_001207-012345.jpg"**_

#### (1-B) _FileName_ - Dividing a filename into folder, file and extension:

###### FileName(filename, mode = "default")

|argument|optional|default|available|
|---|---|---|---|
|filename|_no_| | [ string type ] |
|mode|_yes_|FileName.MODE_FORWARDSLASH|FileName.MODE_FORWARDSLASH, FileName.MODE_BACKWARDSLASH|

###### self.\_\_getitem\_\_(key = "all")

|argument|optional|default|available|
|---|---|---|---|
|key|_no_|"all"|"all", "folder", "name", "extension"|

##### (1-B-1) Example of using FileName

1. _**from keyscraper.utils import FileName**_
2. _**mode = FileName.MODE_FORWARDSLASH**_
3. _**filename = "C:/Users/VIN/Desktop/utils.py"**_
4. _**name_object = FileName(filename)**_
5. _**full_name = name_object["all"]**_
6. _**file_name = name_object["name"]**_
7. _**folder_name = name_object["folder"]**_
8. _**extension = name_object["extension"]**_
9. _**print(full_name, file_name, folder_name, extension)**_
10. _**# "C:/Users/VIN/Desktop/utils.py utils C:/Users/VIN/Desktop/ .py"**_

#### (1-C) _FileRetrieve_ - Downloading a file from a direct URL:

###### FileRetrieve(directlink, filename = None, buffer = 4096, progress_bar = False, overwrite = None)

|argument|optional|default|available|
|---|---|---|---|
|directlink|_no_|  | [ string type ] |
|filename|_yes_|  | [ string type ] |
|buffer|_yes_|4096| [ integer (>0) type ] |
|progress_bar|_yes_|False|True, False|
|overwrite|_yes_|None|None, True, False|

If overwrite is _**None**_, the programmer will be asked to enter _**(Y/N)**_ on each download.

###### self.simple_retrieve()

Calling this function will download the file from the target URL and save it to disk with the provided filename.

##### (1-C-1) Example of using FileRetrieve

1. _**from keyscraper.utils import FileRetrieve**_
2. _**url = " http://www.lenna.org/len_top.jpg "**_
3. _**filename = "lenna.jpg"**_
4. _**progress_bar = True**_
5. _**overwrite = True**_
6. _**downloader = FileRetrieve(url, filename = filename, progress_bar = progress_bar, overwrite = overwrite)**_
7. _**downloader.simple_retrieve()**_

#### (1-D) _ImageGrabber_ - Downloading an image from a direct URL:

###### ImageGrabber(filename, progressBar = False, url_timeout = None)

|argument|optional|default|available|
|---|---|---|---|
|filename|_no_|  | [ string type ] |
|progressBar|_yes_|False|True, False|
|url_timeout|_yes_|600| [ integer (>0) type ] |

The URL request will be open for a maximum of _**url_timeout**_ seconds.

###### self.retrieve(directlink, overwrite = None, timeout = None)

|argument|optional|default|available|
|---|---|---|---|
|directlink|_no_| | [ string type ] |
|overwrite|_yes_|None|None, True, False|
|timeout|_yes_|None|None, [ integer (>0) type ] |

If the image hasn't finished downloading in _**timeout**_ seconds, the process will terminate.

If overwrite is _**None**_, the programmer will be asked to enter _**(Y/N)**_ on each download.

##### (1-D-1) Example of using ImageGrabber

1. _**from keyscraper.utils import ImageGrabber**_
2. _**url = " http://www.lenna.org/len_top.jpg "**_
3. _**filename = "lenna.jpg"**_
4. _**progressBar = True**_
5. _**url_timeout = 60**_
6. _**downloader = ImageGrabber(filename, progressBar = progressBar, url_timeout = url_timeout)**_
7. _**downloader.retrieve(url, overwrite = True, timeout = 15)**_

***

## [2] Static Scraper

#### (2-A) _SSFormat_ - Defining the node attributes to scrape:

###### SSFormat(element_type, **kwargs)

|argument|optional|default|available|
|---|---|---|---|
|element_type|_no_| | [ string type ] |
|search_type|_yes_|None|None, [ string type ] |
|search_clue|_yes_|None|None, [ string type ] |
|multiple|_yes_|False| True, False |
|extract|_yes_|None|None, [ function (1-arg) type ] |
|format|_yes_|None|None, [ function (1-arg) type ] |
|nickname|_yes_|None|None, [ string type ] |
|filter|_yes_|None|None, [ function (1-arg) type ] |
|keep|_yes_|True|True, False |

###### self.\_\_getitem\_\_(key)

|argument|optional|default|available|
|---|---|---|---|
|key|_no_| | "element_type", "search_type", "search_clue", "multiple", "extract", "format", "nickname", "filter", "keep"|

###### self.get_value(key)

|argument|optional|default|available|
|---|---|---|---|
|key|_no_| | "element_type", "search_type", "search_clue", "multiple", "extract", "format", "nickname", "filter", "keep"|

#### (2-B) _SSInfo_ - Defining information needed for scraping:

###### SSInfo(f_site, f_page, f_item, f_attr)

|argument|optional|default|available|
|---|---|---|---|
|f_site|_no_| | [ string type ] |
|f_page | _no_| | [ string type ] |
|f_item | _no_ | | [ SSFormat type ] |
|f_attr | _no_ | | [ list-SSFormat type ] |

###### self.\_\_getitem\_\_(key)

|argument|optional|default|available|
|---|---|---|---|
|key|_no_| | "f_site", "f_page", "f_item", "f_attr"|

###### self.format_page(page)

|argument|optional|default|available|
|---|---|---|---|
|page|_no_| | [ integer/string type ]|

If _**f_page**_ is not an empty string, page is put into _**f_page**_ inside curly braces. For instance, if _**f_page**_ = **"page-{}.html"** and _**page**_ = **5**, this function will return **"page-5.html"**. On the contrary, if _**f_page**_ = **""**, the function will return **""**.

#### (2-C) _StaticScraper_ - Scraping a static webpage:

###### StaticScraper(info, filename = None, mode = "default", timesleep = 0, **kwargs)

|argument|optional|default|available|
|---|---|---|---|
|info|_no_| | [ SSInfo type ] |
|filename|_yes_|None|None, [ string type ]|
|mode|_yes_|StaticScraper.MODE_FILE|StaticScraper.MODE_FILE, StaticScraper.MODE_READ|
|timesleep|_yes_|0|[ integer/float (>=0) type ] |
|buffer|_yes_|100|[ integer (>0) type ]|

###### self.scrape(start = 1, pages = 1)

|argument|optional|default|available|
|---|---|---|---|
|start|_yes_|1|[ integer (>0) type ]|
|pages|_yes_|1|[ integer (>0) type ]|

##### (2-C-1) Example of using StaticScraper

1. _**from keyscraper.staticscraper import SSFormat, SSInfo, StaticScraper**_
2. _**f_site = " http://books.toscrape.com/catalogue/ "**_
3. _**f_page = "page-{}.html"**_
4. **f\_item = SSFormat(element\_type = "li", search\_type = "class\_", search\_clue = "col-xs-6 col-sm-4 col-md-3 col-lg-3", multiple = True)**
5. __**f\_price = SSFormat(element\_type = "p", search\_type = "class\_", search\_clue = "price\_color", extract = "text", nickname = "price")**__
6. _**f_url = SSFormat(element\_type = "a", extract = "href", nickname = "link")**_
7. _**f_attr = [ f\_price, f\_url ]**_
8. _**info = SSInfo(f\_site, f\_page, f\_item, f\_attr)**_
9. _**scraper = StaticScraper(info)**_
10. _**scraper.scrape(start = 1, pages = 15)**_
