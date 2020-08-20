# import requests
# import json
# from flask import jsonify, make_response
# import pandas
#
# import requests
#
# headers = {
# 	'apikey': '2aff7050-183e-11ea-8eec-bb267472c7df',
# }
#
# params = (
# 	('sport', 'soccer'),
# 	('country', 'scotland'),
# 	('league', 'soccer-england-premier-league')
# )
#
# response = requests.get('https://app.oddsapi.io/api/v1/odds', headers=headers, params=params)
#
# print(response.json())
#
# def run(leagueName,round):
#
#     def getNormalOdds(Home,Draw,Away):
#         _rH = 1/float(Home)
#         _rD = 1/float(Draw)
#         _rA = 1/float(Away)
#         _r = _rH + _rD + _rA
#         return _r
#
#     headers = {
#         'apikey': '2aff7050-183e-11ea-8eec-bb267472c7df',
#     }
#
#     # Premier
#     if leagueName == "PremierLeague":
#         params = (
#             ('sport', 'soccer'),
#             ('country', 'england'),
#             ('league', 'soccer-england-premier-league'),
#             ('mkt','h2h'),
#             ('region','uk')
#         )
#     if leagueName == "Serie":
#         # Italy
#         params = (
#             ('sport', 'soccer'),
#             ('country', 'italy'),
#             ('league', 'soccer-italy-serie-a'),
#             ('mkt','h2h'),
#             ('region','uk')
#         )
#     if leagueName == "Bundesliga":
#     # Bundesliga
#         params = (
#             ('sport', 'soccer'),
#             ('country', 'germany'),
#             ('league', 'soccer-germany-bundesliga'),
#             ('mkt','h2h'),
#             ('region','uk')
#         )
#     if leagueName == "Laliga":
#         # Laliga
#         params = (
#             ('sport', 'soccer'),
#             ('country', 'spain'),
#             ('league', 'soccer-spain-laliga'),
#             ('mkt','h2h'),
#             ('region','uk')
#         )
#
#     response = requests.get('https://app.oddsapi.io/api/v1/odds', headers=headers, params=params)
#     table = []
#     counter = 0
#     for x in response.json():
#         t = {}
#         try:
#             homtTeam = x['event']['home']
#             awayTeam = x['event']['away']
#
#             HomeOdds = x['sites']['1x2']['bet365']['odds']['1']
#             DrawOdds = x['sites']['1x2']['bet365']['odds']['X']
#             AwayOdds = x['sites']['1x2']['bet365']['odds']['2']
#
#             HomeOdds = x['sites']['1x2']['bwin']['odds']['1']
#             DrawOdds = x['sites']['1x2']['bwin']['odds']['X']
#             AwayOdds = x['sites']['1x2']['bwin']['odds']['2']
#
#             HomeOdds = x['sites']['1x2']['unibet']['odds']['1']
#             DrawOdds = x['sites']['1x2']['unibet']['odds']['X']
#             AwayOdds = x['sites']['1x2']['unibet']['odds']['2']
#
#             HomeOdds = x['sites']['1x2']['10bet']['odds']['1']
#             DrawOdds = x['sites']['1x2']['10bet']['odds']['X']
#             AwayOdds = x['sites']['1x2']['10bet']['odds']['2']
#
#             HomeOdds = x['sites']['1x2']['betfair']['odds']['1']
#             DrawOdds = x['sites']['1x2']['betfair']['odds']['X']
#             AwayOdds = x['sites']['1x2']['betfair']['odds']['2']
#
#             HomeOdds = x['sites']['1x2']['betway']['odds']['1']
#             DrawOdds = x['sites']['1x2']['betway']['odds']['X']
#             AwayOdds = x['sites']['1x2']['betway']['odds']['2']
#             counter = counter + 1
#         except:
#             continue
#
#
#         _R = getNormalOdds(HomeOdds/counter,DrawOdds/counter,AwayOdds/counter)
#         HwinOdds = (1/(HomeOdds/counter))/_R
#         DrawOds = (1/(DrawOdds/counter))/_R
#         AwinOdds = (1/(AwayOdds/counter))/_R
#
#         t["Home Team"] = homtTeam
#         t["Away Team"] = awayTeam
#         t["Home Team Win Odds"] = HwinOdds
#         t["Draw Odds"] = DrawOds
#         t["Away Team Win Odds"] = AwinOdds
#         table.append(t)
#
#     df = pandas.DataFrame(table)
#     df.to_csv(leagueName + "PredictBettingOdds.csv")

