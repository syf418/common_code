# -*- coding: utf-8 -*-
# @Time: 2020/3/10 9:36
import warnings
warnings.filterwarnings(action='ignore')

import os
from flask import Flask, jsonify, request, redirect
import traceback
import getopt
import sys

# 配置区
PORT = 8400

app = Flask(__name__)
@app.route('/docker_demo', methods=['POST'])
def roadrun():
    err_msg = None
    code = 0
    try:
        if not request.json:
            redirect(request.url)

    except Exception as e:
        traceback.print_exc()
        code = -1
        err_msg = str(e)
    if err_msg is None:
        result = {"code": code,
                  "err_msg": "succeed!"
                  }
    else:
        result = {"code": code,
                  "err_msg": err_msg
                 }

    return jsonify(result)

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hp:",["port="])
    for opt, arg in opts:
        if opt == "-h":
            print("%s [-p <port>]" % os.path.basename(sys.argv[0]))
            sys.exit()
        elif opt in ("-p", "--port"):
            PORT = arg
    app.run(host="0.0.0.0", port=PORT, threaded=True)