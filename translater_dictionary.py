from configparser import ConfigParser

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

mode = 1

############################  functions  ##########################

# check if the network is ok
def net_check():
    try:
        requests.get("https://www.baidu.com", timeout= 5)
        return True
    except:
        return False

# google translate
def google_trans(content):
    """
        Func:
            Using google translate to translate the content.
        Args:
            content: the content you wanna translate -- it can be a string, and it can also be a list.
    """
    trans = Translator(service_urls=["translate.google.cn"])
    result = trans.translate(content, ini["to"])
    print("\n")
    print(" google translate ".center(40, "*"))
    print("\n\t", proc_str(result.text), "\n\n")

# Cambridge dictionary
def cam_dic(content):
    """
        Func:
            catching the Cambridge Online-dictionary's result and return a "dic" Object.
        Args:
            content: the word you wanna look for.
    """
    print("\n\n")
    print(" Cambridge Dictionary ".center(40, "*"), end="\n\n")
    
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
    
    word_ls = isWord(content)
    
    for word in word_ls:
        result_dic[word] = {}  # create a new word-space
        r_url = "https://dictionary.cambridge.org/us/dictionary/learner-english/%s"%(word)
        # r_url = "https://dictionary.cambridge.org/us/search/direct/?datasetsearch=learner-english&q=%s"%(content)
        # print(header["Referer"])
        
    # to get the checking result
        result = requests.get(r_url, headers=header)
        results = []
        results.append(result)
        # print(result.url)
        # if the word has multi-meaning
        if "1" in result.url.split("_")[-1]:
            # print(result.url)
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
                # print(position)
                for j in zh:
                    result_dic[word][position]["zh"].append(proc_str(j.text))
                    # print(proc_str(j.text))
                for j in en:
                    result_dic[word][position]["en"].append(proc_str(j.text))
                    # print(proc_str(j.text))
                for e in examples:
                    result_dic[word][position]["example"].append(proc_str(e.text))
                    # print(proc_str(e.text))
    
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
    command = {
        "dic off": 0,
        "dic on": 1
    }
    
    # We type "##" to enter the command mode
    if "## " in content:
        content = content.replace("## ", "")
        code = command[content]
        mode = code
        
        return mode
        
#################################  test code  ########################

if __name__ == "__main__":
    print("Checking the Internet Connection. Wait a minute please!\n")
    if net_check():
        content = get_input("Type the content, please: \n\t")
        mode = super_set(content)
        while content != "-1":
            mode = super_set(content)
            if len(content) != 0:
                google_trans(content)
                if mode:
                    cam_result = cam_dic(content)
                    for i in cam_result.keys():
                        for j in cam_result[i].keys():
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
            content = get_input("Type the content, please: \n\t")
    else:
        print("Please check your network connection!")
    
    