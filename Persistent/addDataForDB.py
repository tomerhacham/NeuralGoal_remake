import sqlite3
import sys
import os
import pandas

from Persistent import dto, repository
# [ Serie , PremierLeague , Bundesliga , Laliga , Ligue1, Jupiler, Eredivisie ]
leagueName = "Bundesliga"
repo = repository.Repository()
years = [19]

BundesligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Bundesliga",9)
eredivisiteUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Eredivisie",9)
jupilerUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Jupiler",10)
laligaUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Laliga",10)
ligue1UpcomingGames = repo.upcoming_games.select_by_league_name_limited("Ligue1",10)
premierLeagueUpcomingGames = repo.upcoming_games.select_by_league_name_limited("PremierLeague",10)
serieUpcomingGames = repo.upcoming_games.select_by_league_name_limited("Serie",10)

toPredit = [BundesligaUpcomingGames,eredivisiteUpcomingGames,jupilerUpcomingGames,laligaUpcomingGames,laligaUpcomingGames,ligue1UpcomingGames,premierLeagueUpcomingGames,serieUpcomingGames]
toPredit = pandas.concat(toPredit,ignore_index=True)
toPredit.to_csv('test',index=False)


for year in years:

    filePath = "{}-{}-{}-Final.csv".format(leagueName, str(year), str(year + 1))
    tableToAdd = pandas.read_csv(filePath, parse_dates=True)
    game = 0

    for index, row in tableToAdd.iterrows():
        game = game + 1
        print(game)
        _date = row[1]
        splitedDate = _date.split("/")  # output -> DD MM YYYY
        if(len(splitedDate[2])==2):
            splitedDate[2] = "20" + str(splitedDate[2])
        _day = str(splitedDate[0])
        _month = str(splitedDate[1])
        _yaer = str(splitedDate[2])

        _date = _yaer + "-" + _month + "-" + _day
        # convert string to date time format

        if leagueName == "Bundesliga":
            _round = int((game / 9) + 1)
        else:
            _round = int((game / 10) + 1)
        _home_team_name = row[2]
        _away_team_name = row[3]
        _home_team_rank = row[17]
        _away_team_rank = row[18]
        _home_team_scored = row[19]
        _away_team_scored = row[20]
        _home_team_received = row[21]
        _away_team_received = row[22]
        _home_att = row[4]
        _away_att = row[5]
        _home_def = row[6]
        _away_def = row[7]
        _home_mid = row[8]
        _away_mid = row[9]
        _home_odds_n = row[10]
        _draw_odds_n = row[11]
        _away_odds_n = row[12]
        _result = row[13]

        gameToAdd = dto.match(leagueName, _date, _round, _home_team_name, _away_team_name,
                              _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                              _home_team_received, _away_team_received, _home_att, _away_att, _home_def, _away_def,
                              _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result)
        try:
            repo.upcoming_games.insert(gameToAdd)
            #repo.main_table.insert(gameToAdd)
        except:
            continue
