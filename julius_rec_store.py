# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

import json
import collections as cl
import sys
import datetime

def store(sentence, score, CM, word, k, count, Time):
    """
    sentence :音声認識結果の文字列（１文）
    score :尤度
    CM :単語信頼度
    word :単語ごとの文字列
    """


    sentence_list = ["sentence1", "sentence2", "sentence3", "sentence4", "sentence5", "sentence6", "sentence7", "sentence8", "sentence9", "sentence10"]

    '''データ等格納'''
    ys = cl.OrderedDict()#順番にデータ格納するため
    for i in range(len(sentence_list)):
        data = cl.OrderedDict()#順番にデータ格納するため
        data["sentence"] = sentence[i]
        data["score"] = score[i]
        data["word"] = word[i]
        data["CM"] = CM[i]


        ys[sentence_list[i]] = data #辞書型のデータ


    ys.update(Time)
    fs = open('./'+k+'_speech/'+k+'_'+str(count)+'_sentence.json','w')
    #fl = open(k+'sentence_log.json', 'a+')

    json.dump(ys,fs,indent=4,ensure_ascii=False)
    #json.dump(ys,fl,indent=4,ensure_ascii=False)
    return ys
    #indent がないと１行でJSONに書き込まれる（読みにくい）
    #ensure_ascii=False はJSONに書き込んだ時に文字化けしないように
