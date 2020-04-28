import time

import numpy as np
import pandas as pd
from Persistent.repository import Repository
from NeuralNetwork.DataProccess import data_preprocessor
from NeuralNetwork import neuralnet
import platform



#y_pred is numpy array
#y_test is pandas dataframe
def apply_indexes(y_pred, y_test):
    indexes = list(y_test.index.values.tolist())
    y_pred_df = pd.DataFrame(data=y_pred, index=indexes, columns=['pred_1','pred_2','pred_X'])
    return y_pred_df,indexes


def makePredictions(_round):
    predictions = []
    repo = Repository()
    #region Data
    data=repo.main_table.select_all()
    upcoming_games=repo.upcoming_games.select_by_league_by_round(_round)

    x,y = data_preprocessor.train_preprocess(data)
    to_predict = data_preprocessor.prediction_preprocess(upcoming_games)
    #endregion
    #region ANN
    avg = 30
    epoc = 30
    for i in range(0,avg):
        ann = neuralnet.neuralnet(x.shape[1])
        ann.train(x,y,epoc)
        predictions.append(ann.predict(to_predict))
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
            avgPrediction[line, cell] = sum/avg
    #endregion
    #region Converting avgPrediction to pandas DataFrame
    y_pred, indexes =apply_indexes(avgPrediction,upcoming_games)
    details=upcoming_games.iloc[indexes]
    details=details[['league','date','home_team_name','away_team_name','home_odds_nn','draw_odds_nn','away_odds_nn']]
    final = pd.concat([details,y_pred],axis=1,sort=False)

    slashDirection = "\\"
    if platform.system() == "Darwin":
        slashDirection = "//"

    pathToSave = 'outputs{}predictions-Week-{}.csv'.format(slashDirection,_round)
    final.to_csv(pathToSave,index=False)

    return upcoming_games
    #endregion


