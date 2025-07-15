import tensorflow as tf
from tensorflow import keras

# # # 输入数据
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
print(x_train.shape)

# # # 显示训练集中前25个图像
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20,20))
axes = axes.ravel()

for i in range(25):
    axes[i].imshow(x_train[i], cmap='gray')
    axes[i].set_title(y_train[i])
    axes[i].axis('off')

plt.subplots_adjust(hspace=0.5)
plt.show()

# # # 设定神经网络模型
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    layers.Flatten(input_shape=(28, 28, 1)),
    layers.Dense(25, activation='relu', name='layer1'),
    layers.Dense(15, activation='relu', name='layer2'),
    layers.Dense(10, activation='softmax', name='layer3')
],name='MINST_Model'
)

model.summary()

# # # 神经网络编译部分
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
)

# # # 训练模型
history = model.fit(
    x_train, y_train,
    epochs=40
)

# # # 根据 Loss 绘制曲线
import matplotlib.pyplot as plt

train_loss = history.history['loss']

plt.plot(train_loss, label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# # # 进行预测
from sklearn.metrics import accuracy_score
import numpy as np

pred_y = model.predict(x_test)
pred_labels = np.argmax(pred_y, axis=1)
acc = accuracy_score(y_test, pred_labels)
print('Test accuracy:', acc)
