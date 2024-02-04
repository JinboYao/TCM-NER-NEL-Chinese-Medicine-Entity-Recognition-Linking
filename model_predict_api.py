# -*- coding: utf-8 -*-
from flask import Flask, request
import json
import tensorflow as tf
from project.model import Model
app = Flask(__name__)

@app.route("/nerApi", methods=["GET"])
def nerApi():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    get_data = request.args.to_dict()
    text = get_data.get('name').replace(' ', '')
    model = Model()
    sess = model.sess
    graph = model.graph
    with sess.as_default():
        with graph.as_default():
            init = tf.global_variables_initializer()
            sess.run(init)
            res = model.handle(text)
            # 对参数进行操作
            print(res)
            return_dict['result'] = res
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/nelApi", methods=["GET"])
def nelApi():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    get_data = request.args.to_dict()
    text = get_data.get('name').replace(' ', '')
    model = Model()
    sess = model.sess
    graph = model.graph
    with sess.as_default():
        with graph.as_default():
            init = tf.global_variables_initializer()
            sess.run(init)
            res = model.handle(text)
            # 对参数进行操作
            nelRes=model.nel(res)
            return_dict['result'] = "success"
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/ownApi", methods=["GET"])
def ownApi():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': "False"}
    get_data = request.args.to_dict()
    text = get_data.get('name').replace(' ', '')
    model = Model()
    sess = model.sess
    graph = model.graph
    with sess.as_default():
        with graph.as_default():
            init = tf.global_variables_initializer()
            sess.run(init)
            res = model.handle(text)
            # 对参数进行操作
            res0=model.resSolution(res)
            print(res0)
            res1=model.own(res0)
            print(res1)
            return_dict['result'] = "success"
    return json.dumps(return_dict, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)
