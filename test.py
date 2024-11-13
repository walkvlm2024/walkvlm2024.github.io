import yaml
import numpy as np
import pickle
import os,random, time
from threading import Timer
import ipdb
import sys
import requests, re
import shutil

# 加载参数
def get_config(path_opt="utils_dir/config.yaml"):
    with open(path_opt, 'rb') as handle:
        options = yaml.load(handle,Loader = yaml.FullLoader)
    return options

def get_time_diff(ddl_time):
    """
    格式化时间差
    :param time1: 2023-02-15 23:59:59
    :param time2: 2024-08-17 23:59:59
    :return: diff s
    """
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    start_time = time.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
    end_time = time.strptime(ddl_time, "%Y-%m-%d %H:%M:%S")

    time_diff = time.mktime(end_time) - time.mktime(start_time)
    return time_diff


def get_ccf_ddl(path_opt='config_dir/allconf.yml', map_opt='config_dir/types.yml'):

    map_opt_infos = get_config(map_opt)
    map_sub_name = {}
    for info in map_opt_infos:
        map_sub_name[info['sub']] = info['name']


    ddl_src_infos = get_config(path_opt)
    confs = []
    for conf in ddl_src_infos:
        title = conf['title']
        description = conf['description']
        sub = conf['sub']
        ccf = conf['rank']['ccf']
        ddl = conf['confs'][-1]['timeline']
        try:
            for conf_single in ddl:
                deadline = conf_single['deadline']
                time_diff = get_time_diff(conf_single['deadline'])

                if 'comment' in conf_single.keys():
                    comment = conf_single['comment']
                else:
                    comment = ''

                confs.append({
                        'title': title,
                        'description': description,
                        'sub': sub,
                        'sub_name': map_sub_name[sub],
                        'ccf': ccf,
                        'deadline': deadline,
                        'time_diff': time_diff,
                        'comment': comment,
                })

                # if time_diff > 0:
                #     not_due_conf.append({
                #         'title': title,
                #         'description': description,
                #         'sub': sub,
                #         'sub_name': map_sub_name[sub],
                #         'ccf': ccf,
                #         'deadline': deadline,
                #         'time_diff': time_diff,
                #         'comment': comment,
                #         'due': 0
                #     })
                # else:
                #     due_conf.append({
                #         'title': title,
                #         'description': description,
                #         'sub': sub,
                #         'sub_name': map_sub_name[sub],
                #         'ccf': ccf,
                #         'deadline': deadline,
                #         # 'time_diff': time_diff,
                #         'comment': comment,
                #         # 'due': 1
                #     })
        except Exception as e:
            # print(conf)
            # print(e)
            # exit()
            pass

    # sort
    confs.sort(key=lambda x: x['time_diff'])

    # 建立索引
    maps = {}
    results = {}
    for idx, conf in enumerate(confs):
        if conf['title'] not in results:
            k = conf['title']
            maps[k] = 1
        else:
            k = f"{conf['title']}_{maps[conf['title']]}"
            maps[conf['title']] += 1
        results[k] = conf

    # results = {idx:conf for idx, conf in enumerate(confs)}

    return results

def get_conf_info(path_opt='config_dir/allacc.yml'):
    conf_infos = get_config(path_opt)
    conf_infos = {v['title']:v for v in conf_infos}
    return conf_infos


def update_ccf_confs():

    if not os.path.exists('config_dir/types_cache.yml'):

        allconf = 'https://raw.githubusercontent.com/ccfddl/ccfddl.github.io/page/conference/allconf.yml'
        result = requests.get(url=allconf)
        if os.path.exists('config_dir/allconf.yml'): shutil.move('config_dir/allconf.yml', 'config_dir/allconf_bk.yml')
        with open('config_dir/allconf.yml', 'w', encoding='utf8') as f:
            f.write(result.text)

        allconf = 'https://raw.githubusercontent.com/ccfddl/ccfddl.github.io/page/conference/allacc.yml'
        result = requests.get(url=allconf)
        if os.path.exists('config_dir/allacc.yml'): shutil.move('config_dir/allacc.yml', 'config_dir/allacc_bk.yml')
        with open('config_dir/allacc.yml', 'w', encoding='utf8') as f:
            f.write(result.text)

        allconf = 'https://raw.githubusercontent.com/ccfddl/ccfddl.github.io/page/conference/types.yml'
        result = requests.get(url=allconf)
        if os.path.exists('config_dir/types.yml'): shutil.move('config_dir/types.yml', 'config_dir/types_bk.yml')
        with open('config_dir/types.yml', 'w', encoding='utf8') as f:
            f.write(result.text)

        try:
            ccf_confs = get_ccf_ddl(path_opt='config_dir/allconf.yml', map_opt='config_dir/types.yml')
        except:
            ccf_confs = get_ccf_ddl(path_opt='config_dir/allconf_bk.yml', map_opt='config_dir/types_bk.yml')
            shutil.copy('config_dir/allconf_bk.yml', 'config_dir/allconf_cache.yml')
            shutil.copy('config_dir/allacc_bk.yml', 'config_dir/allacc_cache.yml')
            shutil.copy('config_dir/types_bk.yml', 'config_dir/types_cache.yml')

    else:
        ccf_confs = get_ccf_ddl(path_opt='config_dir/allconf_cache.yml', map_opt='config_dir/types_cache.yml')

    return ccf_confs
# -------------------------------------------------------------


if __name__=="__main__":
    # update_ccf_confs()
    confs = get_ccf_ddl(path_opt='config_dir/allconf.yml', map_opt='config_dir/types.yml')

    titles = []
    for k,v in confs.items():
        print(k,v)
        titles.append(v['title'])
    print(len(set(titles)))

    # get_conf_info()