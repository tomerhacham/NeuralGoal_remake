import glob
import json
from time import sleep
from subprocess import *
import pandas
from Persistent.Data.utils import MapperWinnerToFifa, getScriptName


def run(LeagueName):


    fileName = getScriptName(LeagueName)

    p = Popen(['cypressScript.bat', fileName], stdout=PIPE, stderr=PIPE)
    output, errors = p.communicate()
    p.wait()  # wait for process to terminate

    jsonFilePath = 'C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\Prediction\\' + LeagueName + 'Winner.json'

    f = open(jsonFilePath, 'r+',encoding="utf8")
    data = json.load(f)
    games = data['table']
    Table = []
    for game in games:
        gameRow = {}

        gameRow['HomeTeamName'] = MapperWinnerToFifa(game[0]['HomeTeam'])
        gameRow['AwayTeamName'] = MapperWinnerToFifa(game[1]['AwayTeam'])
        gameRow['HomeTeamOdds'] = game[2]['HomeTeamOdds']
        gameRow['DrawOdds'] = game[3]['DrawOdds']
        gameRow['AwayTeamOdds'] = game[4]['AwayTeamOdds']

        Table.append(gameRow)

    df = pandas.DataFrame(Table)

    csvFilePath = ""
    for name in glob.glob(
            'C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\Prediction\\{}R*.csv'.format(
                LeagueName)):
        csvFilePath = name

    currentLeagueGames = pandas.read_csv(csvFilePath, parse_dates=True, index_col=0)

    for currentLeagueGamesindex, currentLeagueGamesrow in currentLeagueGames.iterrows():
        for toConcatindex, toConcatrow in df.iterrows():
            if currentLeagueGames['home_team_name'][currentLeagueGamesindex] == df['HomeTeamName'][toConcatindex] and currentLeagueGames['away_team_name'][currentLeagueGamesindex] == df['AwayTeamName'][toConcatindex]:
                currentLeagueGames['home_odds_nn'][currentLeagueGamesindex] = df["HomeTeamOdds"][
                    toConcatindex]
                currentLeagueGames['draw_odds_nn'][currentLeagueGamesindex] = df["DrawOdds"][toConcatindex]
                currentLeagueGames['away_odds_nn'][currentLeagueGamesindex] = df["AwayTeamOdds"][
                    toConcatindex]
    currentLeagueGames.fillna(0, inplace=True)
    currentLeagueGames.to_csv(csvFilePath)

