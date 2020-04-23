import time

import numpy as np
import pandas as pd

from NeuralNetwork import neuralnet
from NeuralNetwork.DataProccess import data_preprocessor
from Persistent.repository import Repository

predictions=[]
repo=Repository()
Number_Of_Runs=1

#region Data
data=repo.main_table.select_by_league_name_last_seasons('Serie')
x_train, x_test, y_train, y_test = data_preprocessor.train_preprocess(data,True)
#endregion
#region ANN
for i in range(0,Number_Of_Runs):
    ann = neuralnet.neuralnet(x_train.shape[1])
    ann.train(x_train,y_train,50)
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
#avgPrediction.T[[1, 2]] = avgPrediction.T[[2, 1]] #flipping the X with 2 so the output is 1|x|2
pred_df = pd.DataFrame(avgPrediction)
pred_df.columns = {'Pred 1','Pred 2','Pred X'}
y_test.columns = {'Actual 1', 'Actual 2', 'Actual X'}
pred_df.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)
#x_test.reset_index(drop=True, inplace=True)
final = pd.concat([pred_df,y_test],axis=1)
final.to_csv('predictions {}.csv'.format((int)(time.time())))
#endregion


