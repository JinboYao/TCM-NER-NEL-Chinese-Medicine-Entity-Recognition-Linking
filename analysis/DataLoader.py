import json
import numpy
import matplotlib
from matplotlib import pylab, mlab, pyplot
np = numpy
plt = pyplot
import jieba.analyse
from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs

from pylab import *
from numpy import *


def read_font():
    file = open('medical_ner_entities.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    f1 = open('F:\D数据\毕设\命名实体识别\medical.txt', 'w',encoding='utf-8')
    for i in s:
        s=i.get('text')
        #s0=re.sub(r'【.*?】','',s)
        print(s)
        f1.write(s+"\n")
    # print(is)

def medician_name():
    f2 = open('F:\D数据\毕设\命名实体识别\medical_name.txt', 'w', encoding='utf-8')
    file = open('medical_ner_entities.json', 'r', encoding='utf-8-sig')
    s = json.load(file)
    for i in s:
        print(i.get('annotations')[0].get('entity'))
        f2.write(i.get('annotations')[0].get('entity')+'\n')


def sys():
    path = 'F:\D数据\毕设\命名实体识别\medical_name.txt'
    file_in = open(path, 'r',encoding='utf-8')
    content = file_in.read()
    try:
        jieba.load_userdict("词典")  # 加载词典，补充默认词典
        jieba.analyse.set_stop_words('F:\D数据\毕设\命名实体识别\medical_name.txt')
        tags = jieba.analyse.extract_tags(content, topK=100, withWeight=True)
        for v, n in tags:
            # 权重是小数，为了凑整，乘了一万
            print(v + '\t' + str(float(n)))
    finally:
        file_in.close()



if __name__ == '__main__':
    # read_font()
    #medician_name()
    sys()