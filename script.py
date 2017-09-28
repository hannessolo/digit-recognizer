import sys
import os
import numpy
import tensorflow as tf
from mnist_data import Data

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# input
X = tf.placeholder(tf.float32, [None, 28, 28, 1])

# weights for convolutional layers
W1 = tf.Variable(tf.truncated_normal([6, 6, 1, 6], stddev=0.1))
b1 = tf.Variable(tf.ones([6])/10)
W2 = tf.Variable(tf.truncated_normal([5, 5, 6, 12], stddev=0.1))
b2 = tf.Variable(tf.ones([12])/10)
W3 = tf.Variable(tf.truncated_normal([4, 4, 12, 24], stddev=0.1))
b3 = tf.Variable(tf.ones([24])/10)
# fully connected layer weights and bias
W4 = tf.Variable(tf.truncated_normal([1176, 200], stddev=0.1))
b4 = tf.Variable(tf.ones([200])/10)

# weight and bias for readout layer
Wf = tf.Variable(tf.truncated_normal([200, 10], stddev=0.1))
bf = tf.Variable(tf.zeros([10]) + 0.1)

# model
Y1cnv = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
Y1 = tf.nn.relu(Y1cnv + b1)
Y2cnv = tf.nn.conv2d(Y1, W2, strides=[1, 2, 2, 1], padding='SAME')
Y2 = tf.nn.relu(Y2cnv + b2)
Y3cnv = tf.nn.conv2d(Y2, W3, strides=[1, 2, 2, 1], padding='SAME')
Y3 = tf.nn.relu(Y3cnv + b3)

Y4 = tf.nn.relu(tf.matmul(tf.reshape(Y3, [-1, 1176]), W4) + b4)
Y = tf.nn.softmax(tf.matmul(Y4, Wf) + bf)
# placeholder for correct labels
Y_ = tf.placeholder(tf.float32, [None, 10])

# loss
cross_entropy = -tf.reduce_sum(Y_ * tf.log(Y))

# percent of correct answers in batch
is_correct = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

optimizer = tf.train.AdamOptimizer(0.003)
train_step = optimizer.minimize(cross_entropy)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

saver = tf.train.Saver()

if sys.argv[1] == 'train':

    testing_data = Data('E:\storage_data\documents\code\machine_learning\mnist_test.csv')
    training_data = Data('E:\storage_data\documents\code\machine_learning\mnist_train.csv')
    test_vals = testing_data.next_batch(2000, conv=True)

    test_data = {X: test_vals['x'], Y_: test_vals['y']}

    for i in range(1000):
        next_batch = training_data.next_batch(100, conv=True)
        batch_X = next_batch['x']
        batch_Y = next_batch['y']
        train_data = {X: batch_X, Y_: batch_Y}

        sess.run(train_step, feed_dict=train_data)
        if i % 100 == 0:
            print('accuracy:', sess.run(accuracy, feed_dict=test_data))
            print('cross entropy:', sess.run(cross_entropy, feed_dict=test_data))

    print(sess.run(accuracy, test_data))

    saver.save(sess, os.path.dirname(os.path.realpath(__file__))+'/model/saved_model')

    test_val = testing_data.next_batch(5, conv=True)
    print(sess.run(Y, feed_dict={X: test_val['x'], Y: test_val['y']})[4])

else:

    saver.restore(sess, os.path.dirname(os.path.realpath(__file__))+'/model/saved_model')
    array = sys.argv[1].split(',')
    array = (numpy.asfarray(array) / 255 * 0.99 ) + 0.01
    result = sess.run(Y, feed_dict={X: array.reshape([1,28,28,1])})
    print(numpy.argmax(result, 1)[0])
sess.close()
