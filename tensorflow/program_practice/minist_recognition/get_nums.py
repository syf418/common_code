"""
基于TensorFlow的手写数字识别
Author_Zjh
2018/12/3
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
import matplotlib.patches as mpatches
from skimage import data,segmentation,measure,morphology,color
import tensorflow as tf
class Number_recognition():
    """ 模型恢复初始化"""
    def __init__(self,img):
        self.sess = tf.InteractiveSession()
        saver = tf.train.import_meta_graph('model_data/model.meta')
        saver.restore(self.sess, 'model_data/model') #模型恢复
        # graph = tf.get_default_graph()
        # 获取输入tensor,,获取输出tensor
        self.input_x = self.sess.graph.get_tensor_by_name("Mul:0")
        self.y_conv2 = self.sess.graph.get_tensor_by_name("final_result:0")
        self.Preprocessing(img)#图像预处理
    def recognition(self,im):
        im = cv2.resize(im, (28, 28), interpolation=cv2.INTER_CUBIC)
        x_img = np.reshape(im, [-1, 784])
        output = self.sess.run(self.y_conv2, feed_dict={self.input_x: x_img})
        print('您输入的数字是 %d' % (np.argmax(output)))
        return np.argmax(output)#返回识别的结果

    def Preprocessing(self,image):
        if image.shape[0]>800:
            image = imutils.resize(image, height=800) #如果图像太大局部阈值分割速度会稍慢些，因此图像太大时进行降采样

        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to gray picture
        m1, n1 = img.shape
        k = int(m1 / 19) + 1
        l = int(n1 / 19) + 1
        img = cv2.GaussianBlur(img, (3, 3), 0) # 高斯滤波
        imm = img.copy()
        # 基于Niblack的局部阈值分割法，对于提取文本类图像分割效果比较好
        for x in range(k):
            for y in range(l):
                s = imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)]
                me = s.mean() # 均值
                var = np.std(s) # 方差
                t = me * (1 - 0.2 * ((125 - var) / 125))
                ret, imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)] = cv2.threshold(
                imm[19 * x:19 * (x + 1), 19 * y:19 * (y + 1)], t, 255, cv2.THRESH_BINARY_INV)
                label_image = measure.label(imm) # 连通区域标记
                for region in measure.regionprops(label_image): # 循环得到每一个连通区域属性集
                    # 忽略小区域
                    if region.area < 100:
                        continue
                    minr, minc, maxr, maxc = region.bbox# 得到外包矩形参数
                    cv2.rectangle(image, (minc, minr), (maxc, maxr), (0, 255, 0), 2)#绘制连通区域
                    im2 = imm[minr - 5:maxr + 5, minc - 5:maxc + 5] #获得感兴趣区域，也即每个数字的区域
                    number = self.recognition(im2)#进行识别
                    cv2.putText(image, str(number), (minc, minr - 10), 0, 2, (0, 0, 255), 2)#将识别结果写在原图上
                    cv2.imshow("Nizi", imm)
                    cv2.imshow("Annie", image)
                    cv2.waitKey(0)
if __name__=='__main__':
    img = cv2.imread("nums.jpg")
    x=Number_recognition(img)