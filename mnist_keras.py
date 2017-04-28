import tensorflow as tf
from keras.initializers import Constant
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras import backend as K

from keras.objectives import categorical_crossentropy
from tensorflow.examples.tutorials.mnist import input_data

sess = tf.Session()
K.set_session(sess)

# this placeholder will contain our input digits, as flat vectors
img = tf.placeholder(tf.float32, shape=(None, 784), name="input_tensor")
labels = tf.placeholder(tf.float32, shape=(None, 10))

# Keras layers can be called on TensorFlow tensors:
x = Reshape((-1, 28, 28))(img)
x = Conv2D(32, kernel_size=(5, 5), strides=(1, 1), padding='same',
    activation='relu', use_bias=True, bias_initializer='zeros', name="conv2d_1")(x)
x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', name="max_pool_1")(x)
x = Conv2D(64, kernel_size=(5, 5), strides=(1, 1), padding='same',
    activation='relu', use_bias=True, bias_initializer='zeros', name="conv2d_2")(x)
x = MaxPooling2D(pool_size=(2, 2), strides=None, padding='same', name="max_pool_2")(x)
x = Flatten(name='flatten')(x)
x = Dense(1024, activation='relu', use_bias=True, bias_initializer='zeros', name='fc1')(x)
x = Dropout(0.5, name='dropout')(x)
preds = Dense(10, use_bias=True, bias_initializer='zeros', name='fc2')(x)  # output layer with 10 units and a softmax activation
preds = tf.identity(preds, name="output_tensor")

# Training function
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=preds))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# Accuracy so we can verify method
correct_prediction = tf.equal(tf.argmax(preds,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Prepare saver.
builder = tf.saved_model.builder.SavedModelBuilder("./model_keras")

# Initialize all variables
sess.run(tf.global_variables_initializer())

# Load traning data.
mnist_data = input_data.read_data_sets('MNIST_data', one_hot=True)

# Run training loop
with sess.as_default():
    for i in range(20000):
        batch = mnist_data.train.next_batch(50)
        if i%100 == 0:
            train_accuracy = accuracy.eval(feed_dict={
                img:batch[0], labels: batch[1], K.learning_phase(): 0})
            print("step %d, training accuracy %g"%(i, train_accuracy))
        train_step.run(feed_dict={img: batch[0],
                                  labels: batch[1],
                                  K.learning_phase(): 1})

# Save model so we can use it in java.
builder.add_meta_graph_and_variables(sess, [tf.saved_model.tag_constants.SERVING])
builder.save(True)

# Print final accuracy.
with sess.as_default():
    print("test accuracy %g" % accuracy.eval(feed_dict={
        img: mnist_data.test.images,
        labels: mnist_data.test.labels,
        K.learning_phase(): 0}))
