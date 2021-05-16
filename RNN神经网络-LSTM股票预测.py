import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
# rescale工具
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
# LSTM Long Short-Term Memory Networks 层
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer


def importData(src):#'predict.csv'
    dataset_train = pd.read_csv(src, encoding = 'gbk')
    dataset_train = dataset_train.iloc[::-1]
    training_set = dataset_train.iloc[:,[6,4,3]].values
    return training_set

def preProcessing(training_set):
    # pre-process
    imputer = SimpleImputer(missing_values=0,strategy='median')
    training_set[:,:] = imputer.fit_transform(training_set[:,:])
    # rescale
    sc = MinMaxScaler(feature_range=(0,1))
    real_stock_price = sc.fit_transform(training_set)
    return real_stock_price

def generateDatasets (real_stock_price):
    #用开盘价和最高价预测收盘价
    X_train = []
    y_train = []
    for i in range(10,real_stock_price.shape[0]-20):
        X_train.append(real_stock_price[i-10:i,[0,1]])
        y_train.append(real_stock_price[i,2])
    X_train,y_train = np.array(X_train), np.array(y_train)
    #每一次append进去十组数据，意思就是记忆长度为10
    #y结果由第一维的认证
    X_test = []
    y_test = []
    for i in range(real_stock_price.shape[0]-20,real_stock_price.shape[0]):
        X_test.append(real_stock_price[i-10:i,[0,1]])
        y_test.append(real_stock_price[i,2])
    X_test,y_test = np.array(X_test), np.array(y_test)
    return  X_train,y_train,X_test,y_test
        

def plotResult(real_stock_price, y_pred2, y_test, y_train):
    X_axis = np.array(range(real_stock_price.shape[0]-20,real_stock_price.shape[0]))
    X_axis_past = np.array(range(10,real_stock_price.shape[0]-20))
    fig = plt.figure(num=1, figsize=(15, 5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    pl1, = ax1.plot(X_axis,y_pred2,color='red',linewidth=1.0,linestyle='--')
    pl2, = ax1.plot(X_axis,y_test,color='blue',linewidth=1.0,linestyle='-')
    pl3, = ax2.plot(X_axis_past,y_train,color='blue',linewidth=1.0,linestyle='-')
    ax1.legend([pl1, pl2],['predict','real'])
    ax2.legend([pl3],['history'])
    # legend = ax1.legend([p1, p2], ["predict", "real"], facecolor='blue')
    # plt.plot(X_axis,y_pred2,color='red',linewidth=1.0,linestyle='--')
    # plt.plot(X_axis,y_test,color='blue',linewidth=1.0,linestyle='-')

def main():
    training_set = importData('predict.csv')
    real_stock_price = preProcessing(training_set)
    X_train,y_train,X_test,y_test = generateDatasets (real_stock_price)
    
    #模型建立
    rnn = Sequential()
    rnn.add(LSTM(10, input_shape=(X_train.shape[1],X_train.shape[2])))
    #维度数据直接取X_train的shape即可
    rnn.add(Dense(units=1))
    rnn.summary()
    # training
    rnn.compile(optimizer='adam', loss='mse')
    #这种loss是(yhat-y)^2
    rnn.fit(X_train,y_train, epochs = 15, batch_size=5)
    # prediction   
    y_pred2 = rnn.predict(X_test)
    y_pred2 = y_pred2.reshape(-1,)
    y_test = y_test.reshape(-1,)
    plotResult(real_stock_price, y_pred2, y_test, y_train)

# plt.plot(np.concatenate((y_pred1,y_pred2)),'red')
# plt.plot(np.concatenate((y_train,y_test)),'blue')

if __name__ =='__main__':
    main()

