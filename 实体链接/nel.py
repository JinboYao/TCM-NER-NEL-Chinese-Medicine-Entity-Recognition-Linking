import  json
import csv
import pandas as pd
from py2neo import Graph, Node, Relationship

def lis(dic):
  res=list()
  name=None
  for k,v in dic.items():
    if(k=="药品"):
      name=v[0]
      print(name)
    else:
      for i in v:
        res0 = list()
        res0.append(name)
        res0.append(str(k))
        res0.append(str(i))
        res.append(res0)
  return res

if __name__ == '__main__':
  knowledge=lis(dic)
  print(knowledge)
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
