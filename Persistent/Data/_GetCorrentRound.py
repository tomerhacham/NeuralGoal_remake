import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
from Persistent.Data.utils import getTeamName, getRoundPerLeague
from Persistent.Data.utils import getNameToFifaIndex
from Persistent.Data.utils import getLeagueNameForWorldFootball

gameDate = ""
def getLastScoredGoals(teamName, leagueName, Cround,teamScore):
    try:
        scoredGaols = teamScore.loc[Cround, teamName + " scored"]
    except KeyError:
        scoredGaols = 1
    return scoredGaols


def getLastRecivedGoals(teamName, leagueName, Cround,teamScore):
    try:
        scoredGaols = teamScore.loc[Cround, teamName + " received"]
    except KeyError:
        scoredGaols = 1
    return scoredGaols
    
def run(leagueName,sY):

    sY = sY
    eY = sY + 1

    MAIN_URL = "https://www.fifaindex.com/teams/fifa"



    table = []
    _le = getLeagueNameForWorldFootball(leagueName,sY)

    dataForRound = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY, eY))
    toSout = dataForRound.content
    urlForNextRound = BeautifulSoup(toSout,"html.parser").find("div",{"class":"navibox2"}).find("div",{"class":"data"}).find_all("ul",{"":""})[1].find_all("li",{"":""})[0].find("a",{"":""})['href']
    _round = int(urlForNextRound.split('/')[3])

    if leagueName == "Laliga" and sY == "16":
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sY,eY))
    else:
        data = requests.get("https://www.worldfootball.net/schedule/" + urlForNextRound)

    teamData = data.content
    games = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[0].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})
    xxxx = games[1].find_all("td",{"":""})[5].text
    if games[1].find_all("td",{"":""})[5].text.find('-:-') == -1 and games[1].find_all("td",{"":""})[5].text.find('resch.') == -1:
        _round = _round + 1
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/{}/".format(sY, eY,_round))

        teamData = data.content
        games = BeautifulSoup(teamData, "html.parser").find_all("div", {"class": "box"})[0].find("table", {
            "class": "standard_tabelle"}).find_all("tr", {"": ""})

    standing = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[1].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})

    if _round == 1 :
        path = leagueName + " stats//Stats For {}-{}//".format(str(sY-1),str(eY-1)) + "standing-" + str(sY-1) + "-" + str(eY-1) + "-AVG-Goals.csv"
    else:
        path = leagueName + " stats//Stats For {}-{}//".format(str(sY), str(eY)) + "standing-" + str(sY) + "-" + str(
            eY) + "-AVG-Goals.csv"
    teamScore = pandas.read_csv(path)

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

            isGameGoing = teams.find_all("td",{"":""})[5].text
            resss = isGameGoing.find('resch.')
            if isGameGoing.find('resch.') >= 0:
                continue
            homeTeam = data[0].text
            AwayTeam = data[1].text
            homeTeam = getTeamName(homeTeam)
            AwayTeam = getTeamName(AwayTeam)
            CgameDate = teams.find("td",{"":""}).text
            if CgameDate is not "":
                d["date"] = CgameDate
                gameDate = CgameDate
            else:
                d["date"] = gameDate
            d["league"] = leagueName
            d["round"] = _round
            d["home_team_name"] = homeTeam
            d["away_team_name"] = AwayTeam

            d["home_team_rank"] = int(standing_teams.index(homeTeam)) + 1
            d["away_team_rank"] = int(standing_teams.index(AwayTeam)) + 1

            _homeTeam, _AwayTeam = getNameToFifaIndex(homeTeam, AwayTeam)
            urlHomeTeam = MAIN_URL + str(eY) + "/?name=" + _homeTeam
            urlAwayTeam = MAIN_URL + str(eY) + "/?name=" + _AwayTeam

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

            d["home_att"] = homeTeamData.find("td",{"data-title":"ATT"}).text
            d["away_att"] = awayTeamData.find("td",{"data-title":"ATT"}).text
            d["home_def"] = homeTeamData.find("td",{"data-title":"DEF"}).text
            d["away_def"] = awayTeamData.find("td",{"data-title":"DEF"}).text
            d["home_mid"] = homeTeamData.find("td",{"data-title":"MID"}).text
            d["away_mid"] = awayTeamData.find("td",{"data-title":"MID"}).text



            if _round == 1:
                shape = teamScore.shape[0]
                d["home_team_scored"] = getLastScoredGoals(homeTeam, str(leagueName), int(shape) - 1, teamScore)
                d["home_team_received"] = getLastRecivedGoals(homeTeam, str(leagueName), int(shape) - 1, teamScore)
                d["away_team_scored"] = getLastScoredGoals(AwayTeam, str(leagueName), int(shape) - 1, teamScore)
                d["away_team_received"] = getLastRecivedGoals(AwayTeam, str(leagueName), int(shape) - 1, teamScore)
            else:
                d["home_team_scored"] = getLastScoredGoals(homeTeam,str(leagueName),int(_round)-2,teamScore)
                d["home_team_received"] = getLastRecivedGoals(homeTeam,str(leagueName),int(_round)-2,teamScore)
                d["away_team_scored"] = getLastScoredGoals(AwayTeam,str(leagueName),int(_round)-2,teamScore)
                d["away_team_received"] = getLastRecivedGoals(AwayTeam,str(leagueName),int(_round)-2,teamScore)

            # tomer
            d["home_odds_n"] = ""
            d["draw_odds_n"] = ""
            d["away_odds_n"] = ""

            # idan
            d["home_odds_nn"] = ""
            d["draw_odds_nn"] = ""
            d["away_odds_nn"] = ""


            




            table.append(d)
            gameCounter = gameCounter + 1
        except:
            continue


    df = pandas.DataFrame(table)
    df.to_csv("Prediction//" + leagueName + "Round({})ToPredict.csv".format(_round))
