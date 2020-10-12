"""
	###########################################################################
	#		                                                                  #
	#		Project: Translator & Dictionary                                  #
	#		                                                                  #
	#		Filename: translater_dictionary.py                                #
	#		                                                                  #
	#		Programmer: Vincent Holmes (Vincent_HolmesZ@outlook.com)          #
	#		                                                                  #
	#		Description: if you like this, feel free to click and give me a   #
	#                      star~~                                             #
	#		                                                                  #
	#		Start_date: 2020-10-10                                            #
	#		                                                                  #
	#		Last_update: 2020-10-10                                           #
	#		                                                                  #
	###########################################################################
"""


from configparser import ConfigParser
import logging
import traceback
from threading import Thread
from time import sleep
import os
import sys

# Check the required packages
try:
    import requests
    from bs4 import BeautifulSoup
    from googletrans import Translator
except Exception as e:
    print(e)


############################  load the initialization file  ################

cfg = ConfigParser()
cfg.read("./lang.ini")
ini = dict(cfg.items("language"))

############################  params  ##########################



############################  functions  ##########################

# check if the network is ok
def net_check():
    try:
        requests.get("https://www.baidu.com", timeout= 5)
        return True
    except:
        return False

# Cambridge dictionary
def cam_dic(content, mode = 1):
    """
        Func:
            catching the Cambridge Online-dictionary's result and return a "dic" Object.
        Args:
            content: the word you wanna look for.
    """
    result_dic = {}
    
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Host": "dictionary.cambridge.org",
        "Referer": "https://dictionary.cambridge.org/us/dictionary/learner-english/%s"%(content),
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    param = {
        "datasetsearch": "learner-english",
        "q": content
    }
    
    if mode == 1:
        word_ls = isWord(content)
    else:
        word_ls = []
    
    for word in word_ls:
        result_dic[word] = {}  # create a new word-space
        r_url = "https://dictionary.cambridge.org/us/dictionary/learner-english/%s"%(word)
        
    # to get the checking result
        result = requests.get(r_url, headers=header)
        results = []
        results.append(result)
        if "1" in result.url.split("_")[-1]:
            try:
                for i in [2,3]:
                    results.append(requests.get(r_url+"_%s"%(i), headers=header))
            except:
                pass
        else:
            results.append(result)
        
        # parsing the page
        for r in results:
            soup = BeautifulSoup(r.text, "html.parser")
            zh = soup.find_all(attrs={"[class]":"stateDictTrans.dataset == 'english-chinese-traditional' ? 'had lmt-20' : 'had lmt-20 nojs'"})
            en = soup.find_all(attrs={"class":"def ddef_d db"})
            pos = soup.find_all(attrs={"class":"pos dpos"})
            examples = soup.find_all(attrs={"class":"examp dexamp"})
            for i in pos:
                position = proc_str(i.text)
                result_dic[word][position] = {}
                result_dic[word][position]["zh"] = []
                result_dic[word][position]["en"] = []
                result_dic[word][position]["example"] = []
                for j in zh:
                    result_dic[word][position]["zh"].append(proc_str(j.text))
                for j in en:
                    result_dic[word][position]["en"].append(proc_str(j.text))
                for e in examples:
                    result_dic[word][position]["example"].append(proc_str(e.text))
        result_dic[word]["pos"] = [pos for pos in result_dic[word].keys()]
    return result_dic

# process the string
def proc_str(string):
    delete = ["  ", "\t", "See more", "Learn more.", "\n", ":"]
    for i in delete:
        string = string.replace(i, "")
    return string

# to check whether the content is a word: if not, it will seperate it and return a list of words.
def isWord(content):
    if ' ' in content:
        if input("\tWanna lookup for each word?(y/n) ") == 1:
            return content.split(" ")
        else:
            return []
    else:
        return [content]

def get_input(title):
    """
        Func:
            to get every line of content and combine them together.
    """
    content = ""
    print(title)
    while 1:
        part_sentence = input()
        if len(part_sentence) == 0:
            break
        else:
            content += part_sentence
    content = content.replace("\n", " ")
    content = content.replace("  ", " ")
    content = proc_str(content)
    
    return content

def super_set(content):
    """
        Func:
            to set something by using commands.
    """
    command = {
        "dic off": 0,
        "dic on": 1,
    }
    
    # We type "##" to enter the command mode
    if "## " in content:
        content = content.replace("## ", "")
        mode = command.get(content, 1)
        
        return mode
    
    return 1

def isChinese(strs, type=0):
    """
        Func:
            to check if there's chinese in the content。

        Args:
            type: default to be 0, means it returns True only if all the content is Chinese
                  when type=1, it returns True if there's at least one chinese letter in it
    """
    chinese = []
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            chinese.append(False)
        else:
            chinese.append(True)
    if type == 0:
        if not False in chinese:
            return True
        else:
            return False
    else:
        if True in chinese:
            return True
        else:
            return False

# google translate
def google_trans(content, l_to = ini["to"]):
    """
        Func:
            Using google translate to translate the content.
        Args:
            content: the content you wanna translate -- it can be a string, and it can also be a list.
            l_to: the language you wanna translate to(default to be zh-CH)
    """
    trans = Translator(service_urls=["translate.google.cn"])
    result = trans.translate(content, l_to)
    
    return result

