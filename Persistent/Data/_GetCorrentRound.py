import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
from Persistent.Data.utils import getTeamName
from Persistent.Data.utils import getNameToFifaIndex
from Persistent.Data.utils import getLeagueNameForWorldFootball

    
def run(leagueName,round):

    sY = 19
    eY = 20 
    path = "standing-" + str(sY) + "-" + str(eY) + "-AVG-Goals.csv"

    teamScore = pandas.read_csv(path)
    MAIN_URL = "https://www.fifaindex.com/teams/fifa"

    def getLastScoredGoals(teamName,leagueName,Cround):
        scoredGaols = teamScore.loc[Cround,teamName + " scored"]
        return scoredGaols

    def getLastRecivedGoals(teamName,leagueName,Cround):
        scoredGaols = teamScore.loc[Cround,teamName + " received"]
        return scoredGaols
    
    table = []

    _round = round

    _le = getLeagueNameForWorldFootball(leagueName,sY)

    if leagueName == "Laliga" and sY == "16":
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sY,eY))
    else:
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY,eY))
    teamData = data.content
    games = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[0].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})
    standing = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[1].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})

    standing_teams = []

    for team in standing:
        try:
            data = team.find("a",{"":""})
            teams_name = data.text
            team_name = getTeamName(teams_name)
            standing_teams.append(team_name)
        except:
            continue
    
    gameCounter = 0
    for teams in games:
        try:
            d = {}
            data = teams.find_all("td",{"":""})
            data = teams.find_all("a",{"":""})
            homeTeam = data[0].text
            AwayTeam = data[1].text
            homeTeam = getTeamName(homeTeam)
            AwayTeam = getTeamName(AwayTeam)

            d["Home Team"] = homeTeam
            d["Away Team"] = AwayTeam
            d["Home Team Rank"] = int(standing_teams.index(homeTeam)) + 1
            d["Away Team Rank"] = int(standing_teams.index(AwayTeam)) + 1
            d["Home Team Scored Goals"] = getLastScoredGoals(homeTeam,str(leagueName),int(_round)-2)
            d["Home Team Received Goals"] = getLastRecivedGoals(homeTeam,str(leagueName),int(_round)-2)
            d["Away Team Scored Goals"] = getLastScoredGoals(AwayTeam,str(leagueName),int(_round)-2)
            d["Away Team Received Goals"] = getLastRecivedGoals(AwayTeam,str(leagueName),int(_round)-2)

            homeTeam,AwayTeam = getNameToFifaIndex(homeTeam,AwayTeam)
            urlHomeTeam = MAIN_URL + str(sY) + "/?name=" + homeTeam
            urlAwayTeam = MAIN_URL + str(sY) + "/?name=" + homeTeam

            dataHomeTeam = requests.get(urlHomeTeam)
            dataHomeTeamContenet = dataHomeTeam.content
            
            dataAwayTeam = requests.get(urlAwayTeam)
            dataAwayTeamContenet = dataAwayTeam.content

            try:    
                homeTeamData= BeautifulSoup(dataHomeTeamContenet,"html.parser")
                awayTeamData= BeautifulSoup(dataAwayTeamContenet,"html.parser")
            except:
                print("EXCEPTION " + homeTeam + " " + AwayTeam)
                continue

            d["Home ATT"] = homeTeamData.find("td",{"data-title":"ATT"}).text
            d["Away ATT"] = awayTeamData.find("td",{"data-title":"ATT"}).text
            d["Home DEF"] = homeTeamData.find("td",{"data-title":"DEF"}).text
            d["Away DEF"] = awayTeamData.find("td",{"data-title":"DEF"}).text
            d["Home MID"] = homeTeamData.find("td",{"data-title":"MID"}).text
            d["Away MID"] = awayTeamData.find("td",{"data-title":"MID"}).text

            # tomer
            d["Home win Odds Bet365"] = ""
            d["Draw Odds not Bet365"] = ""
            d["Away win Odds Bet365"] = ""
            
            # idan
            d["Home win Odds Winner"] = "" #_homeWinOdds
            d["Draw Odds not Winner"] = "" #_drawOdds
            d["Away win Odds Winner"] = "" #_awayWinOdds

            d["Home win Odds Winner +1"] = "" #_homeWinOdds
            d["Draw Odds not Winner +1"] = "" #_drawOdds
            d["Away win Odds Winner +1"] = "" #_awayWinOdds

            table.append(d)
            gameCounter = gameCounter + 1
        except:
            continue


    df = pandas.DataFrame(table)
    df.to_csv(leagueName + "NextRoundToPredict.csv")
