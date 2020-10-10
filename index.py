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

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("./templates/index.html")
    else:
        content = request.form.get("search")
        google, cam_dic, content = get_search(content)
        return render_template("./templates/h.html", google=google.text, cam_dic=cam_dic, content=content, code=code)


@app.route('/search', methods=['POST'])
def search():
    content = request.form.get("search")
    google, cam_dic, content = get_search(content)
    code = len(content)
    return render_template("./templates/h.html", google=google.text, cam_dic=cam_dic, content=content, code=code)


def get_search(content):
    content = content.replace("\n", " ")
    content = content.replace("  ", " ")
    content = td.proc_str(content)
    google = ""
    cam_dic = {}
    if len(content) != 0:
        if td.isChinese(content):
            google = td.google_trans(content, "en")
        else:
            google = td.google_trans(content)
            cam_dic = td.cam_dic(content)

    return google, cam_dic, content


if __name__ == "__main__":
    app.run()S