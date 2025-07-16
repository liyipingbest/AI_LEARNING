import tensorflow as tf
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense

# 定义神经网络模型
model = Sequential([
    Flatten(input_shape=(28, 28, 1)),
    Dense(25, activation='relu', name='layer1'),
    Dense(15, activation='relu', name='layer2'),
    Dense(10, activation='softmax', name='layer3')
], name='MINST_Model')

# 保存神经网络结构图到当前目录
plot_model(model, to_file='./model_structure.png', show_shapes=True, show_layer_names=True)

print("神经网络结构图已保存为 model_structure.png")