class Trans_Dic():
    def __init__(self):
        self.finished = [1,1]
        self.mode = 1
        self.content = ""
        
    def show_Cam_result(self):
        if self.mode == 1:
            cam_result = cam_dic(self.content)
            print(cam_result)
            print("\n\n")
            print(" Cambridge Dictionary ".center(40, "*"), end="\n\n")
            for i in cam_result.keys():
                for j in cam_result[i]["pos"]:
                    print("\nPosition: ", j)
                    print("\nChinese: ")
                    for k in cam_result[i][j]["zh"]:
                        print("\t", k)
                    
                    print("\nEnglish: ")
                    for k in cam_result[i][j]["en"]:
                        print("\t", k)
                    
                    if len(cam_result[i][j]["example"]) != 0:
                        print("\nExample: ")
                        for k in cam_result[i][j]["example"]:
                            print("\t", k)
                        print("\n\n")
                    else:
                        print("\nDon't have an example.\n\n")
            self.finished[1] = 1
    
    # google translate
    def google_trans(self, l_to = ini["to"]):
        """
            Func:
                Using google translate to translate the content.
            Args:
                content: the content you wanna translate -- it can be a string, and it can also be a list.
                l_to: the language you wanna translate to(default to be zh-CH)
        """
        trans = Translator(service_urls=["translate.google.cn"])
        result = trans.translate(self.content, l_to)
        print("\n")
        print(" google translate ".center(40, "*"))
        print("\n\t", proc_str(result.text), "\n\n")
        self.finished[0] = 1
    
    def main(self):
        print("Checking the Internet Connection. Wait a minute please!\n")
        try:
            if net_check():
                self.content = get_input("Type the content, please: \n\t")
                self.mode = super_set(self.content)
                
                while self.content != "-1":
                    t = []  # threading pool
                    self.mode = super_set(self.content)
                    if len(self.content) != 0:
                        if isChinese(self.content, 1):
                            t.append(Thread(target = self.google_trans, args = ("en",)))
                            self.finished[0] = 0
                        else:
                            t.append(Thread(target = self.google_trans))
                            t.append(Thread(target = self.show_Cam_result))
                            self.finished[0] = 0
                            self.finished[1] = 0
                    for i in t:
                        i.start()
                    while 0 in self.finished:
                        sleep(1)
                    self.content = get_input("Type the content, please: \n\t")
            else:
                print("Please check your network connection!")
        except Exception as e:
            logging.error(traceback.format_exc(3))

class Youdao:
    """
        Func:
            look up word in YouDao
    """

    params = {
        'keyfrom': 'longcwang',
        'key': '131895274',
        'type': 'data',
        'doctype': 'json',
        'version': '1.1',
        'q': 'query'
    }
    api_url = u'http://fanyi.youdao.com/openapi.do'
    voice_url = u'http://dict.youdao.com/dictvoice?type=2&audio={word}'
    web_url = u'http://dict.youdao.com/w/eng/{0}/#keyfrom=dict2.index'

    error_code = {
        0:  'normal',
        20: 'your content is too long',
        30: 'Cannot translate well',
        40: 'Unsupported language type',
        50: 'Invalid key',
        60: 'dictionary doesn\'t have results'
    }

    result = {
        "query": "",
        "errorCode": 0,
    }

    def __init__(self, word):
        self.word = word
        self.result = {}
        self.result["basic"] = {}

    def get_result(self, use_api=False):
        """
            Func:
                to get the result
            
            Args:
                use_api:whether using YouDao-API, or spider the web-page
            
            Return:
                a dictionary include searching result
        """
        try:
            if use_api:
                self.params['q'] = self.word
                r = requests.get(self.api_url, params=self.params)
                r.raise_for_status()  # a 4XX client error or 5XX server error response
                self.result = r.json()
            else:
                r = requests.get(self.web_url.format(self.word))
                r.raise_for_status()
                self.parse_html(r.text)
        except Exception as e:
            logging.error(traceback.format_exc(3))
        return self.result

    def parse_html(self, html):
        """
            Func:
                parsing web-YouDao
            
            Args:
                html: the webpage
            
            Return:
                the result
        """
        soup = BeautifulSoup(html, "lxml")
        root = soup.find(id='results-contents')

        # query: the keyword you search
        keyword = root.find(class_='keyword')
        if not keyword:
            self.result['query'] = self.word
        else:
            self.result['query'] = keyword.string

        # the basic explains
        basic = root.find(id='phrsListTab')
        if basic:
            trans = basic.find(class_='trans-container')
            if trans:
                self.result['basic'] = {}
                self.result['basic']['explains'] = [tran.string for tran in trans.find_all('li')]
                # Chinese
                if len(self.result['basic']['explains']) == 0:
                    exp = trans.find(class_='wordGroup').stripped_strings
                    self.result['basic']['explains'].append(' '.join(exp))

                # phonetic
                phons = basic(class_='phonetic', limit=2)
                if len(phons) == 2:
                    self.result['basic']['uk-phonetic'], self.result['basic']['us-phonetic'] = \
                        [p.string[1:-1] for p in phons]
                elif len(phons) == 1:
                    self.result['basic']['phonetic'] = phons[0].string[1:-1]
        else:
            self.result['basic'] = {}
        
        #translate
        trans = root.find(id='fanyiToggle')
        if trans:
            self.result["translate"] = trans.find_all("p")[1].text

        # phrase
        web = root.find(id='webPhrase')
        if web:
            web_result = [
                {
                    'key': wordgroup.find(class_='search-js').string.strip(),
                    'value': [v.strip() for v in wordgroup.find('span').next_sibling.split(';') if not v.strip() == ""]
                } for wordgroup in web.find_all(class_='wordGroup', limit=10)
            ]
            
            self.result['webPhrase'] = [phrase for phrase in web_result if phrase["value"] != []]
   
#################################  test code  ########################

if __name__ == "__main__":
    trans = Trans_Dic()
    test = Youdao("This").get_result()
    print(test)
    trans.main()
    
    
    