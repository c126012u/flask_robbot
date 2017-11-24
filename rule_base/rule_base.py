# coding: utf-8　　　　　出力はjson形式で 入力＝音声のテキストファイル　画像認識のテキストファイル（物体5候補、らしさ5,動作）
import csv
import json
import re
import sys
import math
import random

#csvファイルの辞書化
def Csv_to_dict(mycsv):
    mydict = []
    with open(mycsv,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mydict.append(row)
    return mydict

#yes/noの選択
def yes_no_input():
    while True:
        choice = input("どうしますか？ 'yes' = 雑談APIへ 'no' =  [y/N]: ").lower()
        if choice in ['y', 'ye', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False

#未知語の検出
def format_text(text):

    text=re.sub("これは", "", text)
    text=re.sub('です', "", text)
    text=re.sub("知ってますか","",text)
    text=re.sub(r'[!-~?]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字

    return text

#ルールマッチ======================================================================
def main(myspeech, mydict):
    #with open("api.json",encoding="UTF-8") as f:
        #myspeech = json.load(f)
    MIN = -10000.0
    #for h in myspeech:
    #    if(float(myspeech[h]["score"]) > float(MIN)):
    #        MIN = myspeech[h]["score"]
    #        sp = myspeech[h]["sentence"]
    sp = myspeech["sentence1"]["sentence"]
    #sp = "エルモ？"
    word = Csv_to_dict("rule_base/jisyo.csv")
    rule = Csv_to_dict("rule_base/rule2.csv")
    #print(word)
    #print(rule)
    print("===発話===")
    print(sp)
    #sp = sys.stdin.readline().rstrip()
    #print(sp)
    count = 0
    a = 0
    b = 0
    rule_count = 0
    for i in word:
        matchOB = re.search((i["tango"]),sp)
        if matchOB:
            print("===検出させた単語===")
            print(matchOB.group())
            for j in rule:
                if(j["NAME"] == ""):
                    pass
                else:

                    if re.match("{}".format(j["SPEECH"]),sp):
                        #with open("input_scene.json",encoding="UTF-8") as f:
                        #    mydict = json.load(f)
                        MAX = 0.0
                        result = {}
                        print("result")
                        for hoge in mydict:
                            for h in range(5):
                                if isinstance(mydict[hoge],dict):
                                    if (j["NAME"].format(matchOB.group()) == mydict[hoge]["object"][h]):
                                        if(float(mydict[hoge]["confidence"][h]) > float(MAX)):
                                            MAX = mydict[hoge]["confidence"][h]
                                            #print(MAX)
                                            #result = {}
                                            result["ID"] = "{}".format(hoge)
                                            result["RESPONSE"] = "{}".format(j["RESPONSE"]).format(matchOB.group())
                                            result["ORDER"] = "{}".format(j["ORDER"])
                                    #else:
                                        #result["ID"] = ""
                                        #result["RESPONSE"] = "{}は机の上にありません".format(matchOB.group())
                                        #result["ORDER"] = ""
                        if(result != {}):
                            print("===結果===")
                            print(result)
                            return result

                        if(result == {}):
                            result["ID"] = ""
                            result["RESPONSE"] = "{}は机の上にありません".format(matchOB.group())
                            result["ORDER"] = ""
                            print("===結果===")
                            print(result)
                            return result
                    else: #単語を検知してもルールにマッチしなかったとき
                        print("===結果===")
                        print("ルールにマッチしません")
                        print("=========")
                        #if yes_no_input():
                        if sp != "":
                            result = {}
                            result["input_txt"] = sp
                            result["ID"] = ""
                            result["RESPONSE"] = ""
                            result["ORDER"] = ""
                            print(result)
                            return result
                        else: #音声なし、
                            result = {}
                            print(result)
                            return result

        else:
            count += 1
#===============================================================================


    if(count == len(word)):
        #print("===検出された単語===")
        print("辞書にある単語はありません")
        for j in rule:
            rule_count += 1
            if(j["NAME"] == ""):
                if re.match("{}".format(j["SPEECH"]),sp):
                    #with open("input_scene.json",encoding="UTF-8") as f:
                    #    mydict = json.load(f)
                    MAX2 = 0
                    result3 = {}
                    if len(mydict) != 1:
                        if j["MOTION"] != "":
                            for hoge in mydict:
                                #for h in range(5):
                                ##dict(scene)のうしろに付いている骨格情報も for hoge ...で回してしまい
                                ##mydict[hoge]がfoalt型になる時があるのでifではじいている
                                if isinstance(mydict[hoge],dict):
                                    if j["MOTION"] == mydict[hoge]["motion"]:
                                        result3["ID"] = "{}".format(hoge)
                                        result3["RESPONSE"] = "{}".format(j["RESPONSE"]).format(mydict[hoge]["object"][0])
                                        result3["ORDER"] = "{}".format(j["ORDER"])
                                        #if(float(mydict[hoge]["confidence"][h]) > float(MAX2)):
                                            #MAX2 = mydict[hoge]["confidence"][h]
                                            #print(MAX)
                                            #result3 = {}
                                            #result3["ID"] = "{}".format(hoge)
                                            #result3["RESPONSE"] = "{}".format(j["RESPONSE"]).format(mydict[hoge]["object"][0])
                                            #result3["ORDER"] = "{}".format(j["ORDER"])

                            if(result3 != {}):
                                print("===結果===")
                                print(result3)
                                return result3

                            if(result3 == {} and sp != ""):
                                result3["ID"] = ""
                                result3["RESPONSE"] = "どれのことですか"
                                result3["ORDER"] = ""
                                print("===結果===")
                                print(result3)
                                return result3
                        else:
                            for hoge in mydict:
                                result3["RESPONCE"] = "{}".format(j["RESPONSE"]).format(mydict[hoge]["object"][0])
                                result3["ID"] = "{}".format(hoge)
                                result3["ORDER"] = "{}".format(j["ORDER"])
                            print("===結果===")
                            print(result3)
                            return result3
                    else:
                        for hoge in mydict:
                            result3["ID"] = "{}".format(hoge)
                            result3["RESPONSE"] = "{}".format(j["RESPONSE"]).format(mydict[hoge]["object"][0])
                            result3["ORDER"] = "{}".format(j["ORDER"])
                            print("===結果===")
                            print(result3)
                            return result3
                else:
                    a += 1
            else:
                a += 1

        #print(a)
        #print(b)

#===============================================================================
    if(rule_count == len(rule)):
        print("===結果===")
        print("単語にもルールにもマッチしません")
        print("=========")
        #if yes_no_input():
        if sp != "":
            result2 = {}
            result2["input_txt"] = sp
            result2["ID"] = ""
            result2["RESPONSE"] = ""
            result2["ORDER"] = ""
            print(result2)
            return result2
        else:
            #with open("jisyo.csv","a") as f:
                #writer = csv.writer(f)
                #writer.writerows(format_text(sp))
            result4 = {}
            #result4["ID"] = ""
            #result4["RESPONSE"] = "{}って何ですか".format(format_text(sp))
            #result4["ORDER"] = ""
            #print(format_text(sp))
            return result4

if __name__ == "__main__":
    main()
