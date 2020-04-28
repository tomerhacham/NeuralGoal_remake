from MakePrediction import makePredictions
from Persistent import dto
from Persistent.repository import Repository
import platform
import pandas
import os

currentDirectory = os.getcwd()

slashDirection = "\\"
if platform.system() == "Darwin":
    slashDirection = "//"

rounds_to_predict = 23


def resultForGame(_date, home_team_name, away_team_name, league):
    filePath = currentDirectory + '{}Persistent{}Data{}{} stats{}Final{}{}-19-20-Final.csv'.format(slashDirection,
                                                                                                   slashDirection,
                                                                                                   slashDirection,
                                                                                                   league,
                                                                                                   slashDirection,
                                                                                                   slashDirection,
                                                                                                   league)
    tableToRead = pandas.read_csv(filePath, parse_dates=True)
    date = _date.replace('-', '/')
    date = date.split('/')
    date = str(date[2]) + "/" + str(date[1]) + "/" + str(date[0])

    for index, row in tableToRead.iterrows():
        if row[1] == date:
            if row[2] == home_team_name:
                if row[3] == away_team_name:
                    return row[13]
    return -1


# for _round in range(rounds_to_predict):
#     _round = _round + 1
#     gamesToMainTable = makePredictions(_round)
#     for ind in gamesToMainTable.index:
#
#         leagueName = gamesToMainTable['league'][ind]
#         _date = gamesToMainTable['date'][ind]
#         gameCounter = int(gamesToMainTable['round'][ind])
#
#         _home_team_name = gamesToMainTable['home_team_name'][ind]
#         _away_team_name = gamesToMainTable['away_team_name'][ind]
#
#         _home_team_rank = int(gamesToMainTable['home_team_rank'][ind])
#         _away_team_rank = int(gamesToMainTable['away_team_rank'][ind])
#
#         _home_team_scored = gamesToMainTable['home_team_scored'][ind]
#         _away_team_scored = gamesToMainTable['away_team_scored'][ind]
#
#         _home_team_received = gamesToMainTable['home_team_received'][ind]
#         _away_team_received = gamesToMainTable['away_team_received'][ind]
#
#         _home_att = int(gamesToMainTable['home_att'][ind])
#         _away_att = int(gamesToMainTable['away_att'][ind])
#
#         _home_def = int(gamesToMainTable['home_def'][ind])
#         _away_def = int(gamesToMainTable['away_def'][ind])
#
#         _home_mid = int(gamesToMainTable['home_mid'][ind])
#         _away_mid = int(gamesToMainTable['away_mid'][ind])
#
#         _home_odds_n = gamesToMainTable['home_odds_n'][ind]
#         _draw_odds_n = gamesToMainTable['draw_odds_n'][ind]
#         _away_odds_n = gamesToMainTable['away_odds_n'][ind]
#
#         _home_odds_nn = gamesToMainTable['home_odds_nn'][ind]
#         _draw_odds_nn = gamesToMainTable['draw_odds_nn'][ind]
#         _away_odds_nn = gamesToMainTable['away_odds_nn'][ind]
#
#         _result = resultForGame(_date, _home_team_name, _away_team_name, leagueName)
#
#         if _result == -1:
#             print("Cant find")
#
#         gameToAdd = dto.match(leagueName, _date, gameCounter, _home_team_name, _away_team_name,
#                               _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
#                               _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
#                               _away_def,
#                               _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
#                               _home_odds_nn, _draw_odds_nn, _away_odds_nn)
#         repo = Repository()
#         repo.upcoming_games.delete(_date, _home_team_name, _away_team_name)
#         repo.main_table.insert(gameToAdd)
#
#
# for prediction in range(rounds_to_predict):
#     prediction = prediction + 1
#     path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction)
#     tableToRead = pandas.read_csv(path, parse_dates=True)
#     tableToRead['Result'] = 0
#     for index, row in tableToRead.iterrows():
#         gameResult = resultForGame(row[1], row[2], row[3], row[0])
#         tableToRead['Result'][index] = str(gameResult)
#     tableToRead.to_csv(str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction))


def maxPrediction(list):
    return max(list)


def indexOfMaxPrediction(list):
    x = list.index(max(list))
    if x == 0:
        return '1'
    if x == 1:
        return '2'
    return 'X'


def nnOds(list):
    x = list.index(max(list))
    if x == 0:
        return 5
    if x == 1:
        return 7
    return 6


def AW(Excpected, Acutal):
    if (Excpected == Acutal):
        return 'True'
    return 'False'


def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

