import time

import numpy as np
import pandas as pd

from NeuralNetwork import neuralnet
from NeuralNetwork.DataProccess import data_preprocessor
from Persistent.repository import Repository

#y_pred is numpy array
#y_test is pandas dataframe
def apply_indexes(y_pred, y_test):
    indexes = list(y_test.index.values.tolist())
    y_pred_df = pd.DataFrame(data=y_pred, index=indexes, columns=['pred_1(0)','pred_2(1)','pred_X(2)'])
    return y_pred_df,indexes

predictions=[]
repo=Repository()
Number_Of_Runs=1

#region Data
data=repo.main_table.select_all(as_dataframe=True)
x_train, x_test, y_train, y_test = data_preprocessor.train_preprocess(data,True)
#endregion
#region ANN
for i in range(0,Number_Of_Runs):
    ann = neuralnet.neuralnet(x_train.shape[1])
    ann.train(x_train,y_train,1)
    predictions.append(ann.predict(x_test))
#endregion
#region Calculate avg of predictions
lines = predictions[0].shape[0]
columns = predictions[0].shape[1]
avgPrediction = np.zeros((lines, columns))
for line in range(lines):
    for cell in range(columns):
        sum = 0
        for prediction in predictions:
            sum = sum + prediction[line, cell]
        avgPrediction[line, cell] = sum/Number_Of_Runs
#endregion
#region Converting avgPrediction to pandas DataFrame

y_pred,indexes = apply_indexes(avgPrediction,y_test)
details=data.iloc[indexes]
details=details[['league','date','home_team_name','away_team_name','result']]
final = pd.concat([details,y_pred,y_test],axis=1,sort=False)
final.to_csv('outputs\\predictions-all-db-{}.csv'.format((int)(time.time())))
#endregion


