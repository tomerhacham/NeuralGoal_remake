import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
import time
from Persistent.Data.utils import getTeamName
from Persistent.Data.utils import getLeagueNameForWorldFootball

def run(leagueName, round, startYear, endYear):
    startY = [startYear]
    endY = [endYear]

    for year in range(len(startY)):

        table = []
        t_t = []

        if startY[year] < 10:
            sY = "0" + str(startY[year])
        else:
            sY = str(startY[year])
        if endY[year] < 10:
            eY = "0" + str(endY[year])
        else:
            eY = str(endY[year])

        counter = 0
        _until = 0

        _round = round

        _le = getLeagueNameForWorldFootball(leagueName,startYear)

        for x in range(1, _round + 1):

            try:
                if leagueName == "Laliga" and sY == "16":
                    data = requests.get(
                        "https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sY, eY) + str(
                            x))
                else:
                    data = requests.get(
                        "https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY, eY) + str(x))
                teamData = data.content
                d = {}
                teamData = BeautifulSoup(teamData, "html.parser").find_all("div", {"class": "box"})[1].find("table", {
                    "class": "standard_tabelle"}).find_all("tr", {"": ""})
            except:
                continue
            _lastRoundScored = 0
            _lastRoundRecived = 0
            _round = 1
            print(x)
            for team in teamData:
                if (counter == 0):
                    try:
                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        team_name = getTeamName(teams_name)

                        try:
                            a = team.find_all("td", {"": ""})[7].text
                            goalsScored = a.split(":")[0]
                            goalsRecived = a.split(":")[1]
                            d[team_name + " scored"] = goalsScored
                            d[team_name + " received"] = goalsRecived
                        except:
                            goalsScored = -1
                            goalsRecived = -1
                            d[team_name + " scored"] = goalsScored
                            d[team_name + " received"] = goalsRecived
                    except:
                        continue
                else:
                    try:
                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        team_name = getTeamName(teams_name)

                        a = team.find_all("td", {"": ""})[7].text
                        goalsScored = a.split(":")[0]
                        goalsRecived = a.split(":")[1]
                        d[team_name + " scored"] = int(goalsScored)
                        d[team_name + " received"] = int(goalsRecived)
                    except:
                        continue
            counter = counter + 1
            t_t.append(d)
            table.append(d)

        if startY[year] < 10:
            sY = str(startY[year])
        if endY[year] < 10:
            eY = str(endY[year])

        df = pandas.DataFrame(table)
        df.to_csv("standing-" + sY + "-" + eY + ".csv")
