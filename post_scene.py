import urllib.request, json
import base64

def convert_b64(file_path):
    """
    b64にエンコード
    """
    return base64.encodestring(open(file_path, 'rb').read()).decode("utf-8")

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/post_request"
    #url = "http://127.0.0.1:5000/K1chat"
    image = "test.jpg"
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    #value = convert_b64(image)
    # PythonオブジェクトをJSONに変換する
    #obj = {"image0" : value}
    #obj = {'sentence1':{'sentence':'エルモ嫌い？','score':'-9615.755859','word': ['エルモ', '特権', '。']},'sentence2':{'sentence':'エルモとって。','score':'-9621.711914','word':['エルモ','と','って','。']},'sentence3':{'sentence':'エルモとって。','score':'-9621.742188','word':['エルモ', 'と', 'って', '。']}, 'sentence4': {'sentence': 'エルモとって？', 'score': '-9623.018555', 'word': ['エルモ', 'と', 'って', '？']},'sentence5':{'sentence':'エルモとって？','score':'-9623.049805','word':['エルモ','と','って','？']},'sentence6':{'sentence':'エルモ通って。','score':'-9623.997070','word':['エルモ','通っ','て', '。']},'sentence7': {'sentence': 'エルモとって。', 'score': '-9625.153320', 'word': ['エルモ', 'と', 'って', '。']},'sentence8':{'sentence': 'エルモ等って。','score':'-9625.697266','word': ['エルモ','等','って', '。']}, 'sentence9': {'sentence': 'エルモって？','score':'-9626.460938','word':['エルモ','って','？'],'CM':['0.498','0.055','0.337','0.049']},'sentence10': {'sentence': 'エルモ等って？', 'score': '-9627.003906', 'word': ['エルモ', '等', 'って', '？']},'start_time': '04:33:57', 'end_time': '04:33:57'}
    obj = {"1_K1_CenterX":"602","1_K1_CenterY":"634","1_K1_ObjectID":"1","1_K1_ObjectPoint":"1005","1_Pointing_K1":"0","2_K1_CenterX":"913","2_K1_CenterY":"666","2_K1_ObjectID":"2","2_K1_ObjectPoint":"878","2_Pointing_K1":"0","K1_SkHead_X":"0.000000","K1_SkHead_Y":"0.000000","K1_SkLeftElbow_X":"0.000000","K1_SkLeftElbow_Y":"0.000000","K1_SkLeftHand_X":"0.000000","K1_SkLeftHand_Y":"0.000000","K1_SkLeftShoulder_X":"0.000000","K1_SkLeftShoulder_Y":"0.000000","K1_SkNeck_X":"0.000000","K1_SkNeck_Y":"0.000000","K1_SkRightElbow_X":"0.000000","K1_SkRightElbow_Y":"0.000000","K1_SkRightHand_X":"0.000000","K1_SkRightHand_Y":"0.000000","K1_SkRightShoulder_X":"0.000000","K1_SkRightShoulder_Y":"0.000000"}

    json_data = json.dumps(obj).encode("utf-8")
    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
