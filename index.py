"""
	###########################################################################
	#		                                                                  #
	#		Project: Translator & Dictionary                                  #
	#		                                                                  #
	#		Filename: index.py                                                #
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


from flask import Flask, render_template, request
import translater_dictionary as td

app = Flask(__name__)

# the home page
@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        content = request.form.get("search")
        google, cam_dic, content = get_search(content)
        # check the content to choose the api
        code = mode_code(content, cam_dic)
        return render_template("h.html", google=google, cam_dic=cam_dic, content=content, code=code)

# the search-result-show page
@app.route('/search', methods=['POST'])
def search():
    content = request.form.get("search")
    google, cam_dic, content = get_search(content)
    code = mode_code(content, cam_dic)
    return render_template("h.html", google=google, cam_dic=cam_dic, content=content, code=code)

def mode_code(content, cam_dic):
    if len(content) == 0:
        code = 0
    elif (cam_dic == {}) or (" " in content):
        code = 1
    else:
        code = 2
    return code

# the core function to get the translate result
def get_search(content):
    content = content.replace("\n", " ")
    content = content.replace("  ", " ")
    content = td.proc_str(content)
    google = ""
    cam_dic = {}
    if len(content) != 0:
        if td.isChinese(content) or (" " in content):
            google = td.google_trans(content, "en").text
        else:
            if " " in content:
                mode = 0
            else:
                mode = 1
            google = td.google_trans(content).text
            cam_dic = td.cam_dic(content, mode)

    return google, cam_dic, content


if __name__ == "__main__":
    app.run()