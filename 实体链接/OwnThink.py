import json
import requests
import  json
import csv
import pandas as pd
from py2neo import Graph, Node, Relationship

def think(indexname):
    sess = requests.get('https://api.ownthink.com/kg/knowledge?entity=' + indexname)
    answer = sess.text
    answer = json.loads(answer)
    return answer['data'].get('avp')

def resSolution(dic):
    res = dict()
    for k, v in dic.items():
        data = []
        for i in range(0, len(v)):
            try:
                key = dict()
                key0 = dict()
                value = dict(think(v[i]))
                if len(think(v[i])) > 0:
                    key[v[i]] = value
                    key0[v[i]] = key[v[i]]
                else:
                    key0 = v[i]
            except:
                key0 = v[i]
            data.append(key0)
        res[k] = data
    return res

def lisOwn(dic):
    res = list()
    name = None
    for k, v in dic.items():
        if (k == "药品"):
            try:
                for key, value in v[0].items():
                    name = key
            except:
                name=v[0]
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
                        for k0,v0 in value.items():
                            res0 = list()
                            res0.append(key)
                            res0.append(str(k0))
                            res0.append(str(v0))
                            res.append(res0)
                            # print(key,k0,v0)
                except:
                    res0=list()
                    res0.append(name)
                    res0.append(str(k))
                    res0.append(str(i))
                    res.append(res0)
                    pass
    return res


def own(dic):
    knowledge = lisOwn(dic)
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

if __name__ == '__main__':
    dic={
  "药品": [
    "乌鸡白凤丸"
  ],
  "药物成分": [
    "乌鸡",
    "鹿角胶",
    "鳖甲",
    "牡蛎",
    "桑螵蛸",
    "人参",
    "黄芪",
    "当归",
    "白芍",
    "香附",
    "天冬",
    "甘草",
    "地黄",
    "熟地黄",
    "川芎",
    "银柴胡",
    "丹参",
    "山药",
    "芡实",
    "鹿角霜",
    "蜂蜜"
  ],
  "药物剂型": [
    "小蜜丸"
  ],
  "药物性味": [
    "味甜",
    "微苦"
  ],
  "中药功效": [
    "补气养血",
    "调经止带"
  ],
  "症状": [
    "月经不调",
    "经期腹痛"
  ],
  "人群": [
    "孕妇"
  ]
}
    dic0=resSolution(dic)
    print(dic0)
    res=own(dic0)
    print(res)
