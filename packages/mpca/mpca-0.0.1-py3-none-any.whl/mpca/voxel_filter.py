# 实现voxel滤波，并加载数据集中的文件进行验证

import open3d as o3d 
import os
import numpy as np
from pyntcloud import PyntCloud
from pandas import DataFrame
import random

# 功能：对点云进行voxel滤波
# 输入：
#     point_cloud：输入点云
#     leaf_size: voxel尺寸
def voxel_filter(point_cloud, leaf_size, method = "Centroid"):
    filtered_points = []
    # 作业3
    # 屏蔽开始
    # 1.compute max and min of the point set
    x_max, y_max, z_max = np.amax(point_cloud, axis=0)
    x_min, y_min, z_min = np.amin(point_cloud, axis=0)
    # 2.set voxel grid size r
    grid_r = leaf_size
    # 3.compute dim of the voxel grid
    dx = (x_max - x_min) / grid_r
    dy = (y_max - y_min) / grid_r
    dz = (z_max - z_min) / grid_r
    # 4.计算每个点在volex grid内每一个维度的值
    h = list()
    for x_i, y_i, z_i in zip(point_cloud['x'], point_cloud['y'], point_cloud['z']):
        hx = np.floor((x_i - x_min) / grid_r)
        hy = np.floor((y_i - y_min) / grid_r)
        hz = np.floor((z_i - z_min) / grid_r)
        h.append(hx + hy * dx + hz * dx * dy)
    # 5.sort points according to h
    arrayH = np.array(h)
    ah_index = np.argsort(arrayH)
    #print("ah_index=\n", ah_index)
    ah_sorted = arrayH[ah_index]
    #print("ah_sorted=\n", ah_sorted)
    # 6.select points according to Centroid / Random method
    count = 0
    for i in range(len(ah_sorted)-1):
        if ah_sorted[i] == ah_sorted[i+1]:
            continue
        else:
            point_idx = ah_index[count: i+1]
            filtered_points.append(choice_core(point_cloud, point_idx, method))
            count = i
    # 屏蔽结束

    # 把点云格式改成array，并对外返回
    filtered_points = np.array(filtered_points, dtype=np.float64)
    return filtered_points

#  点的选取函数
def choice_core(point_cloud, point_idx, method):
    #均值滤波
    if("Centroid" == method):
        point = np.mean(point_cloud.iloc[point_idx], axis=0)
    #随机滤波
    elif("Random" == method):
        random_point_idx = random.choice(point_idx)
        point = point_cloud.iloc[random_point_idx]
    return point

def main():
    # 加载自己的点云文件
    file_name = "./person_0001.off.ply"
    point_cloud_pynt = PyntCloud.from_file(file_name)

    # 转成open3d能识别的格式
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    o3d.visualization.draw_geometries([point_cloud_o3d], window_name="Original Point Cloud") # 显示原始点云

    # 调用voxel滤波函数，实现滤波
    Centroid = "Centroid"
    filtered_cloud = voxel_filter(point_cloud_pynt.points, 5.0, Centroid)
    if len(filtered_cloud):
        point_cloud_o3d.points = o3d.utility.Vector3dVector(filtered_cloud)
        o3d.visualization.draw_geometries([point_cloud_o3d], window_name=Centroid)

    # 调用voxel滤波函数，实现滤波
    Random = "Random"
    filtered_cloud = voxel_filter(point_cloud_pynt.points, 5.0, Random)
    if len(filtered_cloud):
        point_cloud_o3d.points = o3d.utility.Vector3dVector(filtered_cloud)
        o3d.visualization.draw_geometries([point_cloud_o3d], window_name=Random)

if __name__ == '__main__':
    main()
