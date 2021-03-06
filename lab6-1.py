import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def one_hot(x):
    return np.identity(16)[x:x+1]

env = gym.make('FrozenLake-v0')
input_size = env.observation_space.n
output_size = env.action_space.n
learning_rate = 0.1

X = tf.placeholder (shape = [1, input_size], dtype = tf.float32)
W = tf.Variable(tf.random_unitform([input_size, output_size, 0, 0.01]))

Qprediction = tf.matmul(X, W)
Y = tf.placeholder (shape = [1, output_size], dtype = tf.float32)

loss = tf.reduce_sum(tf.square(Y - Qprediction))
train = tf.train.GradientDescentOptimizer(learning_rate = learning_rate).minimize(loss)

discount_reward = 0.99
num_episodes = 2000

rList = []

with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        s = env.reset()
        e = 1. / ((i / 50) + 10)
        rAll = 0
        done = False
        local_loss = []

        while not done:
            Qs = sess.run(Qprediction, feed_dict = {X: one_hot(s)})
            if np.random(e) < e:
                a = env.action_space.sample()
            else:
                a = np.argmax(Qs)
            
            s1, reward, done, _ = env.step(a)
            if done:
                Qs[0, a] = reward
            else: 
                Qs1 = sess.run(Qprediction, feed_dict = {X: one_hot(s1)})
                Qs = reward + discount_reward * np.max(Qs1)

        sess.run(train, feed_dict = {X: one_hot(s), Y: Qs})

        rAll += reward
        s = s1
    rList.append(rAll)
     