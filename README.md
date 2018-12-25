# GestureRecognition
Gesture Recognition implements of PaddlePaddle

# Introduce
1、classify.ipynb: 训练器代码
2、utils.py: 图像处理 
3、infer.py: 使用训练好的代码进行预测  
4、gesture: 训练代码   
5、fronted: 前端可视化  

# Usage  
1、使用utils.py将gesture/raw_data的图片增强  
2、classify.ipynb训练代码模型，生成的模型保存在DNN_model/下  
3、使用infer.py进行预测  

# Enviroment    
在Python2.7的环境下开发  
1、PaddlePaddle Fluid 1.2（建议使用官方docker）  
2、jupyter    
3、Flask   
