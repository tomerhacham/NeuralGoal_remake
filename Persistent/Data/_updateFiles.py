import urllib.request
import os
import pandas as pd
import shutil
from pathlib import Path

baseURL = "https://www.football-data.co.uk/mmz4281/"


# leagueName = "Bundesliga"

def run(leagueName, startYear, endYear):
    currentDirectory = os.getcwd()

    url = ""

    if leagueName == "Serie":
        url = baseURL + "{}{}/I1.csv".format(startYear, endYear)
    if leagueName == "Bundesliga":
        url = baseURL + "{}{}/D1.csv".format(startYear, endYear)
    if leagueName == "Laliga":
        url = baseURL + "{}{}/SP1.csv".format(startYear, endYear)
    if leagueName == "PremierLeague":
        url = baseURL + "{}{}/E0.csv".format(startYear, endYear)
    if leagueName == "Ligue1":
        url = baseURL + "{}{}/F1.csv".format(startYear, endYear)
    if leagueName == "Jupiler":
        url = baseURL + "{}{}/B1.csv".format(startYear, endYear)
    if leagueName == "Eredivisie":
        url = baseURL + "{}{}/N1.csv".format(startYear,endYear)

    startYear = str(startYear)
    endYear = str(endYear)

    urllib.request.urlretrieve(url, currentDirectory + "\\" + leagueName + "-" + startYear + "-" + endYear + ".csv")

    df = pd.read_csv(leagueName + "-" + startYear + "-" + endYear + ".csv")
    if startYear == "19":
        df.drop('Time', axis=1, inplace=True)
    df.to_csv(leagueName + "-" + startYear + "-" + endYear + ".csv", index=False)


def cleanAllFile(leagueName, startYear, endYear):
    startYear = str(startYear)
    endYear = str(endYear)
    sPath = os.getcwd()

    files = [leagueName + "-" + startYear + "-" + endYear + "-Goals-AVG3.csv",
             "standing" + "-" + startYear + "-" + endYear + "-AVG.csv",
             "standing" + "-" + startYear + "-" + endYear + ".csv",
             "standing" + "-" + startYear + "-" + endYear + "-Teams.csv",
             "standing" + "-" + startYear + "-" + endYear + "-AVG-Goals.csv",
             leagueName + "-" + startYear + "-" + endYear + "-Final-Stats.csv"]
    for file in files:
        try:
            sourcePath = sPath + "\\" + file
            destinationPath = sPath + "\\" + leagueName + " stats\\Stats For {}-{}\\".format(startYear, endYear) + file
            shutil.move(sourcePath, destinationPath)
        except:
            continue

    # move the final to final destention
    file = leagueName + "-" + startYear + "-" + endYear + "-Final.csv"

    sourcePath = sPath + "\\" + file
    destinationPath = sPath + "\\" + leagueName + " stats\\Final\\" + file

    shutil.move(sourcePath, destinationPath)


def combineToFinal(leagueName, startYear, endYear):
    startYear = str(startYear)
    endYear = str(endYear)
    sPath = os.getcwd()
    sourceFile = leagueName + "-" + startYear + "-" + endYear + "-Goals-AVG3.csv"
    destinationPathFile = leagueName + "-" + startYear + "-" + endYear + "-Final-Stats.csv"

    dfSourceFile = pd.read_csv(sourceFile, usecols=['Home Team Rank', 'Away Team Rank', 'Home Team Scored Goals',
                                                    'Home Team Received Goals', 'Away Team Scored Goals',
                                                    'Away Team received Goals'])
    dfDestiantionFile = pd.read_csv(destinationPathFile,
                                    usecols=['Game Date', 'Home Team', 'Away Team', 'Home ATT', 'Away ATT', 'Home DEF',
                                             'Away DEF', 'Home MID', 'Away MID', 'Home Win Odds', 'Draw Odds',
                                             'Away Win Odds',
                                             'Winner', 'Home win Odds not normal', 'Draw Odds not normal',
                                             'Away win Odds not normal'])

    finalTable = pd.concat([dfDestiantionFile, dfSourceFile], axis=1, sort=False)

    finalTable.to_csv(sPath + "\\" + leagueName + "-" + startYear + "-" + endYear + "-Final.csv")
