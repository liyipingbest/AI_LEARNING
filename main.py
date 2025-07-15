import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from sklearn.metrics import accuracy_score
import numpy as np

# 加载 MNIST 数据集，其中包含手写数字的图像和对应的标签
# x_train 和 y_train 是训练集的图像和标签，分别表示图像数据和对应的数字标签
# x_test 和 y_test 是测试集的图像和标签，用于评估模型的性能
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
print(x_train.shape)  # 输出训练集的形状，验证数据加载是否正确

# 创建一个 5x5 的网格，用于显示训练集中的前 25 个图像
# 使用 Matplotlib 库进行可视化，帮助理解数据的分布和样本特征
fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20,20))
axes = axes.ravel()  # 将子图对象展平为一维数组，方便迭代操作

# 遍历前 25 个图像，将它们显示在网格中
for i in range(25):
    axes[i].imshow(x_train[i], cmap='gray')  # 显示图像，使用灰度颜色映射以突出手写数字的细节
    axes[i].set_title(y_train[i])  # 设置图像标题为对应的标签，显示数字类别
    axes[i].axis('off')  # 关闭坐标轴显示，简化图像展示

# 调整子图之间的间距并显示图像
plt.subplots_adjust(hspace=0.5)  # 设置子图之间的垂直间距，避免标题重叠
plt.show()  # 显示图像网格

# 定义一个顺序模型，用于分类 MNIST 数据集中的手写数字
# 使用 Keras 的 Sequential API 构建模型，按层次顺序添加神经网络层
model = Sequential([
    layers.Flatten(input_shape=(28, 28, 1)),  # 输入层：将 28x28 的图像展平为一维数组，便于后续处理
    layers.Dense(25, activation='relu', name='layer1'),  # 第一隐藏层：25 个神经元，激活函数为 ReLU，用于提取特征
    layers.Dense(15, activation='relu', name='layer2'),  # 第二隐藏层：15 个神经元，激活函数为 ReLU，进一步提取特征
    layers.Dense(10, activation='softmax', name='layer3')  # 输出层：10 个神经元，激活函数为 Softmax，用于分类
], name='MINST_Model')

# 打印模型的结构摘要
# 显示每层的名称、输出形状和参数数量，帮助理解模型的架构
model.summary()

# 编译模型，指定损失函数、优化器和学习率
# 损失函数：稀疏分类交叉熵，用于多分类问题
# 优化器：Adam，具有自适应学习率的优化算法
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
)

# 训练模型，使用训练集的图像和标签，迭代 40 个周期
# 通过 fit 方法进行训练，返回训练历史对象
history = model.fit(
    x_train, y_train,
    epochs=40  # 迭代次数：40，模型将多次学习数据以提高性能
)

# 从训练历史中提取损失值，并绘制损失曲线
# 通过可视化损失值的变化，观察模型的收敛情况
train_loss = history.history['loss']

plt.plot(train_loss, label='Training Loss')  # 绘制训练损失曲线
plt.xlabel('Epoch')  # 设置 x 轴标签为迭代周期
plt.ylabel('Loss')  # 设置 y 轴标签为损失值
plt.legend()  # 显示图例，标注曲线含义
plt.show()  # 显示损失曲线

# 使用模型对测试集进行预测，得到预测的概率分布
# 通过 predict 方法生成每个样本属于各类别的概率
print(f'x_test = {x_test} \n\n')  
pred_y = model.predict(x_test)

# 将预测的概率分布转换为标签
# 使用 argmax 方法找到概率最大的类别，作为预测结果
pred_labels = np.argmax(pred_y, axis=1)

# 计算预测结果的准确率，并打印测试集的准确率
# 使用 scikit-learn 的 accuracy_score 方法评估模型性能
acc = accuracy_score(y_test, pred_labels)
print('Test accuracy:', acc)  # 输出测试集的分类准确率
