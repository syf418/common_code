# @Time: 2020/3/10 9:36
import warnings
warnings.filterwarnings(action='ignore')

import pandas as pd
import os
import base64
from flask import Flask, jsonify, request, abort, redirect
import traceback
import getopt
import sys
import time
import shutil

from utils import logUtils
from config_class import Config_module
from utils.fileUtils import deleteFolderFiles

# 配置区
PORT = 9400

def dirs_check(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_to_local(path, items):
    items = bytes(items, encoding="utf-8")
    with open(path, "wb") as f:
        f.write(items)

def obj_to_nums(df, cols):
    for col in cols:
        if df[col].dtype != object:
            pass
        else:
            df[col] = df[col].apply(lambda x: float(x) if x.replace(".", "").isdigit() else x)
    return df

def read_data(path):
    try:
        data = pd.read_csv(path).to_json(orient="split",force_ascii=False)
    except:
        data = pd.read_csv(path, encoding='gbk').to_json(orient="split",force_ascii=False)
    return data

def delete_dirs(dirs):
    try:
        shutil.rmtree(dirs)
    except Exception as e:
        print("CLEARN Error %s" % (e), flush=True)

app = Flask(__name__)
@app.route('/roadrun', methods=['POST'])
def roadrun():
    err_msg = None
    code = 0
    # 获取时间戳作为唯一标识
    unix_time = str(int(time.time()))
    try:
        if not request.json or "xxx" not in request.json:
            redirect(request.url)
        f = request.json

        # 多sheet excel数据
        f_sheet1 = f["Data_topology"]
        f_sheet2 = f["Data_attributes"]

        # get name and file
        BranchName = f["BranchFile"][0]
        BranchFile = f["BranchFile"][1]

        # save
        save_to_local(input_path + "Data_topology.csv", f_sheet1)
        save_to_local(input_path + "Data_attributes.csv", f_sheet2)
        save_to_local(input_path + "{}.csv".format(BranchName), BranchFile)

        # merge
        df_sheet1 = pd.read_csv(input_path + "Data_topology.csv")
        df_sheet2 = pd.read_csv(input_path + "Data_attributes.csv")

        # excel 多sheet写入
        writer = pd.ExcelWriter(input_path + "GraphData.xls")
        df_sheet1.to_excel(excel_writer=writer, sheet_name='Data_topology', index=False)
        df_sheet2.to_excel(excel_writer=writer, sheet_name='Data_attributes', index=False)
        writer.save()
        writer.close()

        # -----------------  part 2 ----------------
        # modify config
        Config = Config_module(
            GraphDataFile= "GraphData.xls"
            , BranchFile= BranchName + ".csv"
            , CircleFile= CircleName + ".csv"
            , SaggingFile= SaggingName + ".csv"
            , distanceMax= maxDistance
            , OutFileFolder= outputPath + "_{}{}".format(unix_time, os.sep)
            , UniqueID = unix_time)
        outpath = Config.OutFileFolder

        # -----------------  part 3 ----------------
        # main
        from roadRunMain import main_run

        logUtils.print_info("====运行开始===")
        main_run(Config)
        logUtils.print_info("====运行结束===")

        # 读取结果接口返回
        data1 = read_data(outpath + "out_add_del_edge_data.csv")
        data2 = read_data(outpath + "df_graph_circle.csv")
        data3 = read_data(outpath + "df_graph_connect.csv")
        data4 = read_data(outpath + "out_before_info_data.csv")
        data5 = read_data(outpath + "out_after_info_data.csv")
        data6 = read_data(outpath + "out_path_fp_data.csv")

        # 清理文件
        delete_dirs(Config.InFileFolder)
        delete_dirs(Config.tempFileFolder)
        delete_dirs(Config.OutFileFolder)

    except Exception as e:
        logUtils.print_error("运行异常：", e)
        traceback.print_exc()
        code = -1
        err_msg = str(e)
    if err_msg is None:
        result = {"code": code,
                  "err_msg": "succeed!",
                  "out_add_del_edge_data": data1,
                  "df_graph_circle": data2,
                  "df_graph_connect": data3,
                  "out_before_info_data": data4,
                  "out_after_info_data": data5,
                  "out_path_fp_data": data6}
    else:
        result = {"code": code,
                  "err_msg": err_msg,
                  "out_add_del_edge_data": data1,
                  "df_graph_circle": data2,
                  "df_graph_connect": data3,
                  "out_before_info_data": data4,
                  "out_after_info_data": data5,
                  "out_path_fp_data": data6}

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