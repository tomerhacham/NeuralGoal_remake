import time

import numpy as np
import pandas as pd
from Persistent.repository import Repository
from NeuralNetwork.DataProccess import data_preprocessor
from NeuralNetwork import neuralnet
import platform

predictions=[]
repo=Repository()


#y_pred is numpy array
#y_test is pandas dataframe
def apply_indexes(y_pred, y_test):
    indexes = list(y_test.index.values.tolist())
    y_pred_df = pd.DataFrame(data=y_pred, index=indexes, columns=['pred_1','pred_2','pred_X'])
    return y_pred_df,indexes


#region Data
data=repo.main_table.select_all()
#upcoming_games = repo.upcoming_games()

BundesligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Bundesliga",9)
eredivisiteUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Eredivisie",9)
jupilerUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Jupiler",10)
laligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Laliga",10)
ligue1UpcomingGames = repo.upcoming_games.select_by_league_name_limited("Ligue1",10)
premierLeagueUpcomingGames = repo.upcoming_games.select_by_league_name_limited("PremierLeague",10)
serieUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Serie",10)

toPredit = [BundesligaUpcomingGames,eredivisiteUpcomingGames,jupilerUpcomingGames,laligaUpcomingGames,
            ligue1UpcomingGames,premierLeagueUpcomingGames,serieUpcomingGames]
toPredit = pd.concat(toPredit,ignore_index=False)
toPredit.to_csv('test.csv',index=False)

x,y = data_preprocessor.train_preprocess(data)
to_predict = data_preprocessor.prediction_preprocess(toPredit)
#endregion
#region ANN
avg = 1
epoc = 1
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
y_pred, indexes =apply_indexes(avgPrediction,toPredit)
details=toPredit.iloc[indexes]
details=details[['league','date','home_team_name','away_team_name']]
final = pd.concat([details,y_pred],axis=1,sort=False)

slashDirection = "\\"
if platform.system() == "Darwin":
    slashDirection = "//"

final.to_csv('outputs{}predictions-{}.csv'.format(slashDirection,(int)(time.time())),index=False)
#endregion


