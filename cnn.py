import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问
# 1. 数据加载与预处理
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# 数据归一化并添加通道维度 (60000, 28, 28) -> (60000, 28, 28, 1)
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# 2. 构建CNN模型 - 使用步幅卷积替代池化层减少信息损失
model = models.Sequential([
    # 卷积层1：使用32个3x3滤波器，步幅1保持分辨率
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(28, 28, 1)),

    # 使用步幅卷积替代池化 (stride=2实现降采样)
    layers.Conv2D(64, (3, 3), activation='relu', strides=2, padding='same'),

    # 卷积层2：增加特征提取能力
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),

    # 再次使用步幅卷积降维
    layers.Conv2D(256, (3, 3), activation='relu', strides=2, padding='same'),

    # 正则化层防止过拟合
    layers.Dropout(0.3),

    # 展平特征图
    layers.Flatten(),

    # 全连接层
    layers.Dense(128, activation='relu'),

    # 输出层 (10个数字类别)
    layers.Dense(10, activation='softmax')
])

# 3. 模型编译
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 4. 训练模型 (使用20%数据作为验证集)
history = model.fit(train_images, train_labels,
                    epochs=10,
                    batch_size=128,
                    validation_split=0.2)

# 5. 模型评估
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(f'\n测试准确率: {test_acc:.4f}')

# 6. 可视化训练过程
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Taining accuracy')
plt.plot(history.history['val_accuracy'], label='Validation accuracy')
plt.title('Ｍodel Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Taining loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

#model.save('model.h5')
# 7. 进行预测示例
import numpy as np

# 随机选择测试图像
sample_idx = np.random.randint(0, test_images.shape[0])
sample_image = test_images[sample_idx]
sample_label = test_labels[sample_idx]

# 预测并显示结果
prediction = model.predict(np.array([sample_image]))
predicted_label = np.argmax(prediction)

# 可视化
plt.imshow(sample_image.squeeze(), cmap='gray')
plt.title(f'RealTags: {sample_label} | Prediction: {predicted_label}')
plt.axis('off')
plt.show()