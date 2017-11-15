#参考 https://kledgeb.blogspot.jp/2014/05/ubuntu-open-jtalk-1-open-jtalkopen-jtalk.html

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import wave
#import pyaudio

def jtalk(t):
       open_jtalk=['open_jtalk']
       #mech=['-x','open_jtalk-1.08/mecab-naist-jdic']
       mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
       htsvoice=['-m','MMDAgent_Example-1.4/Voice/mei/mei_normal.htsvoice']
       speed=['-r','1.0']
       outwav=['-ow','open_jtalk.wav']
       cmd=open_jtalk+mech+htsvoice+speed+outwav

       c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
       c.communicate(t)
       c.stdin.close()
       c.wait()
       aplay = ['aplay','-q','open_jtalk.wav']
       wr = subprocess.Popen(aplay)

def say(text):

       jtalk(text.encode('utf-8'))


if __name__ == '__main__':
       text = sys.argv[1]
       say(text) #音声ファイル生成
       #audio()
