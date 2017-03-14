#coding=utf-8
import numpy as np
#import pylab as pl
from sklearn.cluster import KMeans


# np.random.seed(0)
# centers = [[1,1], [-1,-1], [1, -1]]
# k = len(centers)
# x , labels = make_blobs(n_samples=3000, centers=centers, cluster_std=.7)
# print type(x)

def clusting(path):
    #历史数据导入
    dataSet = []
    mac=[]
    #簇数
    k=2
    #聚类权重
    weigth=[3,1]
    #导入数据
    fileIn = open(path)
    for line in fileIn.readlines():
        lineArr = line.strip().split('|')
        dataSet.append([float(lineArr[2])*weigth[0], float(lineArr[3])*weigth[1]])
        mac.append(lineArr[4])
    x=np.array(dataSet)
    print "待聚类样本 %s",x
    if x.size<5: return [""]

    kmeans = KMeans(init='k-means++', n_clusters=2, n_init = 100)
    kmeans.fit(x)

    targetlabel=1

    if kmeans.cluster_centers_[0][0]>kmeans.cluster_centers_[1][0]:
        targetlabel=0

    print "target cluster:"+str(targetlabel)


    colors = ['r', 'b']
    targetcluster=[[],[]]
    for k , col in zip( range(k) , colors):
        members = (kmeans.labels_ == k )

        for i in range(len(members)):
            if members[i]:
                targetcluster[k].append(mac[i])

    #     pl.plot( x[members, 0] , x[members,1] , 'w', markerfacecolor=col, marker='.',markersize=10)
    #     pl.plot(kmeans.cluster_centers_[k,0], kmeans.cluster_centers_[k,1], 'o', markerfacecolor=col,markeredgecolor='k', markersize=10)
    # pl.show()
    print "cluter 0"
    print len(targetcluster[0])
    print targetcluster[0]
    print "cluter 1"
    print len(targetcluster[1])
    print targetcluster[1]
    #返回目标簇mac集
    return targetcluster[targetlabel]


#clusting("P:/data/wifiresult/23/history_statistic_1477879200")