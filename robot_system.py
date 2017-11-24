from flask import Flask,request,jsonify
import base64
import re
import sys
from rule_base import rule_base
import time
import json
import jtalk #OpenJTalk
import talk #talkAPI
import copy
import logging
#import cv2

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
    global K1scene
    global res
    global count

    res = rule_base.main(speech, K1scene)
    print(K1scene)
    #print("scene:",K1scene)

    if res == {}: #音声なし、ルールマッチなし
        print("0.1秒待つ")
        time.sleep(0.1)
        #pass
    #音声なし、ルールマッチあり
    elif res["ID"]!="" and res["RESPONSE"]=="" and res["ORDER"]!="":
        print("ロボット")
        print("res",res)
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)

        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        K1scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        point_keep = 0
        K1_object_list = []
        K1_confidence_list = []


    elif res["RESPONSE"]==res["ID"]==res["ORDER"]=="":#音声有り、ルールマッチなし
        res["RESPONSE"] = talk.chat(res["input_txt"])
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)
        print("API:",res["RESPONSE"])
        jtalk.say(res["RESPONSE"])
        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        K1scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        point_keep = 0
        K1_object_list = []
        K1_confidence_list = []

    #音声有り、ルールマッチあり
    else:
        #書き込み
        with open('res.json','w') as fw:
            json.dump(res, fw, indent=4,ensure_ascii=False)
        jtalk.say(res["RESPONSE"])
        #trig = "" ##認識開始前にもどる
        speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
        K1scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
        res = {}
        point_keep = 0
        K1_object_list = []
        K1_confidence_list = []


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
    global K1scene
    global count
    global K1_object_list
    global K1_confidence_list
    global point_keep #指差し情報保持

    test_count = 0
    #jsonを取得
    data = request.json
    #keysを取得
    keys_array = list(data.keys())
    #valuesを取得
    values_array = list(data.values())
    """
    送ってくるjsonは一つ目の要素が{画像名:base64エンコード}としたもの
    """
    K1IDlist=[]
    #depth用のlist
    K1depthlist=[]
    K1center=[]
    K1sk={}
    pointK1 = 0
    #keys_arrayにあるkeyリストをひとつひとつ見ていく
    for key_index in range(len(keys_array)):
        #key_index は　0,1,2...

        """
        ここでJSONkeyの場合分けをしている
        """

        #画像だった場合
        if re.search("K1_Objects",keys_array[key_index]):
            '''
            K1_object_list = [[ID, [エルモ,トトロ,ねこ...]],
                              [ID, [ピカチュウ,コップ,ねこ...]]]
            confidence_listも同様
            '''
            #画像の保存名
            save_name = "./K1fig/"+keys_array[key_index] + ".jpg"
            #コンバート
            convert_b64_to_file(bytes(values_array[key_index],"utf-8"),save_name)
            """
            画像表示
            windowName = keys_array[key_index]
            cv2.namedWindow(windowName)
            img = cv2.imread("./K1fig/"+keys_array[key_index] + ".jpg")
            if img is None:
                print("can not read file")
                sys.exit()
            cv2.imshow(windowName,img)
            cv2.waitKey(1)
            """

            '''
            切り出し画像を、物体認識プログラムへ入力
            '''

            """決め打ち"""
            #ピカチュウ、エルモ、トトロ
            name = [["ピカチュウ","トトロ","コップ","金魚","箱"],["エルモ","トトロ","コップ","金魚","ピカチュウ"],["トトロ","ピカチュウ","コップ","金魚","エルモ"]]
            confidence = [50.0, 20.0, 11.0, 10.0, 9.0]

            K1_object_list.append([int(keys_array[key_index][0]),name[test_count]])
            K1_confidence_list.append([int(keys_array[key_index][0]),confidence])
            test_count += 1

        #ID番号が入っている場合
        elif re.search("K1_ObjectID",keys_array[key_index]):
            #IDlistに追加
            K1IDlist.append(int(keys_array[key_index][0]))
            ##int(keys_array[key_index][0])はID番号が入る
            ##"1_K1_ObjectID"の最初の文字の"1"
            #ソート
            K1IDlist=sorted(K1IDlist)
            """　試し"""
            name = [["ピカチュウ","トトロ","コップ","金魚","箱"],["エルモ","トトロ","コップ","金魚","ピカチュウ"],["トトロ","ピカチュウ","コップ","金魚","エルモ"]]
            confidence = [50.0, 20.0, 11.0, 10.0, 9.0]

            K1_object_list.append([int(keys_array[key_index][0]),name[len(K1IDlist)-1]])
            K1_confidence_list.append([int(keys_array[key_index][0]),confidence])

        elif re.search("K1_ObjectDepth",keys_array[key_index]):
            K1depthlist.append([int(keys_array[key_index][0]),int(values_array[key_index])])
        elif re.search("Pointing_K1",keys_array[key_index]):
            if int(values_array[key_index]) == 1:
                pointK1=int(keys_array[key_index][0])
                point_keep = int(keys_array[key_index][0])

        elif re.search("K1_Sk",keys_array[key_index]):
            #K1sk.append([str(keys_array[key_index]),float(values_array[key_index])])
            #→["K1_SkLeftHand_X","0.000000"]
            K1sk[str(keys_array[key_index])]=float(values_array[key_index])
        elif re.search("K1_Center",keys_array[key_index]):
            if keys_array[key_index][-1] == "X":
                lflag = 0
            else:
                lflag = 1
            K1center.append([lflag,int(keys_array[key_index][0]),int(values_array[key_index])])
        #それ以外の場合は空文字を表示
        else:
            print("",end="")
    #K1scene = cl.OrderedDict()#順番にデータ格納するため
    #K1data = cl.OrderedDict()#順番にデータ格納するため
    K1scene = {}
    K1data = {}
    for i in K1IDlist:
        #if i == pointK1:
        if i == pointK1 or point_keep == i:
            K1data["motion"] = "POINTING"

        elif i != pointK1 :
            K1data["motion"] = ""

        for name in K1_object_list:
            if i == name[0]:
                K1data["object"] = name[1]
        for conf in K1_confidence_list:
            if i == conf[0]:
                K1data["confidence"] = conf[1]
        center = []
        for k in range(len(K1IDlist)):
            center.append([float("inf"),float("inf"),float("inf")])

        tempcount=0
        tempID = 0
        for j in K1center:
            if tempcount == 2:
                # center.append([float("inf"),float("inf"),float("inf")])
                tempID+=1
                tempcount=1
            else:
                tempcount+=1
            if j[0] == 0:
                center[tempID][0]=j[2]
            else:
                center[tempID][1]=j[2]

        for dep in K1depthlist:
            if dep[0] == i:
                center[dep[0]-1][2]=dep[1]

        K1data["location"] = center[i-1]
            # if j[1] == i:
            #     if j[0] == 0:
            #         center.append(["X",j[2]])
            #     else:
            #         center.append(["Y",j[2]])

        # for j in K1depthlist:
            # if j[1] == i:
                # K1data["location"] = center.append(j[1])
                # K1data["location"] =
                #f.write(str(j[1])+"\t")
        #K1data["object"] = K1_object_list[i-1]
        #K1data["confidence"] = K1_confidence_list[i-1]
        # K1scene[str(i)] = K1data #辞書型のデータ
        """
        辞書型のDeep Copy
        """
        K1scene[str(i)] = copy.deepcopy(K1data)
    #print('scene',K1scene)
    K1scene.update(K1sk)

    K1_f = open('./K1_scene/K1scene'+str(count)+'.json','w')
    count += 1
    #fl = open('scene_log.json', 'a+')
    json.dump(K1scene,K1_f,indent=4,ensure_ascii=False)

    #sceneをルールマッチへ
    rule_or_api()

    return jsonify(res='success', **data)

##発話の認識結果のjsonを保存する
@app.route('/K1chat', methods=['POST'])
def post_request_chat():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    ###jsonはdict型なので即変換できないからlistに入れて処理している

    #jsonを取得
    global speech
    global K1scene
    speech = request.json
    #print(speech)
    rule_or_api()

    return jsonify(res='success', **speech)


if __name__ == "__main__":
    count = 0
    #app.run(host = "163.225.223.101")
    speech = {'sentence1': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence2': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence3': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence4': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence5': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence6': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence7': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence8': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence9': {'sentence': '', 'score': '0', 'word': [], 'CM': []}, 'sentence10': {'sentence': '', 'score': '0', 'word': [], 'CM': []}}
    K1scene = {'':{'location':[],'motion':'','name':[],'confidence':[]} }
    res = {}
    point_keep = 0
    K1_object_list = []
    K1_confidence_list = []

    #while trig == "\n":
        #thread = threading.Thread(target=rule_or_api)
        #thread.start()
    #trig = sys.stdin.readline()
    app.debug = True
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')#error以外は表示しない
    log.setLevel(logging.ERROR)
    app.run(host = "127.0.0.1")
