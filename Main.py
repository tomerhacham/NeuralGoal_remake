import numpy as np
import pandas as pd
from Persistent.repository import Repository
from NeuralNetwork.DataProccess import data_preprocessor
from NeuralNetwork import neuralnet
predictions=[]
repo=Repository()
#region Data
#data=repo.main_table.select_all()
#upcoming_games = repo.upcoming_games()

BundesligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Bundesliga",9)
eredivisiteUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Eredivisie",9)
jupilerUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Jupiler",10)
laligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Laliga",10)
ligue1UpcomingGames = repo.upcoming_games.select_by_league_name_limited("Ligue1",10)
premierLeagueUpcomingGames = repo.upcoming_games.select_by_league_name_limited("PremierLeague",10)
serieUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Serie",10)

toPredit = [BundesligaUpcomingGames,eredivisiteUpcomingGames,jupilerUpcomingGames,laligaUpcomingGames,laligaUpcomingGames,ligue1UpcomingGames,premierLeagueUpcomingGames,serieUpcomingGames]
toPredit = pd.concat(toPredit,ignore_index=False)
toPredit.to_csv('test',index=False)

x,y = data_preprocessor.train_preprocess(data)
to_predict = data_preprocessor.prediction_preprocess(upcoming_games)
#TODO:complite script to load relevent game each batch
#endregion
#region ANN
for i in range(0,50):
    ann = neuralnet.neuralnet(x.shape[1])
    ann.train(x,y,300)
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
        avgPrediction[line, cell] = sum/50
#endregion
#region Converting avgPrediction to pandas DataFrame
avgPrediction.T[[1, 2]] = avgPrediction.T[[2, 1]] #flipping the X with 2 so the output is 1|x|2
pred_df = pd.DataFrame(avgPrediction)
pred_df.columns = {'1','X','2'}
#endregion


