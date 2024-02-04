import json
import numpy as np
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy, crf_viterbi_accuracy
from keras.models import load_model
from collections import defaultdict
from project.albert_zh.extract_feature import BertVector
import re
import json
import tensorflow as tf
import requests
import csv
import pandas as pd
from py2neo import Graph, Node, Relationship
class Model:
    def __init__(self):
        self.sess = tf.keras.backend.get_session()
        self.graph = tf.get_default_graph()


    '''
    命名实体识别
    '''
    def get_entity(self,sent, tags_list):
        entity_dict = defaultdict(list)
        i = 0
        for char, tag in zip(sent, tags_list):
            if 'B-' in tag:
                entity = char
                j = i + 1
                entity_type = tag.split('-')[-1]
                while j < min(len(sent), len(tags_list)) and 'I-%s' % entity_type in tags_list[j]:
                    entity += sent[j]
                    j += 1
                entity_dict[entity_type].append(entity)
            i += 1
        return dict(entity_dict)

    def handle(self, text):
        event_type = "subtask1"
        MAX_SEQ_LEN = 128  # 输入的文本最大长度
        # 读取label2id字典
        with open("%s_label2id.json" % event_type, "r", encoding="utf-8") as h:
            label_id_dict = json.loads(h.read())
        id_label_dict = {v: k for k, v in label_id_dict.items()}
        # 利用ALBERT提取文本特征
        bert_model = BertVector(pooling_strategy="NONE", max_seq_len=MAX_SEQ_LEN)
        # 载入模型苦瓜干 市场走动不快，近期市场价格药用在21元左右，山东选片在28元左右，广西片在35元左右
        custom_objects = {'CRF': CRF, 'crf_loss': crf_loss, 'crf_viterbi_accuracy': crf_viterbi_accuracy}
        ner_model = load_model("%s_ner.h5" % event_type, custom_objects=custom_objects)
        f = lambda text: bert_model.encode([text])["encodes"][0]
        text = text.replace(' ', '')
        text = re.split('【.*?】', text)
        res = dict()
        for item in text:
            if len(item) > 0:
                # 利用训练好的模型进行预测
                train_x = np.array([f(item)])
                y = np.argmax(ner_model.predict(train_x), axis=2)
                y = [id_label_dict[_] for _ in y[0] if _]
                # 输出预测结果
                dic = self.get_entity(item, y)
                # 存入res
                for k, v in dic.items():
                    if k not in res:
                        res[k] = v
        return res
    '''
    实体链接，存入Node4j
    '''
    def nel(self,dic):
        knowledge = self.lis(dic)
        data = pd.DataFrame(data=knowledge)
        data.to_csv('input.csv', encoding='utf-8')
        # 连接本地 Neo4j 图数据库
        graph = Graph('http://localhost:7474', user='neo4j', password='yjb952178')
        graph.delete_all()
        # 构建知识图谱
        with open('input.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for item in reader:
                if reader.line_num == 1:  # 过滤掉第 1 列（0， 1， 2）
                    continue
                print("当前行数: ", reader.line_num, "当前内容: ", item)
                start_node = Node("姓名", name=item[1])
                end_node = Node("属性值", value=item[3])
                relation = Relationship(start_node, item[2], end_node)
                graph.merge(start_node, "姓名", "name")
                graph.merge(end_node, "属性值", "value")
                graph.merge(relation, "值", "属性")
        return data

    def lis(self,dic):
        res = list()
        name = None
        for k, v in dic.items():
            if (k == "药品"):
                name = v[0]
                print(name)
            else:
                for i in v:
                    res0 = list()
                    res0.append(name)
                    res0.append(str(k))
                    res0.append(str(i))
                    res.append(res0)
        return res
    '''
    调用ownThink，获得知识图谱
    '''
    def think(self,indexname):
        sess = requests.get('https://api.ownthink.com/kg/knowledge?entity=' + indexname)
        answer = sess.text
        answer = json.loads(answer)
        return answer['data'].get('avp')

    def resSolution(self,dic):
        res = dict()
        for k, v in dic.items():
            data = []
            for i in range(0, len(v)):
                try:
                    key = dict()
                    key0 = dict()
                    value = dict(self.think(v[i]))
                    if len(self.think(v[i])) > 0:
                        key[v[i]] = value
                        key0[v[i]] = key[v[i]]
                    else:
                        key0 = v[i]
                except:
                    key0 = v[i]
                data.append(key0)
            res[k] = data
        return res

    def lisOwn(self,dic):
        res = list()
        name = None
        for k, v in dic.items():
            if (k == "药品"):
                try:
                    for key, value in v[0].items():
                        name = key
                except:
                    name = v[0]
            else:
                for i in v:
                    try:
                        for key, value in i.items():
                            # print(name,k,key)
                            res0 = list()
                            res0.append(name)
                            res0.append(str(k))
                            res0.append(str(key))
                            res.append(res0)
                            for k0, v0 in value.items():
                                res0 = list()
                                res0.append(key)
                                res0.append(str(k0))
                                res0.append(str(v0))
                                res.append(res0)
                                # print(key,k0,v0)
                    except:
                        res0 = list()
                        res0.append(name)
                        res0.append(str(k))
                        res0.append(str(i))
                        res.append(res0)
                        pass
        return res

    def own(self,dic):
        knowledge = self.lisOwn(dic)
        data = pd.DataFrame(data=knowledge)
        data.to_csv('input.csv', encoding='utf-8')
        # 连接本地 Neo4j 图数据库
        graph = Graph('http://localhost:7474', user='neo4j', password='yjb952178')
        graph.delete_all()
        # 构建知识图谱
        with open('input.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for item in reader:
                if reader.line_num == 1:  # 过滤掉第 1 列（0， 1， 2）
                    continue
                print("当前行数: ", reader.line_num, "当前内容: ", item)
                start_node = Node("姓名", name=item[1])
                end_node = Node("属性值", value=item[3])
                relation = Relationship(start_node, item[2], end_node)
                graph.merge(start_node, "姓名", "name")
                graph.merge(end_node, "属性值", "value")
                graph.merge(relation, "值", "属性")
        return data