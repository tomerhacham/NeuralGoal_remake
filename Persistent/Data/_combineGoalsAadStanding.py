import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
import time

def run(leagueName,round,startYear,endYear):

    startY = [startYear]
    endY = [endYear]

    for x in range(len(startY)):

        sY = str(startY[x])
        eY = str(endY[x])

        table = []
        rows = []

        team_standing = pandas.read_csv("standing-" + sY + "-" + eY + "-AVG.csv")

        for index, row in team_standing.iterrows():
            rows.append(row)
        _Range = 0
        if leagueName == "Bundesliga" or leagueName == "Eredivisie":
            _Range = 36
        elif leagueName == "Jupiler":
            if startYear <= 8:
                _Range = 36
            else:
                _Range = 32
        else:
            _Range = 40
        t = []
        counter = 0
        for row in rows:
            d = {}
            if(counter == 0):
                for x in range(0,_Range):
                    name = list(team_standing.columns)[x+1]
                    d[name] = row[x+1]
            elif(counter == 1):
                for x in range(0,_Range):
                    name = list(team_standing.columns)[x+1]
                    d[name] = (row[x+1] + rows[counter-1][x+1])/2
            else:
                for x in range(0,_Range):
                    name = list(team_standing.columns)[x+1]
                    d[name] = (row[x+1] + rows[counter-1][x+1] + rows[counter-2][x+1])/3
            counter = counter+1
            t.append(d)

        df_1 = pandas.DataFrame(t)
        df_1.to_csv("standing-" + sY + "-" + eY + "-AVG-Goals.csv")

        team_stat = pandas.read_csv(leagueName +"-" + sY + "-" + eY + "-Final-Stats.csv")
        team_standing_new = pandas.read_csv("standing-" + sY + "-" + eY + "-AVG-Goals.csv")
        team_rank = pandas.read_csv("standing-" + sY + "-" + eY + "-Teams.csv")

        roundCounter = 0
        
        for index, row in team_stat.iterrows():
            d = {}
            
            homeTeam = row[2]
            awayTeam = row[3]
            
            try:
                Hscored = team_standing_new.loc[roundCounter,str(homeTeam) + " scored"]
                Hrecived = team_standing_new.loc[roundCounter,str(homeTeam) + " received"]
                
                Ascored = team_standing_new.loc[roundCounter,str(awayTeam) + " scored"]
                Arecived = team_standing_new.loc[roundCounter,str(awayTeam) + " received"]
            except:
                Hscored = -1
                Hrecived = -1
                
                Ascored = -1
                Arecived = -1
            try:
                d["homeTeam"] = homeTeam
                d["awayTeam"] = awayTeam
                d["Home Team Rank"] = int((team_rank == homeTeam).idxmax(axis=1)[roundCounter]) + 1
                d["Away Team Rank"] = int((team_rank == awayTeam).idxmax(axis=1)[roundCounter]) + 1
                d["Home Team Scored Goals"] = Hscored 
                d["Home Team Received Goals"] = Hrecived
                d["Away Team Scored Goals"] = Ascored
                d["Away Team received Goals"] =Arecived 
            except:
                continue
            _leaguRound = 0
            if leagueName == "Bundesliga" or leagueName == "Eredivisie":
                _leaguRound = 9
            elif leagueName == "Jupiler":
                if startYear <= 8:
                    _leaguRound = 9
                else:
                    _leaguRound = 8
            else:
                _leaguRound = 10
            if index % _leaguRound == 0 and index != 0:
                roundCounter = roundCounter + 1
            if roundCounter >38 :
                roundCounter = 38


            print(index)
            table.append(d)

        df = pandas.DataFrame(table)
        df.to_csv(leagueName + "-" + sY + "-" + eY + "-Goals-AVG3.csv")