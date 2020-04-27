from MakePrediction import makePredictions
from Persistent import dto
from Persistent.repository import Repository
import platform
import pandas
import os

repo=Repository()
currentDirectory = os.getcwd()

slashDirection = "\\"
if platform.system() == "Darwin":
    slashDirection = "//"

def resultForGame(_date,home_team_name,away_team_name,league):
    filePath = currentDirectory + '{}Persistent{}Data{}{} stats{}Final{}{}-19-20-Final.csv'.format(slashDirection,slashDirection,slashDirection,league,slashDirection,slashDirection,league)
    tableToRead = pandas.read_csv(filePath, parse_dates=True)
    date = _date.replace('-', '/')
    date = date.split('/')
    date = str(date[2]) + "/" + str(date[1]) + "/"  + str(date[0])
    for index, row in tableToRead.iterrows():
        if row[1] == date:
            if row[2] == home_team_name:
                if row[3] == away_team_name:
                    return row[13]
    return -1


for round in range(20):
    round = round +1
    gamesToMainTable = makePredictions(round)
    for ind in gamesToMainTable.index:

        leagueName = gamesToMainTable['league'][ind]
        _date = gamesToMainTable['date'][ind]
        gameCounter = int(gamesToMainTable['round'][ind])

        _home_team_name = gamesToMainTable['home_team_name'][ind]
        _away_team_name = gamesToMainTable['away_team_name'][ind]

        _home_team_rank = int(gamesToMainTable['home_team_rank'][ind])
        _away_team_rank = int(gamesToMainTable['away_team_rank'][ind])

        _home_team_scored = gamesToMainTable['home_team_scored'][ind]
        _away_team_scored = gamesToMainTable['away_team_scored'][ind]

        _home_team_received = gamesToMainTable['home_team_received'][ind]
        _away_team_received = gamesToMainTable['away_team_received'][ind]

        _home_att = int(gamesToMainTable['home_att'][ind])
        _away_att = int(gamesToMainTable['away_att'][ind])

        _home_def = int(gamesToMainTable['home_def'][ind])
        _away_def = int(gamesToMainTable['away_def'][ind])

        _home_mid = int(gamesToMainTable['home_mid'][ind])
        _away_mid = int(gamesToMainTable['away_mid'][ind])

        _home_odds_n = gamesToMainTable['home_odds_n'][ind]
        _draw_odds_n = gamesToMainTable['draw_odds_n'][ind]
        _away_odds_n = gamesToMainTable['away_odds_n'][ind]

        _home_odds_nn = gamesToMainTable['home_odds_nn'][ind]
        _draw_odds_nn = gamesToMainTable['draw_odds_nn'][ind]
        _away_odds_nn = gamesToMainTable['away_odds_nn'][ind]



        _result = resultForGame(_date,_home_team_name,_away_team_name,leagueName)

        if _result == -1:
            print("Cant find")

        gameToAdd = dto.match(leagueName, _date, gameCounter, _home_team_name, _away_team_name,
                              _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                              _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
                              _away_def,
                              _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
                              _home_odds_nn, _draw_odds_nn, _away_odds_nn)

        repo.upcoming_games.delete(_date,_home_team_name,_away_team_name)
        repo.main_table.insert(gameToAdd)



