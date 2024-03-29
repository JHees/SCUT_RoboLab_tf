from __future__ import absolute_import, division, print_function, unicode_literals


import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from PIL import Image

mnist = keras.datasets.mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9 ']

train_images = train_images / 255.0
test_images = test_images / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=10)
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

def load_img(filepos):
    img = Image.open(filepos)
    img = img.resize((28,28),Image.ANTIALIAS)
    img = np.array(img.convert("L"))
    opimg = np.empty((28,28),dtype="float")
    for i in range(28):
        for j in range(28):
                opimg[i][j] = 255 - img[i][j]
    opimg = np.array(opimg)
    opimg = opimg.reshape(28,28)
    opimg = opimg.astype(np.float)
    opimg = np.multiply(opimg, 1.0/255.0)
    return opimg
def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, true_label, img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'
    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                    100*np.max(predictions_array),
                                    class_names[true_label]),
                                    color=color)
def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array, true_label
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)
    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


img = np.array([load_img("./pic/0.jpeg"),
                                load_img("./pic/1.jpeg"),
                                load_img("./pic/2.jpeg"),
                                load_img("./pic/3.jpeg"),
                                load_img("./pic/4.jpeg"),
                                load_img("./pic/5.jpeg"),
                                load_img("./pic/6.jpeg"),
                                load_img("./pic/7.jpeg"),
                                load_img("./pic/8.jpeg"),
                                load_img("./pic/9.jpeg")])

predictions = model.predict(img)
num_rows = 5
num_cols = 2
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):

    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions[i], i, img)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions[i], i)
plt.tight_layout()
plt.show()