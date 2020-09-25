import glob

from Persistent.Data import _BettingStats, _fromWinnerToPrediction  # 1
from Persistent.Data import _teamsGoalsScoredReceived  # 2
from Persistent.Data import _teamsGoalsScoredReceivedNormal  # 3
from Persistent.Data import _combineStanding  # 4
from Persistent.Data import _combineGoalsAadStanding  # 5
from Persistent.Data import _GetCorrentRound  # 6
from Persistent.Data import _UpcomingBettingOddsWithAPI  # 7
from Persistent.Data import _updateFiles  # 8
from Persistent.Data import _UpcomingFromWinner
from Persistent.Data import newLeagueValidation  # for adding new leagues
from Persistent.Data.utils import getRoundPerLeague
import os
import sqlite3
import sys
import os
import pandas
import platform

from Persistent import dto, repository


def getData(leagues, years):
    for League in range(len(leagues)):
        for year in range(len(years)):
            startYear = years[year]
            endYear = startYear + 1
            startYear_C = startYear
            endYear_C = endYear

            league = str(leagues[League])
            _round = getRoundPerLeague(league, startYear)

            if startYear < 10:
                startYear_C = "0" + str(startYear)
            if endYear < 10:
                endYear_C = "0" + str(endYear)

            #Download All games until the current round from https://www.football-data.co.uk/
            _updateFiles.run(league, startYear_C, endYear_C)

            #{League name}-20-21-Final-Stats
            _BettingStats.run(league, _round, startYear, endYear)

            #standing-20-21
            _teamsGoalsScoredReceived.run(league, _round, startYear, endYear)

            #standing-8-9-AVG
            _teamsGoalsScoredReceivedNormal.run(league, _round, startYear, endYear)

            #standing-8-9-Teams
            _combineStanding.run(league, _round, startYear, endYear)

            # {League}-8-9-Goals-AVG3
            _combineGoalsAadStanding.run(league, _round, startYear, endYear)

            _updateFiles.combineToFinal(league, startYear, endYear)
            _updateFiles.cleanAllFile(league, startYear, endYear)

            os.remove(league + "-" + str(startYear_C) + "-" + str(endYear_C) + ".csv")

            print("Finished the run successfully !!!")


def RunPrediction(leagues, years):
    for League in range(len(leagues)):
        for year in range(len(years)):
            startYear = years[year]

            league = str(leagues[League])

            #_GetCorrentRound.run(league, startYear)
            #_UpcomingBettingOddsWithAPI.run(league)
            #_fromWinnerToPrediction.run(league)

            print("Finished the run successfully !!!")


def addToUpcoming(leagues):
    repo = repository.Repository()

    for league in leagues:

        #csvFilePath = "C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\{} stats\\Final\\{}-20-21-Final.csv".format(league,league)

        # Not For Predict !
        for name in glob.glob('C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\Prediction\\{}R*.csv'.format(league)):
            csvFilePath = name

        tableToAdd = pandas.read_csv(csvFilePath, parse_dates=True, index_col=0)
        for index, row in tableToAdd.iterrows():

            _date = tableToAdd['date'][index]
            #_date = tableToAdd['Game Date'][index]

            _day = _date.split('/')[0]
            _month = _date.split('/')[1]
            _year = _date.split('/')[2]

            if len(_year) == 2:
                _year = "20" + str(_year)

            _date = _year + '-' + _month + '-' + _day



            _home_team_name = tableToAdd['home_team_name'][index]
            #_home_team_name = tableToAdd['Home Team'][index]
            _away_team_name = tableToAdd['away_team_name'][index]
            #_away_team_name = tableToAdd['Away Team'][index]

            _home_team_rank = int(tableToAdd['home_team_rank'][index])
            #_home_team_rank = int(tableToAdd['Home Team Rank'][index])
            _away_team_rank = int(tableToAdd['away_team_rank'][index])
            #_away_team_rank = int(tableToAdd['Away Team Rank'][index])

            _home_team_scored = tableToAdd['home_team_scored'][index]
            #_home_team_scored = tableToAdd['Home Team Scored Goals'][index]
            _away_team_scored = tableToAdd['away_team_scored'][index]
            #_away_team_scored = tableToAdd['Away Team Scored Goals'][index]

            _home_team_received = tableToAdd['home_team_received'][index]
            #_home_team_received = tableToAdd['Home Team Received Goals'][index]
            _away_team_received = tableToAdd['away_team_received'][index]
            #_away_team_received = tableToAdd['Away Team received Goals'][index]

            _home_att = int(tableToAdd['home_att'][index])
            #_home_att = int(tableToAdd['Home ATT'][index])
            _away_att = int(tableToAdd['away_att'][index])
            #_away_att = int(tableToAdd['Away ATT'][index])

            _home_def = int(tableToAdd['home_def'][index])
            #_home_def = int(tableToAdd['Home DEF'][index])
            _away_def = int(tableToAdd['away_def'][index])
            #_away_def = int(tableToAdd['Away DEF'][index])

            _home_mid = int(tableToAdd['home_mid'][index])
            #_home_mid = int(tableToAdd['Home MID'][index])
            _away_mid = int(tableToAdd['away_mid'][index])
            #_away_mid = int(tableToAdd['Away MID'][index])

            _home_odds_n = tableToAdd['home_odds_n'][index]
            #_home_odds_n = tableToAdd['Home Win Odds'][index]
            _draw_odds_n = tableToAdd['draw_odds_n'][index]
            #_draw_odds_n = tableToAdd['Draw Odds'][index]
            _away_odds_n = tableToAdd['away_odds_n'][index]
            #_away_odds_n = tableToAdd['Away Win Odds'][index]

            _result = ""

            _home_odds_nn = tableToAdd['home_odds_nn'][index]
            #_home_odds_nn = tableToAdd['Home win Odds not normal'][index]
            _draw_odds_nn = tableToAdd['draw_odds_nn'][index]
            #_draw_odds_nn = tableToAdd['Draw Odds not normal'][index]
            _away_odds_nn = tableToAdd['away_odds_nn'][index]
            #_away_odds_nn = tableToAdd['Away win Odds not normal'][index]

            _round = int(tableToAdd['round'][index])
            #_round = 1
            _leagueName = tableToAdd['league'][index]
            #_leagueName = league

            gameToAdd = dto.match(_leagueName, _date, _round, _home_team_name, _away_team_name,
                                  _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                                  _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
                                  _away_def,
                                  _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
                                  _home_odds_nn, _draw_odds_nn, _away_odds_nn)
            try:
                repo.upcoming_games.insert(gameToAdd)
                print(
                    '{} game added to db - {} - {} vs {}'.format(_date, _leagueName, _home_team_name, _away_team_name))
            except:
                print('game is already in db - {} - {} vs {}'.format(_leagueName, _home_team_name, _away_team_name))
                continue


