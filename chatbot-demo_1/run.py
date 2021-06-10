from ast import literal_eval
from flask import Flask, render_template, request, jsonify

import BankFAQbot

app = Flask(__name__)
message_recv = ''
message_send = ''

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send_message', methods=['GET'])
def send_message():
    global message_recv
    # message_get = ""

    message_recv = request.args['message']
    print("收到前端发过来的信息：%s" % message_recv)
    print("收到数据的类型为：" + str(type(message_recv)))

    
    print('message_get:'+message_recv)
    return message_recv


@app.route('/change_to_json', methods=['GET'])
def change_to_json():

    global message_recv
    print('message_send:'+ message_recv)
    # message_json = {
    #     # "message": message_send
    #     "message": '1234'
    # }
    message_send = BankFAQbot.string_find_fun(message_recv)
    print('message_json:'+str(jsonify(message_send)))
    return jsonify(message_send)


if __name__ == '__main__':
    app.debug = True
    app.run(
      host='0.0.0.0',
      port= 5001,
      debug=True
    )

