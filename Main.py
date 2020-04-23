import time

import numpy as np
import pandas as pd
from Persistent.repository import Repository
from NeuralNetwork.DataProccess import data_preprocessor
from NeuralNetwork import neuralnet
predictions=[]
repo=Repository()
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
pred_df = pd.DataFrame(avgPrediction)
pred_df.columns = {'Pred 1','Pred 2','Pred X'}
pred_df.reset_index(drop=False, inplace=True)
toPredict = toPredit.loc[:, 'league':'away_team_name']
toPredict.reset_index(drop=False, inplace=True)
final = pd.concat([toPredict,pred_df],axis=1)
final.to_csv('outputs\\predictions-{}.csv'.format((int)(time.time())),index=False)
#endregion


