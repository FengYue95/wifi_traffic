#coding=utf-8
import pandas

#由mac_list得到相应的数据文件存储地址列表
def get_node_path_list(mac_list,sourcefolder,date):
    node_path_list=[]
    for mac in mac_list:
        path=sourcefolder+mac+"/"+date
        node_path_list.append(path)
    return node_path_list

#从原始数据文件里读取数据转化为dataframe，
# 并为其取字段名字
def get_df_by_path(path):
    name=['mac','signal','time']
    df=pandas.read_table(path,names=name,sep='|',header=None)
    return df

#将一个检测地点部署的若干个ap的数据
# 合并成一个dataframe
def merge_datafeame(df_list):
    df=pandas.DataFrame()
    for temp_df in df_list:
        df=pandas.concat([df,temp_df],ignore_index=True)
    return df


