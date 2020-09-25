import os

import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
import time
from Persistent.Data.utils import getRoundPerLeague, getLastYearRound, gamesInRoundByLeagueName


def run(leagueName,round,startYear,endYear):

    startY = [startYear]
    endY = [endYear]

    for x in range(len(startY)):

        sY = str(startY[x])
        eY = str(endY[x])

        sYL = str(startY[x]-1)
        eYL = str(endY[x]-1)

        table = []
        rows = []

        team_standing = pandas.read_csv("standing-" + sY + "-" + eY + "-AVG.csv")

        if leagueName == "Turkey":
            if sY != '14' and sY != '6':
                currentWD = os.getcwd()
                destinationPath = currentWD + "\\" + leagueName + " stats\\Stats For {}-{}\\".format(sYL,eYL) + "standing-" + sYL + "-" + eYL + "-AVG.csv"
                team_standing_lastYear = pandas.read_csv(destinationPath)
                lastRoundIndex = team_standing_lastYear.shape[0] - 1
        elif sY != "5":
            currentWD = os.getcwd()
            destinationPath = currentWD + "\\" + leagueName + " stats\\Stats For {}-{}\\".format(sYL,eYL) + "standing-" + sYL + "-" + eYL + "-AVG.csv"
            team_standing_lastYear = pandas.read_csv(destinationPath)
            lastRoundIndex = team_standing_lastYear.shape[0]-1
        for index, row in team_standing.iterrows():
            rows.append(row)

        _Range = getLastYearRound(leagueName,int(sY)) + 2
        t = []
        counter = 0


        for row in rows:
            d = {}
            # First round - Take the average of the last 3 games of last year
            # if no data - "-1" will be entered
            if(counter == 0):
                for x in range(0,_Range):
                    try:
                        if sY == "5":
                            name = list(team_standing.columns)[x + 1]
                            d[name] = 1
                        else:
                            name = list(team_standing.columns)[x + 1]
                            lastRoundForTeam = team_standing_lastYear[name][lastRoundIndex]
                            lastRoundForTeamMinus1 = team_standing_lastYear[name][lastRoundIndex-1]
                            lastRoundForTeamMinus2 = team_standing_lastYear[name][lastRoundIndex-2]
                            d[name] = ((lastRoundForTeam+lastRoundForTeamMinus1+lastRoundForTeamMinus2)/3)
                    except:
                        continue
            # Second round - Take the average of the last 2 games of last year and the first round of the current year
            elif(counter == 1):
                for x in range(0,_Range):
                    try:
                        if sY == "5":
                            name = list(team_standing.columns)[x + 1]
                            d[name] = 1
                        else:
                            name = list(team_standing.columns)[x+1]
                            lastRoundForTeam = team_standing_lastYear[name][lastRoundIndex]
                            lastRoundForTeamMinus1 = team_standing_lastYear[name][lastRoundIndex - 1]
                            d[name] = (row[x+1] + lastRoundForTeam + lastRoundForTeamMinus1)/3
                    except:
                        continue
            # Third round - Take the average of the last game of last year and the first 2 rounds of the current year
            elif(counter==2):
                for x in range(0,_Range):
                    try:
                        if sY == "5":
                            name = list(team_standing.columns)[x + 1]
                            d[name] = 1
                        else:
                            name = list(team_standing.columns)[x+1]
                            d[name] = (row[x+1] + rows[counter-1][x+1] + team_standing_lastYear[name][lastRoundIndex])/3
                    except:
                        continue
            # Fourth and Greater - Take last 3 games
            else:
                for x in range(0,_Range):
                    try:
                        name = list(team_standing.columns)[x+1]
                        x11 = row[x+1]
                        x22 = rows[counter-1][x+1]
                        x33 = rows[counter-2][x+1]
                        d[name] = (row[x+1] + rows[counter-1][x+1] + rows[counter-2][x+1])/3
                    except:
                        continue
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
            
            homeTeam = str(row[2]).rstrip()
            awayTeam = str(row[3]).rstrip()
            
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
                try:
                    d["Home Team Rank"] = int((team_rank == homeTeam).idxmax(axis=1)[roundCounter]) + 1
                except:
                    d["Home Team Rank"] = int(0.83*gamesInRoundByLeagueName(leagueName)*2)
                try:
                    d["Away Team Rank"] = int((team_rank == awayTeam).idxmax(axis=1)[roundCounter]) + 1
                except:
                    d["Away Team Rank"] = int(0.83*gamesInRoundByLeagueName(leagueName)*2)
                d["Home Team Scored Goals"] = Hscored 
                d["Home Team Received Goals"] = Hrecived
                d["Away Team Scored Goals"] = Ascored
                d["Away Team received Goals"] =Arecived 
            except:
                continue
            _leaguRound = 0
            if leagueName == "Bundesliga" or leagueName == "Eredivisie":
                _leaguRound = 9

            elif leagueName == "Portugal":
                if startYear <= 5:
                    _leaguRound = 9
                elif startYear <= 13:
                    _leaguRound = 8
                else:
                    _leaguRound = 9
            elif leagueName == "Scotish":
                _leaguRound = 6

            elif leagueName == "Jupiler":
                _leaguRound = 9
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