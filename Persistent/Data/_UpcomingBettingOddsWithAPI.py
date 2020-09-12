import requests
import json
from flask import jsonify, make_response
import pandas
import requests
import glob

from Persistent.Data.utils import gamesInRoundByLeagueName, mapTeamsOdds


def run(leagueName):

    def getNormalOdds(Home, Draw, Away):
        _rH = 1 / float(Home)
        _rD = 1 / float(Draw)
        _rA = 1 / float(Away)
        _r = _rH + _rD + _rA
        return _r

    # Premier
    if leagueName == "PremierLeague":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_epl')
        )
    # Italy
    if leagueName == "Serie":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_italy_serie_a')
        )
    if leagueName == "Bundesliga":
        # Bundesliga
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_germany_bundesliga')
        )
    # Laliga
    if leagueName == "Laliga":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_spain_la_liga')
        )
    # Belgium
    if leagueName == "Jupiler":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_belgium_first_div')
        )
    # Ligue 1
    if leagueName == "Ligue1":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_france_ligue_one')
        )
    # Eredivisie
    if leagueName == "Eredivisie":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_netherlands_eredivisie')
        )
    # Portugal
    if leagueName == "Portugal":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_portugal_primeira_liga')
        )
    # Scottish
    if leagueName == "Scotish":
        params = (
            ('apiKey', '994c68fcabcb997afa737025a839e64b'),
            ('mkt', 'h2h'),
            ('region', 'uk'),
            ('sport', 'soccer_spl')
        )

    response = requests.get('https://api.the-odds-api.com/v3/odds', params=params)
    table = []
    res = response.json()
    numberOfGames = len(res['data'])
    for game in range(numberOfGames):
        t = {}
        try:
            homeTeam = res['data'][game]['teams'][0]
            awayTeam = res['data'][game]['teams'][1]

            home_team = res['data'][game]['home_team']
            if homeTeam != home_team:
                awayTeam = homeTeam
                homeTeam = home_team

            sitesCount = int(res['data'][game]['sites_count'])

            homeOdds = 0
            awayOdds = 0
            drawOdds = 0

            for site in range(sitesCount):
                homeOdds = homeOdds + res['data'][game]['sites'][site]['odds']['h2h'][0]
                awayOdds = awayOdds + res['data'][game]['sites'][site]['odds']['h2h'][1]
                drawOdds = drawOdds + res['data'][game]['sites'][site]['odds']['h2h'][2]

            homeOdds = homeOdds / sitesCount
            awayOdds = awayOdds / sitesCount
            drawOdds = drawOdds / sitesCount

        except:
            continue

        _R = getNormalOdds(homeOdds, awayOdds, drawOdds)
        HwinOdds = (1 / (homeOdds)) / _R
        DrawOds = (1 / (drawOdds)) / _R
        AwinOdds = (1 / (awayOdds)) / _R

        t["Home Team"] = mapTeamsOdds(homeTeam)
        t["Away Team"] = mapTeamsOdds(awayTeam)
        t["Home Team Win Odds"] = HwinOdds
        t["Draw Odds"] = DrawOds
        t["Away Team Win Odds"] = AwinOdds
        table.append(t)

    df = pandas.DataFrame(table)

    csvFilePath = ""
    for name in glob.glob(
            'C:\\Users\\Andrey\\Documents\\NeuralGoal_remake\\Persistent\\Data\\Prediction\\{}R*.csv'.format(
                leagueName)):
        csvFilePath = name

    currentLeagueGames = pandas.read_csv(csvFilePath, parse_dates=True,index_col=0)

    for currentLeagueGamesindex, currentLeagueGamesrow in currentLeagueGames.iterrows():
        for toConcatindex, toConcatrow in df.iterrows():
            if currentLeagueGames['home_team_name'][currentLeagueGamesindex] == df['Home Team'][toConcatindex] and currentLeagueGames['away_team_name'][currentLeagueGamesindex] == df['Away Team'][toConcatindex]:
                currentLeagueGames['home_odds_n'][currentLeagueGamesindex] = df["Home Team Win Odds"][
                    toConcatindex]
                currentLeagueGames['draw_odds_n'][currentLeagueGamesindex] = df["Draw Odds"][toConcatindex]
                currentLeagueGames['away_odds_n'][currentLeagueGamesindex] = df["Away Team Win Odds"][
                    toConcatindex]

    currentLeagueGames.to_csv(csvFilePath)
