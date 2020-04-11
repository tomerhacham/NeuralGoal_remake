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

        table = []

        rows_1 = []
        rows_2 = []

        sY = startY[x]
        eY = endY[x]

        team_standing_1 = pandas.read_csv("standing-" + str(sY) + "-" + str(eY) + ".csv")
        team_standing_2 = pandas.read_csv("standing-" + str(sY) + "-" + str(eY) + ".csv")

        for index, row in team_standing_1.iterrows():
            rows_1.append(row)

        for index, row in team_standing_2.iterrows():
            rows_2.append(row)

        for index, row in team_standing_1.iterrows():
            d = {}
            _range = 0
            if leagueName == "Bundesliga" or leagueName == "Eredivisie":
                _range = 41-4
            elif leagueName == "Jupiler":
                if startYear <= 8:
                    _range = 41-4
                else:
                    _range = 41-8
            else:
                _range =41
            for counter in range(1,_range):
                name = list(team_standing_1.columns)[counter]
                if(index == 0):
                    d[name] = rows_1[0][counter]
                else:

                    x = rows_1[index][counter]
                    y = rows_2[index-1][counter]
                    d[name] = int(x) - int(y)
            table.append(d)
        df = pandas.DataFrame(table)
        df.to_csv("standing-" + str(sY) + "-" + str(eY) + "-AVG.csv")