#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np
import matplotlib.pyplot as plt
"""
Created on Thu Feb 28 11:30:08 2019

@author: samuel
"""

datasetX = np.array([35680, 42514, 15162, 35298, 29800, 40255, 74532, 37464, 31030, 24843, 36172, 39552, 72545, 75352, 18031])
datasetY = np.array([2217, 2761, 990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119])
column_of_ones = np.array(len(datasetX) * [1])
En_data = np.array([column_of_ones, column_of_ones, datasetX, 2*column_of_ones, datasetY]).T

dXf = np.array([36961, 43621, 15694, 36231, 29945, 40588, 75255, 37709, 30899, 25486, 37497, 40398, 74105, 76725, 18317])
dyf = np.array([2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047, 5312, 1215])
Fr_data = np.array([0 * column_of_ones, column_of_ones, dXf, 2 * column_of_ones, dyf]).T


def sse(X, y, w):
    error = y - X @ w
    return error.T @ error


def normalize(Xy):
    maxima = np.amax(Xy, axis=0)
    D = np.diag(maxima)
    D_inv = np.linalg.inv(D)
    Xy = Xy @ D_inv
    return (Xy, maxima)


def perceptron(X, y, alpha, w, lang):
    global logs
    logs = []
    alpha /= len(X)
    for epoch in range(1, 500):
        bin_loss = X @ w - y
        c = 0
        for l in bin_loss:
            if l > 0:
                bin_loss[c] = 1
            else:
                bin_loss[c] = 0
            c += 1
            
        loss = lang - bin_loss
        gradient = X.T @ loss
        w_old = w
        w = w + alpha * gradient
        logs += (w, alpha, sse(X, y, w))        # do we care about the sse?
        if np.linalg.norm(loss,1)  < 0 + 1e-3:
            print("Epoch", epoch, 'loss', np.linalg.norm(loss,1))
            break
    return w


if __name__ == '__main__':
    normalized = True
    debug = False
    
    Data = np.concatenate((En_data, Fr_data), axis=0)
    r = random.randint(0,np.shape(Data)[0]-1)
    test_data = np.array([Data[r,:]])
    Data = np.concatenate((Data[:r,:], Data[r+1:,:]))
    
    X = Data[:,1:3]
    y = Data[:,-1:]
    
    alpha = 1.0e-10
    if normalized:
        X, maxima_X = normalize(X)
        y, maxima_y = normalize(y)
        maxima = np.concatenate((maxima_X, maxima_y))
        alpha = .1
        print("-Normalized-")
    
    print("===Gradient descent===")
    w = np.zeros(X.shape[1]).reshape((-1, 1))
    w = perceptron(X,y, alpha, w, Data[:,:1])

    print("Weights", w)
    if normalized:
        maxima = maxima.reshape(-1, 1)
        print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
    if debug:
        print("Logs", logs)
   
    plt.figure(1)
    plt.plot(list(map(lambda pair: pair[0], logs[0::3])), list(map(lambda pair: pair[1], logs[0::3])), marker='o')
    for i in range(len(logs[0::3])):
        plt.annotate(i, xy=logs[0::3][i])
    plt.title("Gradient descent: Weights")
    plt.show()
        
    restored_w = maxima[-1, 0] * (w / maxima[:-1, 0:1])
    plt.figure(2)
    plt.scatter(Data[:15,2],Data[:15,4], c = 'r', marker = 'x')
    plt.scatter(Data[15:,2],Data[15:,4], c = 'b', marker = 'x')

    xl = np.array([[1,0],[1, maxima_X[1]+100]])
    plt.plot(xl[:,1], xl@restored_w, c = 'g')
    plt.title("Classification by separating plane for english (red) and french (blue)")


    validation = test_data[0,1:3] @ w - test_data[0,-1]       
    if validation > 0:
        validation = 1
    else:
        validation = 0
    if validation == test_data[0,0]:
        print('classification using crossvalidation was successfull!')
    else:
        print('classification using crossvalidation failed :(')

            