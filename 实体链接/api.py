from flask import Flask, request
from project import model_predict_api as pro
import json

app = Flask(__name__)


# 只接受get方法访问
@app.route("/test_1.0", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的params参数
    get_data = request.args.to_dict()
    name = get_data.get('name')
    # age = get_data.get('age')
    # 对参数进行操作
    return_dict['result'] = tt(name)

    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt(name):
    result_str = pro.main(name)
    return result_str


if __name__ == "__main__":
    app.run(debug=True)