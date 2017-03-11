
# coding: utf-8

# ## Support Vector Regression using Scikit-Learn
# 
# Given a regression task, use scikit-learn to use support vector regression in it. 
# 
# **Tools used:** Pandas, Numpy 

# In[2]:

#Import the dependencies 

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split


#Import the data 
train_data = pd.read_csv("dataset/train.csv")

#Clean the data
train_data.drop('idx',axis=1,inplace=True)
train_data_phase=[]
for i in xrange(1,8):
    train_ph = train_data[train_data["PH"] == i]
    train_ph.drop("PH",axis=1,inplace=True)
    train_data_phase.append(train_ph)
    


# In[3]:

#Split the datasets
X_train=[]
X_test = []
y_train=[]
y_test = []

for i in xrange(0,7):
    train,test=train_test_split(train_data_phase[i], test_size = 0.20)
    y_train.append(train.ix[:,train.columns == "FF"])
    y_test.append(test.ix[:,test.columns == "FF"])
    X_train.append(train.ix[:, train.columns != "FF"])
    X_test.append(test.ix[:,test.columns != "FF"])


# In[4]:

#Initialise the regressors
list_svr = []
for i in xrange(0,7):
    list_svr.append(svm.SVR())
    list_svr[i].fit(X_train[i],y_train[i])


# In[5]:

#Calculate the test predictions
y_pred = []
for i in xrange(0,7):
    y_pred.append(list_svr[i].predict(X_test[i]))


# In[6]:

#Calculate the accuracy
from sklearn.metrics import mean_squared_error
error = 0
for i in xrange(0,7):
    error = error + mean_squared_error(y_test[i],y_pred[i])
error = error / 7.0
print error**(1./3.)  #Just a crude metric to visualise the accuracy, has no physical meaning


# In[131]:

# Get in the test data and storing the order
test_data = pd.read_csv("dataset/test.csv")
print test_data.head()
#cleaning the data and splitting across each PH
test_data.drop('idx',axis=1,inplace=True)
test_data_phase = []
for i in xrange(1,8):
    test = test_data[test_data["PH"]==i]
    test_data_phase.append(test)
    test_data_phase[i-1].drop('PH',axis=1,inplace=True)


# In[132]:

assert sum(test_data_phase[i].shape[0] for i in range(0,7)) == test_data.shape[0]


# In[133]:

#Predict using the individual regressors
y_pred_test = []
for i in xrange(0,7):
    y_pred_test.append(list_svr[i].predict(test_data_phase[i]))


# In[134]:

#write the submission
submission = np.empty([test_data.shape[0]],dtype=float)
for i in xrange(1,8):
    submission[test_data[test_data["PH"]==i].index] = y_pred_test[i-1]


# In[151]:

#Save it to text file
np.savetxt("out.txt",np.ceil(submission),fmt="%d")

