# -*- coding:utf-8 -*-
from __future__ import print_function
import paddle
import paddle.fluid as fluid
import numpy
try:
    from paddle.fluid.contrib.trainer import *
    from paddle.fluid.contrib.inferencer import *
except ImportError:
    print("Import error")
    from paddle.fluid.trainer import *
    from paddle.fluid.inferencer import *

import numpy as np
import paddle
import paddle.fluid as fluid
import os
import logging
from PIL import Image, ImageOps
IMAGE_WIDTH, IMAGE_HEGHT = 64,64
logging.basicConfig(filename='logs/api_predict.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_image(filename):
    """
    定义读取输入图片的函数：
        读取指定路径下的图片，将其处理成分类网络输入数据对应形式的数据，如数据维度等
    Args:
        file -- 输入图片的文件路径
    Return:
        im -- 分类网络输入数据对应形式的数据
    """
    im = Image.open(filename).convert('L')
    im = im.resize((IMAGE_WIDTH,IMAGE_HEGHT), Image.ANTIALIAS)
    im = np.array(im).reshape(1, 1, IMAGE_WIDTH,IMAGE_HEGHT).astype(np.float32)
    im = im / 255.0 * 2.0 - 1.0
    return im


def convolutional_neural_network():
    """
    定义卷积神经网络分类器：
        输入的二维图像，经过两个卷积-池化层，使用以softmax为激活函数的全连接层作为输出层
    Args:
        img -- 输入的原始图像数据
    Return:
        predict -- 分类的结果
    """
    img = fluid.layers.data(
        name='img', shape =[1,IMAGE_WIDTH,IMAGE_HEGHT],dtype = 'float32')
    # 第一个卷积-池化层
    # 基本设置参考： filter 的数量 20
    conv_pool1 = fluid.nets.simple_img_conv_pool(input=img, 
                                             num_filters=20, 
                                             filter_size=5, 
                                             pool_size=2, 
                                             pool_stride=2, 
                                             pool_padding=0,
                                             act='relu')


    
    # 第二个卷积-池化层
    # 基本设置参考： filter 的数量 50
    conv_pool2 = fluid.nets.simple_img_conv_pool(input=conv_pool1, 
                                             num_filters=50, 
                                             filter_size=5, 
                                             pool_size=2, 
                                             pool_stride=2, 
                                             pool_padding=0,
                                             act='relu')
    
    
    
    
    # 以softmax为激活函数的全连接输出层，输出层的大小必须为10,对应0-9这10个数字
    predict = fluid.layers.fc(input=conv_pool2, size=5, act='softmax')
    
    return predict

class Classify():

    def __init__(self, place=None, params_dirname="./DNN_model"):
        if not place:
            use_cuda = False
	    place = fluid.CUDAPlace(1) if use_cuda else fluid.CPUPlace()
        self.inferencer = Inferencer(
    		infer_func=convolutional_neural_network,  # uncomment for LeNet5
    		param_path=params_dirname,
    		place=place)

    def predict(self, img_file_path):
        try:
            img = load_image(img_file_path)
            results = self.inferencer.infer({'img': img})
            lab = np.argsort(results)
        except Exception as e:
            logger.exception(e)        
            return -1
        predict_label = lab[0][0][-1]
        logger.info('%s, predict: %s' % (img_file_path, predict_label))
        return predict_label

if __name__ == '__main__':
    classify = Classify()
    predict_label = classify.predict('./gesture/test/5/104.jpg')
    print("predict label: %s" % predict_label)
