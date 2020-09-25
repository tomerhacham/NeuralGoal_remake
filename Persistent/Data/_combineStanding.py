import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests
import time
from Persistent.Data.utils import getTeamName
from Persistent.Data.utils import getLeagueNameForWorldFootball

def run(leagueName,round,startYear,endYear):

    startY = [startYear]
    endY = [endYear]

    for year in range(len(startY)):

        table = []
        t_t = []

        if startY[year] < 10:
            sY = "0" + str(startY[year])
            sYY = "0" + str(int(startY[year])-1)
        else:
            sY = str(startY[year])
            sYY = str(int(startY[year])-1)
        if endY[year] < 10:
            eY = "0" + str(endY[year])
            eYY = "0" + str(int(endY[year])-1)
        else:
            eY = str(endY[year])
            eYY = str(int(endY[year])-1)

        
        _until = 0

        _round = round

        _le = getLeagueNameForWorldFootball(leagueName,startYear)

        for x in range(1,_round+1):





            counter = 0 
            if leagueName == "Laliga" and sY == "16":
                data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sY,eY) + str(x))
            else:
                url = "https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY,eY) + str(x)
                data = requests.get(url)
            teamData = data.content
            teamData = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[1].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})


            d = {}
            print(x)

            for team in teamData:
                try:


                    if sY == "05" and x <= 3:
                        d[counter] = -1
                        counter = counter + 1
                    elif x <= 3:

                        if leagueName == "Laliga" and sYY == "16":
                            data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sYY,eYY))
                        else:
                            url = "https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sYY,eYY)
                            data = requests.get(url)

                        teamData = data.content
                        teamData = BeautifulSoup(teamData, "html.parser").find_all("div", {"class": "box"})[1].find("table", {"class": "standard_tabelle"}).find_all("tr", {"": ""})

                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        team_name = getTeamName(teams_name)
                        d[counter] = team_name
                        counter = counter + 1

                    else:
                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        team_name = getTeamName(teams_name)

                        d[counter] = team_name
                        counter = counter + 1
                except:
                    continue

            t_t.append(d)
            table.append(d)

        if startY[year] < 10:
            sY = str(startY[year])
        if endY[year] < 10:
            eY = str(endY[year])
        df = pandas.DataFrame(table)
        df.to_csv("standing-" + sY + "-"+ eY + "-Teams.csv")