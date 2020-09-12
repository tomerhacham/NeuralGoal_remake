import sqlite3
import sys
import os
import pandas
import platform

from Persistent import dto, repository

#leagues = ['Serie', 'PremierLeague', 'Bundesliga', 'Laliga', 'Ligue1', 'Jupiler', 'Eredivisie', "Scotish" , "Portugal"]
leagues = ['Scotish']

repo = repository.Repository()
years = [20]
#years = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,19]

slashDirection = "\\"
if platform.system() == "Darwin":
    slashDirection = "//"

for leagueName in leagues:
    for year in years:
        try:
            currentDirectory = os.getcwd()
            # filePath = currentDirectory + "{}Persistent{}Data{}{} stats{}Final{}{}-{}-{}-Final.csv".format(
            #      slashDirection, slashDirection, slashDirection, leagueName, slashDirection, slashDirection, leagueName,
            #      str(year), str(year + 1))

            filePath = currentDirectory + "\\predict.csv"

            tableToAdd = pandas.read_csv(filePath, parse_dates=True)
            gameCounter = 1
            counter = 1
            for index, row in tableToAdd.iterrows():
                print(counter)
                _date = row[1]
                splitedDate = _date.split("/")  # output -> DD MM YYYY
                if (len(splitedDate[2]) == 2):
                    splitedDate[2] = "20" + str(splitedDate[2])
                _day = str(splitedDate[0])
                _month = str(splitedDate[1])
                _yaer = str(splitedDate[2])

                _date = _yaer + "-" + _month + "-" + _day
                # convert string to date time format

                #_home_team_name = row[2]
                _home_team_name = row[4]
                #_away_team_name = row[3]
                _away_team_name = row[5]

                #_home_team_rank = row[17]
                _home_team_rank = row[6]
                #_away_team_rank = row[18]
                _away_team_rank = row[7]

                #_home_team_scored = row[19]
                _home_team_scored = row[14]
                #_away_team_scored = row[21]
                _away_team_scored = row[16]

                #_home_team_received = row[20]
                _home_team_received = row[15]
                #_away_team_received = row[22]
                _away_team_received = row[17]

                #_home_att = row[4]
                _home_att = row[8]
                #_away_att = row[5]
                _away_att = row[9]

                #_home_def = row[6]
                _home_def = row[10]
                #_away_def = row[7]
                _away_def = row[11]

                #_home_mid = row[8]
                _home_mid = row[12]
                #_away_mid = row[9]
                _away_mid = row[13]

                #_home_odds_n = row[10]
                _home_odds_n = row[18]
                #_draw_odds_n = row[11]
                _draw_odds_n = row[19]
                #_away_odds_n = row[12]
                _away_odds_n = row[20]

                #_result = row[13]
                _result = ""

                #_home_odds_nn = row[14]
                _home_odds_nn = row[21]
                #_draw_odds_nn = row[15]
                _draw_odds_nn = row[22]
                #_away_odds_nn = row[16]
                _away_odds_nn = row[23]

                #_round = gameCounter
                _round = row[3]
                #_leagueName = leagueName
                _leagueName = row[2]

                gameToAdd = dto.match(leagueName, _date, _round, _home_team_name, _away_team_name,
                                      _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                                      _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
                                      _away_def,
                                      _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
                                      _home_odds_nn, _draw_odds_nn, _away_odds_nn)

                if leagueName == 'Bundesliga':
                    if counter % 9 == 0:
                        gameCounter = gameCounter + 1
                elif leagueName == 'Eredivisie':
                    if counter % 9 == 0:
                        gameCounter = gameCounter + 1
                elif leagueName == 'Scotish':
                    if counter % 6 == 0:
                        gameCounter = gameCounter + 1
                else:
                    if counter % 10 == 0:
                        gameCounter = gameCounter + 1

                repo.upcoming_games.insert(gameToAdd)
                #repo.main_table.insert(gameToAdd)
                counter = counter + 1

        except:
            continue
