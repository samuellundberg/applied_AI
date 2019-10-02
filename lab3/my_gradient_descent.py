"""Gradient descent for linear regression with numpy
"""
import random
import numpy as np
import matplotlib.pyplot as plt

# datasetX = np.array([[35680, 42514, 15162, 35298, 29800, 40255, 74532, 37464, 31030, 24843, 36172, 39552, 72545, 75352, 18031]]).T
datasetX = np.array([35680, 42514, 15162, 35298, 29800, 40255, 74532, 37464, 31030, 24843, 36172, 39552, 72545, 75352, 18031])
column_of_ones = np.array(len(datasetX) * [1.])
datasetX = np.array([column_of_ones, datasetX]).T
datasetY = np.array([[2217, 2761, 990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]]).T

dXf = np.array([36961, 43621, 15694, 36231, 29945, 40588, 75255, 37709, 30899, 25486, 37497, 40398, 74105, 76725, 18317])
# column_of_ones = np.array(len(dXf) * [1.])
dXf = np.array([column_of_ones, dXf]).T
dyf = np.array([[2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047, 5312, 1215]]).T




__author__ = 'Samuel Lundberg'


def sse(X, y, w):
    """
    Sum of squared errors
    :param X:
    :param y:
    :param w:
    :return:
    """
    error = y - X @ w
    return error.T @ error


def normalize(Xy):
    maxima = np.amax(Xy, axis=0)
    D = np.diag(maxima)
    D_inv = np.linalg.inv(D)
    Xy = Xy @ D_inv
    return (Xy, maxima)


def stoch_descent(X, y, alpha, w):
    """
    Stochastic gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :return:
    """
    global logs, logs_stoch
    logs = []
    logs_stoch = []
    random.seed(0)
    idx = list(range(len(X)))
    for epoch in range(500):
        random.shuffle(idx)
        w_old = w
        for i in idx:
            loss = y[i] - X[i] @ w
            gradient = loss * X[i].reshape(-1, 1)
            w = w + alpha * gradient
            logs_stoch += (w, alpha, sse(X, y, w))
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.005:
            print("Epoch", epoch)
            break
        logs += (w, alpha, sse(X, y, w))
    return w


def batch_descent(X, y, alpha, w):
    """
    Batch gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :return:
    """
    global logs
    logs = []
    alpha /= len(X)
    for epoch in range(1, 500):
        loss = y - X @ w
        gradient = X.T @ loss
        w_old = w
        w = w + alpha * gradient
        logs += (w, alpha, sse(X, y, w))
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.0005:
            print("Epoch", epoch)
            break
    return w


if __name__ == '__main__':
    normalized = True
    debug = False
    # mode = 0: Batch descent
    # mode = 1: Stochastic descent
    mode = 0
    # Predictors
    X = datasetX
    # Response
    y = datasetY
    
    Xf = dXf
    yf = dyf

    alpha = 1.0e-10
    if normalized:
        X, maxima_X = normalize(X)
        y, maxima_y = normalize(y)
        maxima = np.concatenate((maxima_X, maxima_y))
        
        Xf, maxima_Xf = normalize(Xf)
        yf, maxima_yf = normalize(yf)
        maximaf = np.array([np.concatenate((maxima_Xf, maxima_yf))]).T        
        # alpha = 1.5343
        alpha = 1
        print("-Normalized-")
        
    
    if mode == 0:
        print("===Batch descent===")
        w = np.zeros(X.shape[1]).reshape((-1, 1))
        w = batch_descent(X, y, alpha, w)
        wf = np.zeros(Xf.shape[1]).reshape((-1, 1))
        wf = batch_descent(Xf, yf, alpha, wf)

        print("Weights", w)
        print("SSE", sse(X, y, w))
        if normalized:
            maxima = maxima.reshape(-1, 1)
            print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
        if debug:
            print("Logs", logs)
        plt.figure(1)
        plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
        plt.title("Batch gradient descent: Sum of squared errors, alpha = 2")
        plt.show()
        plt.figure(2)
        plt.plot(list(map(lambda pair: pair[0], logs[0::3])), list(map(lambda pair: pair[1], logs[0::3])), marker='o')
        for i in range(len(logs[0::3])):
            plt.annotate(i, xy=logs[0::3][i])
        plt.title("Batch gradient descent: Weights, alpha = 2")
        plt.show()
                
        restored_w = maxima[-1, 0] * (w / maxima[:-1, 0:1])
        restored_wf = maximaf[-1, 0] * (wf / maximaf[:-1, 0:1])
        
        plt.figure(3)
        plt.scatter(datasetX[:,1],datasetY, c = 'r', marker = 'x')
        xl = np.array([[1,0],[1,max(maxima_X[1], maxima_Xf[1])+100]])
        plt.plot(xl[:,1], xl@restored_w, c = 'r')
        plt.scatter(dXf[:,1],dyf, c = 'b', marker = 'x')
        plt.plot(xl[:,1], xl@restored_wf, c = 'b')
        plt.title("Linerar regressiong for english (red) and french (blue), alpha = 2")

        
        
    
    if mode == 1:
        print("===Stochastic descent===")
        w = np.zeros(X.shape[1]).reshape((-1, 1))
        w = stoch_descent(X, y, alpha, w)
        wf = np.zeros(Xf.shape[1]).reshape((-1, 1))
        wf = stoch_descent(Xf, yf, alpha, wf)
        print("Weights", w)
        print("SSE", sse(X, y, w))
        if normalized:
            maxima = maxima.reshape(-1, 1)
            print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
        if debug:
            print("Logs", logs)
            print("Logs stoch.", logs_stoch)
            
        plt.figure(1)
        plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
        plt.title("Stochastic gradient descent: Sum of squared errors")
        plt.show()
        plt.figure(2)
        plt.plot(list(map(lambda pair: pair[0], logs[0::3])), list(map(lambda pair: pair[1], logs[0::3])), marker='o')
        plt.title("Stochastic gradient descent: Weights")
        plt.show()
        plt.figure(3)
        plt.scatter(range(len(logs_stoch[2::3])), logs_stoch[2::3], c='b', marker='x')
        plt.title("Stochastic gradient descent: Sum of squared errors (individual updates)")
        plt.show()
        plt.figure(4)
        plt.plot(list(map(lambda pair: pair[0], logs_stoch[0::3])), list(map(lambda pair: pair[1], logs_stoch[0::3])),
                 marker='o')
        plt.title("Stochastic gradient descent: Weights (individual updates)")
        plt.show()
        
        restored_w = maxima[-1, 0] * (w / maxima[:-1, 0:1])
        restored_wf = maximaf[-1, 0] * (wf / maximaf[:-1, 0:1])
        
        plt.figure(5)
        plt.scatter(datasetX[:,1],datasetY, c = 'r', marker = 'x')
        xl = np.array([[1,0],[1,max(maxima_X[1], maxima_Xf[1])+100]])
        plt.plot(xl[:,1], xl@restored_w, c = 'r')
        plt.scatter(dXf[:,1],dyf, c = 'b', marker = 'x')
        plt.plot(xl[:,1], xl@restored_wf, c = 'b')
        plt.title("Linerar regressing for english (red) and french (blue)")

    