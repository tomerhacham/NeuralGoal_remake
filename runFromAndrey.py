import numpy as np
import pandas as pd

from NeuralNetwork import neuralnet
from NeuralNetwork.DataProccess import data_preprocessor
from Persistent.repository import Repository

predictions=[]
repo=Repository()

#region Data
data=repo.main_table.select_all()
x_train, x_test, y_train, y_test = data_preprocessor.train_preprocess(data,True)
#endregion
#region ANN
for i in range(0,50):
    ann = neuralnet.neuralnet(x_train.shape[1])
    ann.train(x_train,y_train,300)
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
        avgPrediction[line, cell] = sum/50
#endregion
#region Converting avgPrediction to pandas DataFrame
avgPrediction.T[[1, 2]] = avgPrediction.T[[2, 1]] #flipping the X with 2 so the output is 1|x|2
pred_df = pd.DataFrame(avgPrediction)
pred_df.columns = {'1','X','2'}
#endregion


