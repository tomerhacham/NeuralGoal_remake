import pandas
import csv
import numpy as np
from bs4 import BeautifulSoup
import requests
import time
from Persistent.Data.utils import getNameToFifaIndex

def column_index(df, query_cols):
    cols = df.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols,query_cols,sorter=sidx)]


def run(leagueName,round,startYear,endYear):

    startY =[startYear]
    endY = [endYear]

    #startY =[14,15,16,17,18]
    #endY = [15,16,17,18,19]


    for index in range(len(startY)):

        current_league = leagueName
        MAIN_URL = "https://www.fifaindex.com/teams/fifa"
        start_year = startY[index]
        end_year = endY[index]
        sY = start_year
        eY = end_year

        if(start_year < 10):
            start_year = "0" + str(start_year)
        if(end_year < 10):
            end_year = "0" + str(end_year)

        table = []

        def getNormalOdds(Home,Draw,Away):
            _rH = 1/float(Home)
            _rD = 1/float(Draw)
            _rA = 1/float(Away)
            _r = _rH + _rD + _rA
            return _r

        def getWinner (home_goals,away_goals):   
            try:
                if int(home_goals) > int(away_goals):
                    return '1'
                elif int(home_goals) == int(away_goals):
                    return 'X'
                else:
                    return '2'
            except:
                return '@@@@@@@@@@@'


        try:
            team_stat = pandas.read_csv(current_league + "-" + str(start_year) + "-" + str(end_year) + ".csv",parse_dates=True)
        except:
            print(str(start_year) + " " + str(end_year) + " Curropt")
            continue

        for index, row in team_stat.iterrows():
            
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
            headers = {'User-Agent': user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

            gameDate = str(row[int(column_index(team_stat, ['Date'])[0])])
            homeNameTeam = str(row[int(column_index(team_stat, ['HomeTeam'])[0])])
            awayNameTeam = str(row[int(column_index(team_stat, ['AwayTeam'])[0])])

            homeNameTeam,awayNameTeam = getNameToFifaIndex(homeNameTeam,awayNameTeam)

            if int(end_year) < 10 :
                urlHomeTeam = MAIN_URL + "0" + str(eY) + "/?name=" + homeNameTeam
                urlAwayTeam = MAIN_URL + "0" + str(eY) + "/?name=" + awayNameTeam
            else:
                urlHomeTeam = MAIN_URL + str(eY) + "/?name=" + homeNameTeam
                urlAwayTeam = MAIN_URL + str(eY) + "/?name=" + awayNameTeam
        

            dataHomeTeam = requests.get(urlHomeTeam, headers=headers)
            dataHomeTeamContenet = dataHomeTeam.content
            
            dataAwayTeam = requests.get(urlAwayTeam, headers=headers)
            dataAwayTeamContenet = dataAwayTeam.content
            
            try:    
                homeTeamData= BeautifulSoup(dataHomeTeamContenet,"html.parser")
                awayTeamData= BeautifulSoup(dataAwayTeamContenet,"html.parser")
            except:
                print("EXCEPTION " + homeNameTeam + " " + awayNameTeam)
                continue

            homeNameTeam = str(row[int(column_index(team_stat, ['HomeTeam'])[0])])
            awayNameTeam = str(row[int(column_index(team_stat, ['AwayTeam'])[0])])
            
            d = {}
            d["Game Date"] = gameDate
            d["Home Team"] = homeNameTeam
            d["Away Team"] = awayNameTeam

            try:
                d["Home ATT"] = homeTeamData.find("td",{"data-title":"ATT"}).text
                d["Away ATT"] = awayTeamData.find("td",{"data-title":"ATT"}).text
                d["Home DEF"] = homeTeamData.find("td",{"data-title":"DEF"}).text
                d["Away DEF"] = awayTeamData.find("td",{"data-title":"DEF"}).text
                d["Home MID"] = homeTeamData.find("td",{"data-title":"MID"}).text
                d["Away MID"] = awayTeamData.find("td",{"data-title":"MID"}).text
            except:
                print("EXCEPTION " + homeNameTeam + " " + awayNameTeam)
                continue
            _homeWinOdds = 0
            _drawOdds = 0
            _awayWinOdds = 0

            startI = int(column_index(team_stat, ['B365H'])[0])
            Counter = 0
            for x in range(startI, startI+(6*3), 3):
                if not pandas.isna(team_stat.iloc[index,x]):
                    Counter = Counter + 1
                    _homeWinOdds += row[x]
                    _drawOdds += row[int(x)+1]
                    _awayWinOdds += row[int(x)+2]
            if Counter == 0:
                break
            else:
                _R = getNormalOdds(_homeWinOdds/Counter,_drawOdds/Counter,_awayWinOdds/Counter)
                HwinOdds = (1/(_homeWinOdds/Counter))/_R
                DrawOdds = (1/(_drawOdds/Counter))/_R
                AwinOdds = (1/(_awayWinOdds/Counter))/_R

            d["Home Win Odds"] = HwinOdds
            d["Draw Odds"] = DrawOdds
            d["Away Win Odds"] = AwinOdds

            FTHG = int(row[int(column_index(team_stat, ['FTHG'])[0])])
            FTAG = int(row[int(column_index(team_stat, ['FTAG'])[0])])
            d["Winner"] = getWinner(FTHG,FTAG)

            d["Home win Odds not normal"] = (_homeWinOdds/Counter)
            d["Draw Odds not normal"] = (_drawOdds/Counter)
            d["Away win Odds not normal"] = (_awayWinOdds/Counter)

            print(index,homeNameTeam,awayNameTeam)

            table.append(d)

        df = pandas.DataFrame(table)
        df.to_csv(current_league + "-" + str(sY) + "-" + str(eY) + "-" + "Final-Stats" + ".csv")