# for prediction in range(rounds_to_predict):
#     prediction = prediction + 1
#     path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction)
#     tableToRead = pandas.read_csv(path, parse_dates=True)
#
#     tableToRead['----------------------------'] = ''
#     tableToRead['Max Probability'] = ''
#     tableToRead['Module Prediction'] = ''
#     tableToRead['Winner Prediction'] = ''
#     tableToRead['Win'] = ''
#     tableToRead['Expectancy of variance'] = ''
#
#     listOfGames = []
#     TrueCounter = 0
#     totalGames = 0
#     for index, row in tableToRead.iterrows():
#         # By module - 0 < x < 1
#         maxP = maxPrediction([float(row[8]), float(row[9]), float(row[10])])
#         tableToRead['Max Probability'][index] = maxP
#         pair = (index, maxP)
#         listOfGames.append(pair)
#         # By Max Prob - 1 X 2
#         mPred = indexOfMaxPrediction([float(row[8]), float(row[9]), float(row[10])])
#         tableToRead['Module Prediction'][index] = mPred
#         # By Module Prob - x > 0
#         WP = row[int(nnOds([float(row[8]), float(row[9]), float(row[10])]))]
#         tableToRead['Winner Prediction'][index] = WP
#         # By module - TRUE FALSE
#         aw = AW(row[11], indexOfMaxPrediction([float(row[8]), float(row[9]), float(row[10])]))
#         if aw == 'True':
#             TrueCounter = TrueCounter + 1
#         tableToRead['Win'][index] = aw
#         # ΩΘ-1
#         FinalP = float(WP * maxP) - 1
#         tableToRead['Expectancy of variance'][index] = FinalP
#
#         totalGames = index + 1
#
#     sortedTuples = Sort_Tuple(listOfGames)
#     sortedTuples.reverse()
#     x = 1
#
#     tableToRead['--------------------------'] = ''
#     index = 0
#     total_stake = 0
#     total_prize = 0
#     price_rate = 0
#     tableToRead['Serial Number'] = ''
#     tableToRead['Probability'] = ''
#     tableToRead['W Prediction'] = ''
#     tableToRead['Odds'] = ''
#     tableToRead['Bet'] = ''
#     tableToRead['Prize'] = ''
#     for pair in sortedTuples:
#         tableToRead['Serial Number'][index] = pair[0]
#         tableToRead['Probability'][index] = pair[1]
#         tableToRead['W Prediction'][index] = tableToRead['Module Prediction'][pair[0]]
#         tableToRead['Odds'][index] = tableToRead['Winner Prediction'][pair[0]]
#         tableToRead['Bet'][index] = 10
#         total_stake = total_stake + tableToRead['Bet'][index]
#         if(tableToRead['Win'][pair[0]] == 'True'):
#             tableToRead['Prize'][index] = tableToRead['Bet'][index] * tableToRead['Odds'][index]
#             total_prize = total_prize + tableToRead['Prize'][index]
#         else:
#             tableToRead['Prize'][index] = 0
#
#         index = index+1
#
#     tableToRead['-------------------------'] = ''
#
#     tableToRead.loc[5, '__'] = "Winning rate"
#     tableToRead.loc[5, '_'] = float(TrueCounter/totalGames)
#
#     tableToRead.loc[6, '__'] = "Total bet"
#     tableToRead.loc[6, '_'] = int(total_stake)
#
#     tableToRead.loc[7, '__'] = "Total prize"
#     tableToRead.loc[7, '_'] = int(total_prize)
#
#     tableToRead.loc[8, '__'] = "Prize rate"
#     tableToRead.loc[8, '_'] = float(total_prize / total_stake)
#
#
#
#
#
#     tableToRead.to_csv(
#         str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction))

TSTACK_06 = 0
TEARINING_06 = 0

TSTACK_065 = 0
TEARINING_065 = 0

TSTACK_07 = 0
TEARINING_07 = 0

TSTACK_075 = 0
TEARINING_075 = 0

TSTACK_08 = 0
TEARINING_08 = 0

TSTACK_085 = 0
TEARINING_085 = 0

TS = 0
TE = 0

for prediction in range(rounds_to_predict):
    prediction = prediction + 1
    path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction)
    tableToRead = pandas.read_csv(path, parse_dates=True)

    for index, row in tableToRead.iterrows():
        TS = TS + 10
        if row[17]:
            TE = TE + 10 * row[23]

        if row[14] > 0.6:
            TSTACK_06 = TSTACK_06 + 10
            cond = row[23]
            if row[17]:
                TEARINING_06 = TEARINING_06 + 10 * row[23]

        if row[14] > 0.65:
            TSTACK_065 = TSTACK_065 + 10
            if row[17]:
                TEARINING_065 = TEARINING_065 + 10 * row[23]

        if row[14] > 0.7:
            TSTACK_07 = TSTACK_07 + 10
            if row[17]:
                TEARINING_07 = TEARINING_07 + 10 * row[23]

        if row[14] > 0.75:
            TSTACK_075 = TSTACK_075 + 10
            if row[17]:
                TEARINING_075 = TEARINING_075 + 10 * row[23]

        if row[14] > 0.8:
            TSTACK_08 = TSTACK_08 + 10
            if row[17]:
                TEARINING_08 = TEARINING_08 + 10 * row[23]

        if row[14] > 0.85:
            TSTACK_085 = TSTACK_085 + 10
            if row[17]:
                TEARINING_085 = TEARINING_085 + 10 * row[23]



totalPre06 = TEARINING_06 / TSTACK_06
totalPre065 = TEARINING_065 / TSTACK_065
totalPre07 = TEARINING_07 / TSTACK_07
totalPre075 = TEARINING_075 / TSTACK_075
totalPre08 = TEARINING_08 / TSTACK_08
totalPre05 = TEARINING_085 / TSTACK_085
totaltotal = TE / TS
x = 5
