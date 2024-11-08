import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

# 1. 数据加载与预处理
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 将图像填充到32x32
x_train = np.pad(x_train, ((0, 0), (2, 2), (2, 2)), mode='constant', constant_values=0)
x_test = np.pad(x_test, ((0, 0), (2, 2), (2, 2)), mode='constant', constant_values=0)
x_train = x_train.reshape((60000, 32, 32, 1)).astype('float32') / 255.0
x_test = x_test.reshape((10000, 32, 32, 1)).astype('float32') / 255.0

# 2. 模型定义
def create_lenet():
    model = models.Sequential()
    model.add(layers.Conv2D(6, (5, 5), activation='tanh', input_shape=(32, 32, 1)))
    model.add(layers.AveragePooling2D((2, 2)))
    model.add(layers.Conv2D(16, (5, 5), activation='tanh'))
    model.add(layers.AveragePooling2D((2, 2)))
    model.add(layers.Conv2D(120, (5, 5), activation='tanh'))
    model.add(layers.Flatten())
    model.add(layers.Dense(84, activation='tanh'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

lenet_model = create_lenet()

# 3. 模型编译与训练
lenet_model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])

history = lenet_model.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.1)

# 4. 模型评估
test_loss, test_acc = lenet_model.evaluate(x_test, y_test, verbose=2)
print(f'Test accuracy: {test_acc}')

# 5. 可视化训练过程
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')
plt.show()
