import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
import time

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

            gameDate = str(row[1])
            homeNameTeam = str(row[2])
            awayNameTeam = str(row[3])

            # Bundesliga
            if homeNameTeam == "Ein Frankfurt":
                homeNameTeam = "Frankfurt&league=19"
            if awayNameTeam == "Ein Frankfurt":
                awayNameTeam = "Frankfurt&league=19"
            
            if homeNameTeam == "Bayern Munich":
                homeNameTeam = "Bayern&league=19"
            if awayNameTeam == "Bayern Munich":
                awayNameTeam = "Bayern&league=19"

            # PremierLeague
            if homeNameTeam == "Man City":
                homeNameTeam = "Manchester City"
            if awayNameTeam == "Man City":
                awayNameTeam = "Manchester City"
            
            if homeNameTeam == "Man United":
                homeNameTeam = "Manchester United"
            if awayNameTeam == "Man United":
                awayNameTeam = "Manchester United"
            
            if homeNameTeam == "Newcastle":
                homeNameTeam = "Newcastle United"
            if awayNameTeam == "Newcastle":
                awayNameTeam = "Newcastle United"
            
            # Serie
            if homeNameTeam == "Inter":
                homeNameTeam = "Inter&league=31"
            if awayNameTeam == "Inter":
                awayNameTeam = "Inter&league=31"
            
            if homeNameTeam == "Reggina":
                homeNameTeam = "Reggi"
            if awayNameTeam == "Reggina":
                awayNameTeam = "Reggi"
            
            if homeNameTeam == "Ascoli":
                homeNameTeam = "Ascoli&league=31"
            if awayNameTeam == "Ascoli":
                awayNameTeam = "Ascoli&league=31"
            
            if homeNameTeam == "Bari":
                homeNameTeam = "Bari&league=31"
            if awayNameTeam == "Bari":
                awayNameTeam = "Bari&league=31"
            
            if homeNameTeam == "Verona":
                homeNameTeam = "Hellas"
            if awayNameTeam == "Verona":
                awayNameTeam = "Hellas"

            #Laliga
            if homeNameTeam == "La Coruna":
                homeNameTeam = "RC Deportivo"
            if awayNameTeam == "La Coruna":
                awayNameTeam = "RC Deportivo"
            
            if homeNameTeam == "Sevilla":
                homeNameTeam = "Sevilla&league=53"
            if awayNameTeam == "Sevilla":
                awayNameTeam = "Sevilla&league=53"
            
            if homeNameTeam == "Espanol":
                homeNameTeam = "RCD Espanyol"
            if awayNameTeam == "Espanol":
                awayNameTeam = "RCD Espanyol"
            
            if homeNameTeam == "Ath Madrid":
                homeNameTeam = "Atlético Madrid"
            if awayNameTeam == "Ath Madrid":
                awayNameTeam = "Atlético Madrid"
            
            if homeNameTeam == "Sociedad":
                homeNameTeam = "Sociedad&league=53"
            if awayNameTeam == "Sociedad":
                awayNameTeam = "Sociedad&league=53"
            
            if homeNameTeam == "Sp Gijon":
                homeNameTeam = "Sporting&league=53"
            if awayNameTeam == "Sp Gijon":
                awayNameTeam = "Sporting&league=53"
            
            if homeNameTeam == "Ath Bilbao":
                homeNameTeam = "Bilbao"
            if awayNameTeam == "Ath Bilbao":
                awayNameTeam = "Bilbao"
            
            if homeNameTeam == "FC Barcelona":
                homeNameTeam = "FC Barcelona&league=53"
            if awayNameTeam == "FC Barcelona":
                awayNameTeam = "FC Barcelona&league=53"
        
            #Ligue1

            if homeNameTeam == "Paris SG":
                homeNameTeam = "Paris"
            if awayNameTeam == "Paris SG":
                awayNameTeam = "Paris"

            if homeNameTeam == "Rennes":
                homeNameTeam = "Renn"
            if awayNameTeam == "Rennes":
                awayNameTeam = "Renn"

            if homeNameTeam == "Lille":
                homeNameTeam = "Osc"
            if awayNameTeam == "Lille":
                awayNameTeam = "Osc"

            if homeNameTeam == "St Etienne":
                homeNameTeam = "Etienne"
            if awayNameTeam == "St Etienne":
                awayNameTeam = "Etienne"

            if homeNameTeam == "Bastia":
                homeNameTeam = "SC Bastia"
            if awayNameTeam == "Bastia":
                awayNameTeam = "SC Bastia"

            if homeNameTeam == "Angers":
                homeNameTeam = "Angers SCO"
            if awayNameTeam == "Angers":
                awayNameTeam = "Angers SCO"

            if homeNameTeam == "Ajaccio GFCO":
                homeNameTeam = "Ajaccio&league=16"
            if awayNameTeam == "Ajaccio GFCO":
                awayNameTeam = "Ajaccio&league=16"

            #Jupiler

            if homeNameTeam == "FC Brussels":
                homeNameTeam = "Brussels"
            if awayNameTeam == "FC Brussels":
                awayNameTeam = "Brussels"

            if homeNameTeam == "St Truiden":
                homeNameTeam = "Truiden"
            if awayNameTeam == "St Truiden":
                awayNameTeam = "Truiden"

            if homeNameTeam == "Bergen":
                homeNameTeam = "Mons"
            if awayNameTeam == "Bergen":
                awayNameTeam = "Mons"

            if homeNameTeam == "Germinal":
                homeNameTeam = "Beerschot"
            if awayNameTeam == "Germinal":
                awayNameTeam = "Beerschot"

            if homeNameTeam == "Mouscron-Peruwelz":
                homeNameTeam = "Mouscron"
            if awayNameTeam == "Mouscron-Peruwelz":
                awayNameTeam = "Mouscron"

            # Eredivisie

            if homeNameTeam == "PSV Eindhoven":
                homeNameTeam = "PSV"
            if awayNameTeam == "PSV Eindhoven":
                awayNameTeam = "PSV"

            if homeNameTeam == "Nijmegen":
                homeNameTeam = "N.E.C."
            if awayNameTeam == "Nijmegen":
                awayNameTeam = "N.E.C."

            if homeNameTeam == "VVV Venlo":
                homeNameTeam = "Venlo"
            if awayNameTeam == "VVV Venlo":
                awayNameTeam = "Venlo"

            if homeNameTeam == "For Sittard":
                homeNameTeam = "Sittard"
            if awayNameTeam == "For Sittard":
                awayNameTeam = "Sittard"

            if homeNameTeam == "AZ Alkmaar":
                homeNameTeam = "AZ&league=10"
            if awayNameTeam == "AZ Alkmaar":
                awayNameTeam = "AZ&league=10"

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
            
            d = {}
            d["Game Date"] = gameDate
            d["Home Team"] = row[2]
            d["Away Team"] = row[3]

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
            
            # FIXME 
            startI = 22
            if int(start_year) == 4:
                startI == 10
            if  int(start_year) == 5 or int(start_year) == 6:
                startI = 23
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

            d["Winner"] = getWinner(row[4],row[5])

            d["Home win Odds not normal"] = (_homeWinOdds/Counter)
            d["Draw Odds not normal"] = (_drawOdds/Counter)
            d["Away win Odds not normal"] = (_awayWinOdds/Counter)

            print(index,row[2],row[3])

            table.append(d)

        df = pandas.DataFrame(table)
        df.to_csv(current_league + "-" + str(sY) + "-" + str(eY) + "-" + "Final-Stats" + ".csv")