# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import socket
import re
import sys
import julius_rec_store as js
import urllib.request, json
import base64
import collections as cl
import datetime
import time

#speech.jsonを保存できたらサーバへ送信
'''
$python julius.py port
 port はポート番号
 portが10500のとき、K1_speech.json
 portが10530のとき、K2_speech.json
'''

def main():

    port = int(sys.argv[1])
    if port == 10500:
        k = "K1"
    elif port == 10530:
        k = "K2"
    host = "localhost"
    #port = 10530
    bufsize = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    count = 0
    #待機コマンド
    ##sock.send(b'PAUSE\n')

    #再開コマンド
    ##sock.send(b'RESUME\n')
    while True: #recv_data を受け取ってない時のループ、このループがないと１回の結果受け取りでプログラムが終了する
        sentence_data = [] #１０個の文字列格納
        score_data = [] #１０個の尤度格納
        matchs = [] #１つの文字列取り出し
        CM= [] #1つの単語信頼度取り出し
        CM_list = [] #単語信頼度リスト
        word_list = [] #単語ごとに文字列をリストに入れる
        start = ''
        end = ''
        while True:

            '''juliusの音声認識受け取り'''
            recv_data = sock.recv(bufsize)


            #recv_data = recv_data.encode("utf-8")
            recv_data = recv_data.decode("utf-8")
            ##クライアント側：UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe3 in position 4095: unexpected end of data
            ##サーバ側:とくにエラー無し
            ##このエラーがたまに出る（プログラムが終了してしまう）
            #t = datetime.datetime.today()
            #print(t.hour, ":", t.minute, ":", t.second, ":", t.microsecond, "マイクロ秒")
            #print('--------\n'+recv_data+'--------\n')
            #Error: module_send:: Connection reset by peer

            ##recv の中にINPUT STATUS="STARTREC"が来たら音声開始
            ##参考　：https://julius.osdn.jp/juliusbook/ja/desc_module.html
            #recv で開始時間と終了時間が同時に送られてくるなら
            #音声時間を計算して、終了のみフラグを立てる

            #音声開始時刻を取得
            pattern = r'"STARTREC" TIME="(.*?)"'
            start_time = re.findall(pattern, recv_data)
            if start_time != []:
                print(int(start_time[0]))
                start_time = datetime.datetime.fromtimestamp(int(start_time[0])).strftime('%H:%M:%S')

            #音声終了時刻を取得
            pattern = r'"ENDREC" TIME="(.*?)"'
            end_time = re.findall(pattern, recv_data)
            if end_time != []:
                print(int(end_time[0]))
                end_time = datetime.datetime.fromtimestamp(int(end_time[0])).strftime('%H:%M:%S')

                Time = {'start_time':start_time,'end_time':end_time}

            ###
            #with open('julius_2.log', mode='+a') as a_file:
            #    a_file.write('--------\n'+recv_data+'--------\n')#juliusの認識結果全部をファイルに書き込み

            with open('julius_N.log', mode='w') as a_file:
                a_file.write(recv_data)#juliusの認識結果全部をファイルに書き込み

            '''一行ごとに読み込み'''
            with open('julius_N.log', 'r') as f:
                recv_line = f.readlines()

            '''認識結果の取り出し（1行毎）'''
            for i in range(len(recv_line)):
                '''文字列（1文）取り出し'''
                pattern = r'WORD="(.*?)"'
                match = re.findall(pattern, recv_line[i])
                matchs = matchs + match
                moji = "".join(matchs)

                '''単語信頼度'''
                pattern2 = r'CM="(.*)"'
                data = re.findall(pattern2, recv_line[i])
                CM += data

                #単語ごとに文字を取り出すと最初と最後の要素が ""になる
                #単語が ""のとき信頼度は1になる
                #そのままだと ["", "りんご", "を", "食べる", ""] と言った形になるので
                #抜き出した単語ごとの文字列のリストから最初と最後の要素を消す
                #単語信頼度のリストも同様
                if "</SHYPO>" in recv_line[i]:
                    del matchs[0]
                    del matchs[len(matchs)-1]
                    del CM[0]
                    del CM[len(CM)-1]

                    CM_list.append(CM)
                    word_list.append(matchs)
                    CM = []

                    sentence_data.append(moji)
                    moji = ""
                    matchs = []

            '''尤度取り出し（juliusの結果全体から）'''
            pattern3 = r'SCORE="(.*)"'
            data = re.findall(pattern3, recv_data)
            if len(data) != 0:

                score_data += data

            if "</RECOGOUT>" in recv_data:
                break

        '''JSONファイルに書き込み'''
        obj = js.store(sentence_data, score_data, CM_list, word_list, k, count, Time)
        count += 1
        """speech.jsonを送る"""
        #url = "http://163.225.223.111:5000/"+k+"chat"

        if k == "K1":
            url = "http://127.0.0.1:5000/K1chat"
        if k == "K2":
            url = "http://127.0.0.1:5000/K2chat"

        method = "POST"
        headers = {"Content-Type" : "application/json"}
        json_data = json.dumps(obj).encode("utf-8")
        # httpリクエストを準備してPOST
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")

    #return obj

if __name__ == '__main__':
    main()
