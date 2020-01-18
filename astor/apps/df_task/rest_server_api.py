#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: li, guiying; Zhong, muyao

import requests, socket
import time, json
import sys
from datetime import datetime as dt
from threading import Thread
import argparse

site_url = 'http://10.20.95.219:34900'
start_test_api = '/user/command/start/'
config_test_api = '/user/upload/config'
stop_test_api = '/user/command/stop/'
job_query_test_api = '/user/query/running_task/'
clusterInfo_query_api = '/user/query/cluster_info'
jobList_query_api = '/user/query/task'

def post_config(json_config: str) -> str:
    """
    向服务端提交算法配置
    :param json_config: 配置模板，json.loads()类型
    :return: job config id
    """
    reply = requests.post(site_url + config_test_api, json=json.loads(json_config))
    reply = json.loads(reply.text)
    print(reply)
    assert reply['type'] == 'response'
    return reply['content']['msg_res']

def start_job(job_config_id: str) -> str:
    """
    开始运行任务
    :param job_config_id: 配置文件编号 (return from post_config(json_config: str))
    :return: job id
    """
    reply = requests.get(site_url + start_test_api + job_config_id)
    reply = json.loads(reply.text)
    assert reply['type'] == 'response'
    return reply['content']['msg_res']

def stop_job(job_id: str):
    """
    停止运行任务
    :param job_id: job name  (return from post_config(json_config: str))
    :return: None
    """
    t=Thread(target=requests.get, args=(site_url + stop_test_api + job_id,))
    t.start()

def query_job(job_id: str):
    """
    查询任务状态
    :param job_id: 任务名
    :return:
    """
    reply = requests.get(site_url + job_query_test_api + job_id)
    reply = json.loads(reply.text)
    return json.loads(reply['content']['msg_res'])['job_state']

def query_cluster():
    """
    查询集群信息
    :return:
    """
    reply = requests.get(site_url + clusterInfo_query_api)
    return reply.text

def query_job_list():
    reply = requests.get(site_url + jobList_query_api)
    return reply.text

if __name__ == "__main__":
    config_str = '''{
  "config_name" : "test_tsp_job3",
  "category" : "tsp",
  "data_path" : "",
  "time_out" : 1,
  "alg_info" : {
    "optimizer" : "ga",
    "opt_param" : {
      "pop_size" : 10,
      "iteration" : 400,
      "rand_seed" : 10
    },
    "alg_param" : {
    }
  },
  "resources" : {
    "task_roles" : ["master", "init", "ga_loop", "evaluator"],
    "task_replicas" : [1, 1, 1, 1],
    "cpu_requirement" : [1, 1, 1,  3],
    "gpu_requirement" : [0, 0, 0,  0],
    "memory_requirement" : [1,  1, 1, 1]
  }
}'''
    # config_id = post_config(config_str)
    # print(query_cluster())
    # print(config_id)
    # print(start_job(config_id))
    # print(query_job_list())
    # config_id = input("[*]
    print(query_job('test_tsp_job3_taskID_1569491267451'))
    stop_job('test_tsp_job3_taskID_1569491267451')
    print(query_job('test_tsp_job3_taskID_1569491267451'))
    # Input the uploaded config id:")
    # rb = requests.get(site_url + start_test_api + config_id)
    # print("The started job name is :", rb.text)
    # time.sleep(10)
    #
    # rc = requests.get(site_url + job_query_test_api + json.loads(rb.text)['content']['msg_res'])
    # rc_dict = json.loads(json.loads(rc.text)['content']['msg_res'])
    # #print(rc_dict,"type",type(rc_dict))
    # #print(json.loads(json.loads(rc.text)['content']['msg_res']))
    # while rc_dict['job_state'] != "RUNNING":
    #     rc = requests.get(site_url + job_query_test_api + json.loads(rb.text)['content']['msg_res'])
    #     rc_dict = json.loads(json.loads(rc.text)['content']['msg_res'])
    #     tmp_t = dt.now()
    #     sys.stdout.write(f"\r{tmp_t}==> Job state:{rc_dict['job_state']}")#
    #     sys.stdout.flush()






def test(test_type):
    if test_type == 'A':
        path = input('Input the path of the user config:(return to use the default "tsp_user.json")')
        if path == "":
            path = '../src/tsp_user.json'
        with open(path, 'r') as f:
            j = json.loads(f.read())
            ra = requests.post(site_url + config_test_api, json=j)
            print("Your config id is :", ra.text)
    elif test_type == 'B':
        config_id = input("[*] Input the uploaded config id:")
        rb = requests.get(site_url + start_test_api + config_id)
        print("The started job name is :", rb.text)
        time.sleep(10)

        rc = requests.get(site_url + job_query_test_api + json.loads(rb.text)['content']['msg_res'])
        rc_dict = json.loads(json.loads(rc.text)['content']['msg_res'])
        #print(rc_dict,"type",type(rc_dict))
        #print(json.loads(json.loads(rc.text)['content']['msg_res']))
        while rc_dict['job_state'] != "RUNNING":
            rc = requests.get(site_url + job_query_test_api + json.loads(rb.text)['content']['msg_res'])
            rc_dict = json.loads(json.loads(rc.text)['content']['msg_res'])
            tmp_t = dt.now()
            sys.stdout.write(f"\r{tmp_t}==> Job state:{rc_dict['job_state']}")#
            sys.stdout.flush()
    elif test_type == 'C':
        job_name = input("[*] Input the job you want to stop:")

        t=Thread(target=requests.get,args=(site_url + stop_test_api + job_name,))
        t.start()

        time.sleep(5)
        #rc = requests.get(site_url + stop_test_api + job_name)
        #print("Job stoped:", rc.text)
        #jn=json.loads(rc.text)['content']['msg_res']
        rc = requests.get(site_url + job_query_test_api + job_name)
        rc_dict=json.loads(json.loads(rc.text)['content']['msg_res'])
        while rc_dict['job_state'] != "STOPPED":
            rc = requests.get(site_url + job_query_test_api + job_name)
            rc_dict = json.loads(json.loads(rc.text)['content']['msg_res'])
            tmp_t = dt.now()
            sys.stdout.write(f"\r{tmp_t}==> Job state:{rc_dict['job_state']}")#
            sys.stdout.flush()
    elif test_type == 'D':
        job_name = input("[*] Input the job you want to query:")
        rc = requests.get(site_url + job_query_test_api + job_name)
        print("Job state:", rc.text)
    elif test_type == 'E':
        job_name = input("[*] The cluster info query [type Enter]")
        rc = requests.get(site_url + clusterInfo_query_api)
        print("Results:", rc.text)
    elif test_type == 'F':
        job_name = input("[*] The job list query [type Enter]")
        rc = requests.get(site_url + jobList_query_api)
        print("Results:{}".format(rc.text))
    else:
        print("Wrong test type.")
#
#
# if __name__ == "__main__":
#     parser=argparse.ArgumentParser()
#     parser.add_argument('--rest',type=str,default='http://127.0.0.1:5000',help='The ip and port of rest server.Example: http://127.0.0.1:5000')
#     args=parser.parse_args()
#     site_url =  args.rest
#     while True:
#         test_type = input("input the test type:[A/B/C/D/E/F]")
#         test(test_type)
