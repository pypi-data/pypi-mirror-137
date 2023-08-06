import os
import open3d as o3d
import numpy as np

EMPTY = "empty"

def load_model(cat_index):
    # 指定点云路径
    # cat_index = 10 # 物体编号，范围是0-39，即对应数据集中40个物体
    root_dir = './../../modelnet40_normal_resampled' # 数据集路径
    cat = os.listdir(root_dir)
    filename = os.path.join(root_dir, cat[cat_index], cat[cat_index]+'_0001.txt') # 默认使用第一个点云
    print(filename)
    if os.access(filename, os.F_OK) :
        print("model file path is exist.")
        return filename
    else:
        print("model file path is not exist.")
        return EMPTY

# 展示原模型
def ori_model(filename):
    rpcm = np.genfromtxt(filename, delimiter=",").reshape((-1,3))
    print("rpcm=\n", rpcm)
    o3dgpc = o3d.geometry.PointCloud()
    o3dgpc.points = o3d.utility.Vector3dVector(rpcm)
    print("o3dgpc=\n", o3dgpc)
    o3d.visualization.draw_geometries([o3dgpc])
    return o3dgpc

def main():
    cat_index = np.random.randint(0, 39)
    filename = load_model(cat_index)
    if (EMPTY == filename) :
        return False
    point_cloud_pynt = ori_model(filename)

if __name__ == "__main__":
    main()
