# 实现PCA分析和法向量计算，并加载数据集中的文件进行验证

import open3d as o3d
import numpy as np
from pandas import DataFrame
from pyntcloud import PyntCloud

# 功能：计算PCA的函数
# 输入：
#     data：点云，NX3的矩阵
#     correlation：区分np的cov和corrcoef，不输入时默认为False
#     sort: 特征值排序，排序是为了其他功能方便使用，不输入时默认为True
# 输出：
#     eigenvalues：特征值
#     eigenvectors：特征向量
def PCA(data, correlation=False, sort=True):
    # 作业1
    # 屏蔽开始
    # print("rows=\n", data.shape[0])
    # print("cols=\n", data.shape[1])
    # 求x\y\z三列的均值
    data_avg = np.mean(data, axis = 0)
    # print("data_avg.shape[0]=\n", data_avg.shape[0])
    # print("data_avg=\n", data_avg)
    # 中心化
    data_c = data - data_avg
    # 协方差矩阵
    H = np.dot(data_c.T, data_c)
    # H_cov= np.cov(data.T) * (data.shape[0] - 1)
    # svd奇异值分解求特征值、特征向量
    eigenvectors, eigenvalues, eigenvectors_T = np.linalg.svd(H)
    # print("eigenvectors=\n", eigenvectors)
    # print("eigenvalues=\n", eigenvalues)
    # 屏蔽结束

    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def main():
    # 加载原始点云
    point_cloud_pynt = PyntCloud.from_file("./person_0001.off.ply") #./bunny10k.ply
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    o3d.visualization.draw_geometries([point_cloud_o3d], window_name="Original Point Cloud") # 显示原始点云

    # 从点云中获取点，只对点进行处理
    points = point_cloud_pynt.points
    print('total points number is:', points.shape[0])
    print("point=\n", points)
    # 用PCA分析点云主方向
    w, v = PCA(points)
    # 点云主方向对应的向量
    point_cloud_vector = v[:, 2]
    print('the main orientation of this pointcloud is: ', point_cloud_vector)
    point_pca = DataFrame((np.dot(v.T, points.T)).T)
    print("point_pca=\n", point_pca)
    point_pca.columns = ['x', 'y', 'z']  # 给选取到的数据 附上标题
    point_cloud_pynt_pca = PyntCloud(point_pca)
    point_cloud_o3d_pca = point_cloud_pynt_pca.to_instance("open3d", mesh=False)
    #o3d.visualization.draw_geometries([point_cloud_o3d_pca])
    
    # 循环计算每个点的法向量
    pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    normals = []
    # 作业2
    # 屏蔽开始
    for i in range(points.shape[0]):
        # #取10个临近点进行曲线拟合
        [k, idx, _] = pcd_tree.search_knn_vector_3d(point_cloud_o3d.points[i], 10)
        k_nearest_point = np.asarray(point_cloud_o3d.points)[idx, :]
        w, v = PCA(k_nearest_point)
        normals.append(v[:, 2])
    # 屏蔽结束
    normals = np.array(normals, dtype=np.float64)
    # print("normals=\n", normals)
    # TODO: 此处把法向量存放在了normals中
    point_cloud_o3d.normals = o3d.utility.Vector3dVector(normals)
    o3d.visualization.draw_geometries([point_cloud_o3d],
                                      point_show_normal=True,
                                      window_name="Normal Point Cloud")


if __name__ == '__main__':
    main()
