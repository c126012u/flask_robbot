# -*- coding: utf-8 -*-
import pya3rt
'''
$ pip install pya3rt
ネットに接続していないと動かない
'''
import sys

def chat(text):
       apikey = "8auKLi5BoSFKoBkIPPgji1bNwD3MukyQ"
       client = pya3rt.TalkClient(apikey)

       AI = client.talk(text)

       if AI['message'] != 'ok': #okのときmessageが返ってくる、それ以外は何らかのエラー
          #f.write("[" + AI['message'] + "]\n")
          return ""
       else:
          #f.write(out_t+AI['results'][0]['reply']+"\n")
          return AI['results'][0]['reply']


def main():

      while True:

          intext = sys.stdin.readline()  #標準入力

          res = chat(intext)



if __name__ == '__main__':
       main()
