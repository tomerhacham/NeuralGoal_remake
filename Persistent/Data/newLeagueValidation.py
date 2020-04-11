import urllib.request
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import shutil

leagueName = ""

baseURL = "https://www.football-data.co.uk/mmz4281/"


def run(leagueName, startYear, endYear, division):
    currentDirectory = os.getcwd()
    if startYear < 10:
        startYear = "0" + str(startYear)
    if endYear < 10:
        endYear = "0" + str(endYear)
    url = baseURL + "{}{}/{}.csv".format(startYear, endYear, division)
    startYear = str(startYear)
    endYear = str(endYear)

    urllib.request.urlretrieve(url, currentDirectory + "\\" + leagueName + "-" + startYear + "-" + endYear + ".csv")

    df = pd.read_csv(leagueName + "-" + startYear + "-" + endYear + ".csv")
    if startYear == "19":
        df.drop('Time', axis=1, inplace=True)
    df.to_csv(leagueName + "-" + startYear + "-" + endYear + ".csv", index=False)


def validate(leagueName, startYear, endYear):
    listOfNotFound = []
    current_league = leagueName
    MAIN_URL = "https://www.fifaindex.com/teams/fifa"
    start_year = startYear
    end_year = endYear
    sY = start_year
    eY = end_year

    if (start_year < 10):
        start_year = "0" + str(start_year)
    if (end_year < 10):
        end_year = "0" + str(end_year)

    table = []
    try:
        team_stat = pd.read_csv(current_league + "-" + str(start_year) + "-" + str(end_year) + ".csv", parse_dates=True)
    except:
        print(str(start_year) + " " + str(end_year) + " Curropt")

    counter = 0
    for index, row in team_stat.iterrows():
        if counter > 8:
            break

        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
        headers = {'User-Agent': user_agent,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

        homeNameTeam = str(row[2])
        awayNameTeam = str(row[3])

        if int(end_year) < 10:
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
            homeTeamData = BeautifulSoup(dataHomeTeamContenet, "html.parser")
        except:
            continue
        try:
            awayTeamData = BeautifulSoup(dataAwayTeamContenet, "html.parser")
        except:
            continue

        d = {}

        try:
            d["Home ATT"] = homeTeamData.find("td", {"data-title": "ATT"}).text
        except:
            listOfNotFound.append(homeNameTeam)
            continue
        try:
            d["Away ATT"] = awayTeamData.find("td", {"data-title": "ATT"}).text
        except:
            listOfNotFound.append(awayNameTeam)
            continue

        counter = counter + 1
    return listOfNotFound


def getAllNames(leagueName, startYear, endYear):
    listOfNames = []

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

        _le = leagueName

        for x in range(1, 2):

            try:
                data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY, eY) + str(x))
                teamData = data.content
                d = {}
                teamData = BeautifulSoup(teamData, "html.parser").find_all("div", {"class": "box"})[1].find("table", {"class": "standard_tabelle"}).find_all("tr", {"": ""})
            except:
                print(str(startYear))
                continue
            for team in teamData:
                if (counter == 0):
                    try:
                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        print(teams_name)
                        listOfNames.append(teams_name)
                    except:
                        continue
                else:
                    try:
                        data = team.find("a", {"": ""})
                        teams_name = data.text
                        print(teams_name)
                        listOfNames.append(teams_name)
                    except:
                        continue
            counter = counter + 1
            t_t.append(d)
            table.append(d)

    return listOfNames
