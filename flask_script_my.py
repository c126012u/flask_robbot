from flask import Flask,request,jsonify
import base64
import re
import sys
from rule_base import res7
import time
import threading
import json
import jtalk #OpenJTalk
import talk #talkAPI


#リクエストを受けたらscene.json（尤度と名前以外）を送るように書き換え
#参考： http://uokada.hatenablog.jp/entry/2012/11/10/002453

#server
app = Flask(__name__)

def convert_b64_to_file(b64,outfile_path):
    """
    b64をデコードしてファイルに書き込む
    """
    s = base64.decodestring(b64)
    with open(outfile_path,"wb") as f :
        f.write(s)

def rule_or_api():
    global speech
    global scene
    global trig
    global res
    global count
    global motion_count

    try:
        res = res7.main(speech, scene)
        print(speech)
        print(scene)

    except UnboundLocalError:
        time.sleep(0.1)
        print("UnboundLocalError")
        pass
    except TypeError:
        time.sleep(0.1)
        print("TypeError")
        pass
    except KeyError:
        time.sleep(0.1)
        print("KeyError")
        pass

    if res == {}: #音声なし、ルールマッチなし
        print("0.1秒待つ")
        time.sleep(0.1)
        #pass
    #音声なし、ルールマッチあり
    elif res["ID"]!="" and res["RESPONSE"]=="" and res["ORDER"]!="":
        print("ロボット")
        print(res)
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)

        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        motion_count = count
        #break
    elif res["RESPONSE"]==res["ID"]==res["ORDER"]=="":#音声有り、ルールマッチなし
        res["RESPONSE"] = talk.chat(res["input_txt"])
        print(res)
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)

        jtalk.say(res["RESPONSE"])
        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        motion_count = count
        #break
    #音声有り、ルールマッチあり
    else:
        #書き込み
        print(res)
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)
        jtalk.say(res["RESPONSE"])
        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        #break

@app.route("/")
def index():
    return "send me json hello "

#base64でエンコードされたjsonファイルをデコード
@app.route('/post_request', methods=['POST'])
def post_request():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している
    global count
    #jsonを取得
    data = request.json
    #keysを取得
    keys_array = list(data.keys())
    #valuesを取得
    values_array = list(data.values())
    """
    送ってくるjsonは一つ目の要素が{画像名:base64エンコード}としたもの
    """
    #f=open("ID_list.txt","w")
    #ske=open("sk.txt","w")

    #IDソート用のlist
    IDlist=[]
    #depth用のlist
    depthlist=[]
    xmin=[]
    xmax=[]
    ymin=[]
    ymax=[]
    skeleton = {}
    #keys_arrayにあるkeyリストをひとつひとつ見ていく
    #f.write("ID\tPointing\tXmax\tYmax\tXmin\tYmin\tDepth\n-------------------------------------------------------------\n")
    for key_index in range(len(keys_array)):

        """
        ここでJSONkeyの場合分けをしている
        """

        #画像だった場合
        if re.search("Objects",keys_array[key_index]):
            object_list = []
            confidence_list = []
            '''
            object_list[0]:ID1の物体名N-best
            object_list[1]:ID2の物体名N-best
            ...
            confidence_list[0]~も同様
            '''
            #画像の保存名
            save_name = keys_array[key_index] + ".jpg"
            #コンバート
            convert_b64_to_file(bytes(values_array[key_index],"utf-8"),save_name)

            object_list.append(["エルモ","箱","ねこ","犬","トトロ"])

            confidence_list.append([60.0,20.0,17.0,15.0,10.0])

            '''
            切り出し画像を、物体認識プログラムへ入力
            ここで物体辞書を用意?
            出力　name=[エルモ,トトロ,ねこ...]
                 confidence = [,,,...]
            '''
            object_list.append(name)
            confidence_list.append(confidence)
        #ID番号が入っている場合
        elif re.search("ObjectID",keys_array[key_index]):
            #IDlistに追加
            IDlist.append(int(keys_array[key_index][0]))
            #ソート
            IDlist=sorted(IDlist)
        elif re.search("ObjectDepth",keys_array[key_index]):
            depthlist.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("Pointing",keys_array[key_index]):
            point=int(keys_array[key_index][0])
        elif re.search("Sk",keys_array[key_index]):
            #ske.write(str(keys_array[key_index])+" "+str(values_array[key_index])+"\n")
            skeleton[str(keys_array[key_index])] = values_array[key_index]
        elif re.search("Xmax",keys_array[key_index]):
            xmax.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("Xmin",keys_array[key_index]):
            xmin.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("Ymax",keys_array[key_index]):
            ymax.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("Ymin",keys_array[key_index]):
            ymin.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        #それ以外の場合は空文字を表示
        else:
            print("",end="")


        
    #ここに関しては即興
    #file_str=""
    '''データ等格納'''
    x_y_list = []
    scene = cl.OrderedDict()#順番にデータ格納するため
    for i in IDlist:
        #f.write(str(i)+"\t")
        data = cl.OrderedDict()#順番にデータ格納するため
        if i == point:
            data["motion"] = "POINTING"
            #f.write("pointing\t")
        else:
            data["motion"] = ""
            #f.write("\t\t")
        for j in xmax:
            if j[0] == i:
                x_y_list.append(j[1])
                #f.write(str(j[1])+"\t")
        for j in ymax:
            if j[0] == i:
                x_y_list.append(j[1])
                #f.write(str(j[1])+"\t")
        for j in xmin:
            if j[0] == i:
                x_y_list.append(j[1])
                #f.write(str(j[1])+"\t")
        for j in ymin:
            if j[0] == i:
                x_y_list.append(j[1])
                #f.write(str(j[1])+"\t")
        x = (x_y_list[0] - x_y_list[2])/2.0 + x_y_list[2]
        y = (x_y_list[1] - x_y_list[3])/2.0 + x_y_list[3]

        for j in depthlist:
            if j[0] == i:
                data["location"] = [x, y, j[1]]
                #f.write(str(j[1])+"\t")
        data["object"] = object_list[i]
        data["confidence"] = confidence_list[i]
        scene[IDlist[i]] = data #辞書型のデータ

    ###
    #global scene
    scene.update(skeleton)

    fs = open('scene'+str(count)+'.json','w')
    #fl = open('scene_log.json', 'a+')
    count += 1
    json.dump(scene,fs,indent=4,ensure_ascii=False)
    #json.dump(scene,fl,indent=4,ensure_ascii=False)

    #sceneをルールマッチへ
    rule_or_api()

    return jsonify(res='success', **data)

##発話の認識結果のjsonを保存する
@app.route('/chat', methods=['POST'])
def post_request_chat():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している

    #jsonを取得
    global speech
    speech = request.json
    print(speech)
    rule_or_api()
    #global trig
    #trig = ""
    return jsonify(res='success', **speech)

@app.route('/scene_test', methods=['POST'])
def post_request_scene_test():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している

    #jsonを取得
    global scene
    scene = request.json
    print(scene)
    rule_or_api()
    #global trig
    #trig = ""
    return jsonify(res='success', **scene)

if __name__ == "__main__":
    count = 0
    #app.run(host = "163.225.223.101")
    speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
    scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
    res = {}

    #while trig == "\n":
        #thread = threading.Thread(target=rule_or_api)
        #thread.start()
    print("認識開始")
    #trig = sys.stdin.readline()
    app.debug = True
    app.run(host = "0.0.0.0",threaded=True)