def addToUMain(leagues, years):
    repo = repository.Repository()

    for league in leagues:
        for year in years:

            sY = year
            eY = year + 1
            csvFilePath = ""
            for name in glob.glob(
                    'C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\{} stats\\Final\\{}-{}-{}-Final.csv'.format(
                        league, league, str(sY), str(eY))):
                csvFilePath = name

            roundCounter = 1
            tableToAdd = pandas.read_csv(csvFilePath, parse_dates=True, index_col=0)
            for index, row in tableToAdd.iterrows():
                _date = tableToAdd['Game Date'][index]

                _day = _date.split('/')[0]
                _month = _date.split('/')[1]
                _year = _date.split('/')[2]


                if len(_year) == 2:
                    _year = "20" + str(_year)

                _date = _year + '-' + _month + '-' +_day

                _home_team_name = tableToAdd['Home Team'][index]
                _away_team_name = tableToAdd['Away Team'][index]

                _home_team_rank = int(tableToAdd['Home Team Rank'][index])
                _away_team_rank = int(tableToAdd['Away Team Rank'][index])

                _home_team_scored = tableToAdd['Home Team Scored Goals'][index]
                _away_team_scored = tableToAdd['Away Team Scored Goals'][index]

                _home_team_received = tableToAdd['Home Team Received Goals'][index]
                _away_team_received = tableToAdd['Away Team received Goals'][index]

                _home_att = int(tableToAdd['Home ATT'][index])
                _away_att = int(tableToAdd['Away ATT'][index])

                _home_def = int(tableToAdd['Home DEF'][index])
                _away_def = int(tableToAdd['Away DEF'][index])

                _home_mid = int(tableToAdd['Home MID'][index])
                _away_mid = int(tableToAdd['Away MID'][index])

                _home_odds_n = tableToAdd['Home Win Odds'][index]
                _draw_odds_n = tableToAdd['Draw Odds'][index]
                _away_odds_n = tableToAdd['Away Win Odds'][index]

                _result = str(tableToAdd['Winner'][index])

                _home_odds_nn = tableToAdd['Home win Odds not normal'][index]
                _draw_odds_nn = tableToAdd['Draw Odds not normal'][index]
                _away_odds_nn = tableToAdd['Away win Odds not normal'][index]

                _round = int(roundCounter / 9) + 1
                _leagueName = league
                roundCounter = roundCounter + 1

                gameToAdd = dto.match(_leagueName, _date, _round, _home_team_name, _away_team_name,
                                      _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                                      _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
                                      _away_def,
                                      _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
                                      _home_odds_nn, _draw_odds_nn, _away_odds_nn)
                try:
                    repo.main_table.insert(gameToAdd)
                    print('{} game added to db - {} - {} vs {}'.format(_date,_leagueName, _home_team_name, _away_team_name))
                except:
                    print('game is already in db - {} - {} vs {}'.format(_leagueName,_home_team_name,_away_team_name))
                    continue


if __name__ == "__main__":
    leagues = ["Serie", "PremierLeague", "Bundesliga", "Laliga", "Ligue1", "Jupiler", "Eredivisie" , "Scotish" , "Portugal" , "Turkey"]
    #leagues = [ "PremierLeague", "Laliga", "Ligue1", "Jupiler", "Eredivisie" , "Scotish", "Turkey"]
    #leagues = ["Turkey","Scotish"]


    #years = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    years = [20]

    #getData(leagues, years)
    #addToUMain(leagues,years)

    #RunPrediction(leagues,years)

    addToUpcoming(leagues)
