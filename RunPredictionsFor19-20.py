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
# def highlight_cols(s):
#     color = 'yellow'
#     return 'background-color: %s' % color
#
#
# def Sort_Tuple_Doubles(tup):
#     return (sorted(tup, key=lambda x: x[5]))
#
#
# for prediction in range(rounds_to_predict):
#
#     TSTACK_06 = 0
#     TEARINING_06 = 0
#     ToalGames_06 = 0
#     TotalWins_06 = 0
#
#     TSTACK_065 = 0
#     TEARINING_065 = 0
#     ToalGames_065 = 0
#     TotalWins_065 = 0
#
#     TSTACK_07 = 0
#     TEARINING_07 = 0
#     ToalGames_07 = 0
#     TotalWins_07 = 0
#
#     TSTACK_075 = 0
#     TEARINING_075 = 0
#     ToalGames_075 = 0
#     TotalWins_075 = 0
#
#     TSTACK_08 = 0
#     TEARINING_08 = 0
#     ToalGames_08 = 0
#     TotalWins_08 = 0
#
#     prediction = prediction + 1
#     path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction)
#     tableToRead = pandas.read_csv(path, parse_dates=True)
#     listOfGames = []
#     for index, row in tableToRead.iterrows():
#         Omega = tableToRead['Expectancy of variance'][index]
#         pair = (index, Omega)
#         listOfGames.append(pair)
#
#         test = row[14]
#         if row[14] > 0.6:
#             TSTACK_06 = TSTACK_06 + 10
#             ToalGames_06 = ToalGames_06 + 1
#             if row[17]:
#                 TotalWins_06 = TotalWins_06 + 1
#                 TEARINING_06 = TEARINING_06 + 10 * row[23]
#
#         if row[14] > 0.65:
#             TSTACK_065 = TSTACK_065 + 10
#             ToalGames_065 = ToalGames_065 + 1
#             if row[17]:
#                 TotalWins_065 = TotalWins_065 + 1
#                 TEARINING_065 = TEARINING_065 + 10 * row[23]
#
#         if row[14] > 0.7:
#             TSTACK_07 = TSTACK_07 + 10
#             ToalGames_07 = ToalGames_07 + 1
#             if row[17]:
#                 TotalWins_07 = TotalWins_07 + 1
#                 TEARINING_07 = TEARINING_07 + 10 * row[23]
#
#         if row[14] > 0.75:
#             TSTACK_075 = TSTACK_075 + 10
#             ToalGames_075 = ToalGames_075 + 1
#             if row[17]:
#                 TotalWins_075 = TotalWins_075 + 1
#                 TEARINING_075 = TEARINING_075 + 10 * row[23]
#
#         if row[14] > 0.8:
#             test1 = row[17]
#             TSTACK_08 = TSTACK_08 + 10
#             ToalGames_08 = ToalGames_08 + 1
#             if row[17]:
#                 TotalWins_08 = TotalWins_08 + 1
#                 TEARINING_08 = TEARINING_08 + 10 * row[23]
#
#     totalPre06 = TEARINING_06 / TSTACK_06
#     totalPre065 = TEARINING_065 / TSTACK_065
#     totalPre07 = TEARINING_07 / TSTACK_07
#     totalPre075 = TEARINING_075 / TSTACK_075
#     totalPre08 = TEARINING_08 / TSTACK_08
#
#     tableToRead.loc[10, '__'] = "Prize rate >0.6 is"
#     tableToRead.loc[10, '_'] = totalPre06
#
#     tableToRead.loc[11, '__'] = "Win rate >0.6 is"
#     tableToRead.loc[11, '_'] = str(float(TotalWins_06 / ToalGames_06) * 100) + "%"
#
#     tableToRead.loc[12, '__'] = "Prize rate >0.65 is"
#     tableToRead.loc[12, '_'] = totalPre065
#
#     tableToRead.loc[13, '__'] = "Win rate >0.65 is"
#     tableToRead.loc[13, '_'] = str(float(TotalWins_065 / ToalGames_065) * 100) + "%"
#
#     tableToRead.loc[14, '__'] = "Prize rate >0.7 is"
#     tableToRead.loc[14, '_'] = totalPre07
#
#     tableToRead.loc[15, '__'] = "Win rate >0.7 is"
#     tableToRead.loc[15, '_'] = str(float(  TotalWins_07/ ToalGames_07) * 100) + "%"
#
#     tableToRead.loc[16, '__'] = "Prize rate >0.75 is"
#     tableToRead.loc[16, '_'] = totalPre075
#
#     tableToRead.loc[17, '__'] = "Win rate >0.75 is"
#     tableToRead.loc[17, '_'] = str(float( TotalWins_075 / ToalGames_075) * 100) + "%"
#
#     tableToRead.loc[18, '__'] = "Prize rate >0.8 is"
#     tableToRead.loc[18, '_'] = totalPre08
#
#     tableToRead.loc[19, '__'] = "Win rate >0.8 is"
#     tableToRead.loc[19, '_'] = str(float( TotalWins_08 / ToalGames_08) * 100) + "%"
#
#     tableToRead['----------------------------'] = ''
#
#     sortedTuples = Sort_Tuple(listOfGames)
#     sortedTuples.reverse()
#     tableToRead['---------------------------------'] = ''
#     index = 0
#     tableToRead['Serial Number_2'] = ''
#     tableToRead['Probability_2'] = ''
#     tableToRead['W Prediction_2'] = ''
#     tableToRead['Odds_2'] = ''
#     tableToRead['Win_2'] = ''
#     tableToRead['Bet_2'] = ''
#     tableToRead['Prize_2'] = ''
#     tableToRead['-----------------'] = ''
#     tableToRead['Win Rate By E*V games'] = ''
#     tableToRead['Win Rate By E*V games Result'] = ''
#
#     best5gamesTrueCounter = 0
#     best5gamesTrueCounterPrize = 0
#     best10gamesTrueCounter = 0
#     best10gamesTrueCounterPrize = 0
#     best15gamesTrueCounter = 0
#     best15gamesTrueCounterPrize = 0
#     best20gamesTrueCounter = 0
#     best20gamesTrueCounterPrize = 0
#
#     for pair in sortedTuples:
#         tableToRead['Serial Number_2'][index] = pair[0]
#         tableToRead['Probability_2'][index] = pair[1]
#         tableToRead['W Prediction_2'][index] = tableToRead['Module Prediction'][pair[0]]
#         tableToRead['Odds_2'][index] = tableToRead['Winner Prediction'][pair[0]]
#         tableToRead['Win_2'][index] = tableToRead['Win'][pair[0]]
#         tableToRead['Bet_2'][index] = 10
#         if tableToRead['Win'][pair[0]] == 1:
#             if index < 5:
#                 best5gamesTrueCounter = best5gamesTrueCounter + 1
#                 best5gamesTrueCounterPrize = best5gamesTrueCounterPrize + 10 * tableToRead['Odds_2'][index]
#             if index < 10:
#                 best10gamesTrueCounter = best10gamesTrueCounter + 1
#                 best10gamesTrueCounterPrize = best10gamesTrueCounterPrize + 10 * tableToRead['Odds_2'][index]
#             if index < 15:
#                 best15gamesTrueCounter = best15gamesTrueCounter + 1
#                 best15gamesTrueCounterPrize = best15gamesTrueCounterPrize + 10 * tableToRead['Odds_2'][index]
#             if index < 20:
#                 best20gamesTrueCounter = best20gamesTrueCounter + 1
#                 best20gamesTrueCounterPrize = best20gamesTrueCounterPrize + 10 * tableToRead['Odds_2'][index]
#             tableToRead['Prize_2'][index] = tableToRead['Bet'][index] * tableToRead['Odds'][index]
#         else:
#             tableToRead['Prize_2'][index] = 0
#
#         index = index + 1
#
#     # Win Rate
#     tableToRead.loc[10, 'Win Rate By E*V games'] = "Best 5 games win rate"
#     tableToRead.loc[10, 'Win Rate By E*V games Result'] = str(float(best5gamesTrueCounter / 5) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[11, 'Win Rate By E*V games'] = "Prize rate for 5 games is"
#     tableToRead.loc[11, 'Win Rate By E*V games Result'] = float(best5gamesTrueCounterPrize / (5 * 10))
#
#     # Win Rate
#     tableToRead.loc[12, 'Win Rate By E*V games'] = "Best 10 games win rate"
#     tableToRead.loc[12, 'Win Rate By E*V games Result'] = str(float(best10gamesTrueCounter / 10) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[13, 'Win Rate By E*V games'] = "Prize rate for 10 games is "
#     tableToRead.loc[13, 'Win Rate By E*V games Result'] = float(best10gamesTrueCounterPrize / (10 * 10))
#
#     # Win Rate
#     tableToRead.loc[14, 'Win Rate By E*V games'] = "Best 15 games win rate"
#     tableToRead.loc[14, 'Win Rate By E*V games Result'] = str(float(best15gamesTrueCounter / 15) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[15, 'Win Rate By E*V games'] = "Prize rate for 15 games is "
#     tableToRead.loc[15, 'Win Rate By E*V games Result'] = float(best15gamesTrueCounterPrize / (15 * 10))
#
#     # Win Rate
#     tableToRead.loc[16, 'Win Rate By E*V games'] = "Best 20 games win rate"
#     tableToRead.loc[16, 'Win Rate By E*V games Result'] = str(float(best20gamesTrueCounter / 20) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[17, 'Win Rate By E*V games'] = "Prize rate for 20 games is "
#     tableToRead.loc[17, 'Win Rate By E*V games Result'] = float(best20gamesTrueCounterPrize / (20 * 10))
#
#     tableToRead['----------------------------------'] = ''
#     listOfDoubles = []
#     for index_1, row_1 in tableToRead.iterrows():
#         for index_2, row_2 in tableToRead.iterrows():
#             if (index_1 > index_2):
#                 probabilty = tableToRead['Max Probability'][index_1] * tableToRead['Max Probability'][index_2]
#                 odds = tableToRead['Winner Prediction'][index_1] * tableToRead['Winner Prediction'][index_2]
#                 isWin = 'False'
#                 if tableToRead['Win'][index_1] == 1:
#                     if tableToRead['Win'][index_2] == 1:
#                         isWin = 'True'
#                 ExpectancyOfVariance = probabilty * odds - 1
#                 touple = (index_1, index_2, probabilty, odds, isWin, ExpectancyOfVariance)
#                 listOfDoubles.append(touple)
#
#     tableToRead['Serial Number Game1'] = ''
#     tableToRead['Serial Number Game2'] = ''
#     tableToRead['Probability Double'] = ''
#     tableToRead['Odds Double'] = ''
#     tableToRead['Win Double'] = ''
#     tableToRead['Expectancy of variance Double'] = ''
#     tableToRead['------------------------'] = ''
#     tableToRead['Win Rate by E*V double'] = ''
#     tableToRead['Win Rate by E*V double result'] = ''
#
#     counterDoubleGamesTrue3 = 0
#     counterDoubleGamesTrue5 = 0
#     counterDoubleGamesTrue10 = 0
#     counterPrizeRate3 = 0
#     counterPrizeRate5 = 0
#     counterPrizeRate10 = 0
#
#     counterDoubleGamesTrue3Dif = 0
#     counterDoubleGamesTrue5Dif = 0
#     counterDoubleGamesTrue10Dif = 0
#     counterPrizeRate3Dif = 0
#     counterPrizeRate5Dif = 0
#     counterPrizeRate10Dif = 0
#
#     sortedT = Sort_Tuple_Doubles(listOfDoubles)
#     sortedT.reverse()
#     doubleIndex = 0
#     for game in range(10):
#         doubleIndex = doubleIndex + 1
#         tableToRead['Serial Number Game1'][doubleIndex] = sortedT[game][0]
#         tableToRead['Serial Number Game2'][doubleIndex] = sortedT[game][1]
#         tableToRead['Probability Double'][doubleIndex] = sortedT[game][2]
#         tableToRead['Odds Double'][doubleIndex] = sortedT[game][3]
#         tableToRead['Win Double'][doubleIndex] = sortedT[game][4]
#         tableToRead['Expectancy of variance Double'][doubleIndex] = sortedT[game][5]
#
#         if doubleIndex <= 3:
#             if sortedT[game][4] == 'True':
#                 counterDoubleGamesTrue3 = counterDoubleGamesTrue3 + 1
#                 counterPrizeRate3 = counterPrizeRate3 + 20 * sortedT[game][3]
#
#         if doubleIndex <= 5:
#             if sortedT[game][4] == 'True':
#                 counterDoubleGamesTrue5 = counterDoubleGamesTrue5 + 1
#                 counterPrizeRate5 = counterPrizeRate5 + 20 * sortedT[game][3]
#         if doubleIndex <= 10:
#             if sortedT[game][4] == 'True':
#                 counterDoubleGamesTrue10 = counterDoubleGamesTrue10 + 1
#                 counterPrizeRate10 = counterPrizeRate10 + 20 * sortedT[game][3]
#
#     doubleIndex = doubleIndex + 2
#
#
#     difCounter = 0
#     CounterIndex = 0
#     listOfSn = []
#     while(difCounter < 10):
#         try:
#             sn1 = sortedT[CounterIndex][0]
#             sn2 = sortedT[CounterIndex][1]
#             if sn1 not in listOfSn:
#                 if sn2 not in listOfSn:
#                     listOfSn.append(sn1)
#                     listOfSn.append(sn2)
#                     tableToRead['Serial Number Game1'][doubleIndex] = sortedT[CounterIndex][0]
#                     tableToRead['Serial Number Game2'][doubleIndex] = sortedT[CounterIndex][1]
#                     tableToRead['Probability Double'][doubleIndex] = sortedT[CounterIndex][2]
#                     tableToRead['Odds Double'][doubleIndex] = sortedT[CounterIndex][3]
#                     tableToRead['Win Double'][doubleIndex] = sortedT[CounterIndex][4]
#                     tableToRead['Expectancy of variance Double'][doubleIndex] = sortedT[CounterIndex][5]
#                     if difCounter < 3:
#                         if sortedT[CounterIndex][4] == 'True':
#                             counterDoubleGamesTrue3Dif = counterDoubleGamesTrue3Dif + 1
#                             counterPrizeRate3Dif = counterPrizeRate3Dif + 20 * sortedT[CounterIndex][3]
#                     if difCounter < 5:
#                         if sortedT[CounterIndex][4] == 'True':
#                             counterDoubleGamesTrue5Dif = counterDoubleGamesTrue5Dif + 1
#                             counterPrizeRate5Dif = counterPrizeRate5Dif + 20 * sortedT[CounterIndex][3]
#                     if difCounter < 10:
#                         if sortedT[CounterIndex][4] == 'True':
#                             counterDoubleGamesTrue10Dif = counterDoubleGamesTrue10Dif + 1
#                             counterPrizeRate10Dif = counterPrizeRate10Dif + 20 * sortedT[CounterIndex][3]
#
#                     doubleIndex = doubleIndex + 1
#                     difCounter = difCounter + 1
#             CounterIndex = CounterIndex + 1
#         except:
#             break
#
#     # Win rate
#     tableToRead.loc[8, 'Win Rate by E*V double'] = "Best 3 Double games win rate"
#     tableToRead.loc[8, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue3 / 3) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[9, 'Win Rate by E*V double'] = "Prize rate for 3 Double games is"
#     tableToRead.loc[9, 'Win Rate by E*V double result'] = float(counterPrizeRate3 / (3 * 20))
#
#     # Win rate
#     tableToRead.loc[10, 'Win Rate by E*V double'] = "Best 5 Double games win rate"
#     tableToRead.loc[10, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue5 / 5) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[11, 'Win Rate by E*V double'] = "Prize rate for 5 Double games is"
#     tableToRead.loc[11, 'Win Rate by E*V double result'] = float(counterPrizeRate5 / (5 * 20))
#
#     # Win rate
#     tableToRead.loc[12, 'Win Rate by E*V double'] = "Best 10 Double games win rate"
#     tableToRead.loc[12, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue10 / 10) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[13, 'Win Rate by E*V double'] = "Prize rate for 10 Double games is"
#     tableToRead.loc[13, 'Win Rate by E*V double result'] = float(counterPrizeRate10 / (10 * 20))
#
#
#
#     # Win rate
#     tableToRead.loc[14, 'Win Rate by E*V double'] = "Best 3 Double games win rate Dif"
#     tableToRead.loc[14, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue3Dif / 3) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[15, 'Win Rate by E*V double'] = "Prize rate for 3 Double games Dif is"
#     tableToRead.loc[15, 'Win Rate by E*V double result'] = float(counterPrizeRate3Dif / (3 * 20))
#
#     # Win rate
#     tableToRead.loc[16, 'Win Rate by E*V double'] = "Best 5 Double games win rate Dif"
#     tableToRead.loc[16, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue5Dif / 5) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[17, 'Win Rate by E*V double'] = "Prize rate for 5 Double games Dif is"
#     tableToRead.loc[17, 'Win Rate by E*V double result'] = float(counterPrizeRate5Dif / (5 * 20))
#
#     # Win rate
#     tableToRead.loc[18, 'Win Rate by E*V double'] = "Best 10 Double games win rate Dif"
#     tableToRead.loc[18, 'Win Rate by E*V double result'] = str(float(counterDoubleGamesTrue10Dif / 10) * 100) + "%"
#     # Prize Win Rate
#     tableToRead.loc[19, 'Win Rate by E*V double'] = "Prize rate for 10 Double games Dif is"
#     tableToRead.loc[19, 'Win Rate by E*V double result'] = float(counterPrizeRate10Dif / (10 * 20))
#
#
#     tableToRead.style.highlight_null(null_color='red')
#     tableToRead.to_csv(
#         str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction),
#         index=False)

avgSingle06 = 0
avgSingle065 = 0
avgSingle07 = 0
avgSingle075 = 0
avgSingle08 = 0

avgSingleByTohelt5 = 0
avgSingleByTohelt10 = 0
avgSingleByTohelt15 = 0
avgSingleByTohelt20 = 0

avgDoubleByTohelt3 = 0
avgDoubleByTohelt5 = 0
avgDoubleByTohelt10 = 0

avgDoubleByToheltDif3 = 0
avgDoubleByToheltDif5 = 0
avgDoubleByToheltDif10 = 0

for prediction in range(rounds_to_predict):
    prediction = prediction + 1
    path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection, prediction)
    tableToRead = pandas.read_csv(path, parse_dates=True)

    avgSingle06 = avgSingle06 + float(tableToRead['_'][10])
    avgSingle065 = avgSingle065 + float(tableToRead['_'][12])
    avgSingle07 = avgSingle07 + float(tableToRead['_'][14])
    avgSingle075 = avgSingle075 + float(tableToRead['_'][16])
    avgSingle08 = avgSingle08 + float(tableToRead['_'][18])

    avgSingleByTohelt5 = avgSingleByTohelt5 + float(tableToRead['Win Rate By E*V games Result'][11])
    avgSingleByTohelt10 = avgSingleByTohelt10 + float(tableToRead['Win Rate By E*V games Result'][13])
    avgSingleByTohelt15 = avgSingleByTohelt15 + float(tableToRead['Win Rate By E*V games Result'][15])
    avgSingleByTohelt20 = avgSingleByTohelt20 + float(tableToRead['Win Rate By E*V games Result'][17])

    avgDoubleByTohelt3 = avgDoubleByTohelt3 + float(tableToRead['Win Rate by E*V double result'][9])
    avgDoubleByTohelt5 = avgDoubleByTohelt5 + float(tableToRead['Win Rate by E*V double result'][11])
    avgDoubleByTohelt10 = avgDoubleByTohelt10 + float(tableToRead['Win Rate by E*V double result'][13])

    avgDoubleByToheltDif3 = avgDoubleByToheltDif3 + float(tableToRead['Win Rate by E*V double result'][15])
    avgDoubleByToheltDif5 = avgDoubleByToheltDif5 + float(tableToRead['Win Rate by E*V double result'][17])
    avgDoubleByToheltDif10 = avgDoubleByToheltDif10 + float(tableToRead['Win Rate by E*V double result'][19])

print('single by prob >0.6 is ' + str(avgSingle06 / rounds_to_predict))
print('single by prob >0.65 is ' + str(avgSingle065 / rounds_to_predict))
print('single by prob >0.7 is ' + str(avgSingle07 / rounds_to_predict))
print('single by prob >0.75 is ' + str(avgSingle075 / rounds_to_predict))
print('single by prob >0.8 is ' + str(avgSingle08 / rounds_to_predict))

print('single by Expectancy of variance Best of 5 games is ' + str(avgSingleByTohelt5 / rounds_to_predict))
print('single by Expectancy of variance Best of 10 games is ' + str(avgSingleByTohelt10 / rounds_to_predict))
print('single by Expectancy of variance Best of 15 games is ' + str(avgSingleByTohelt15 / rounds_to_predict))
print('single by Expectancy of variance Best of 20 games is ' + str(avgSingleByTohelt20 / rounds_to_predict))

print(
    'double by Expectancy of variance Best of 3 games with repetition is ' + str(avgDoubleByTohelt3 / rounds_to_predict))
print(
    'double by Expectancy of variance Best of 5 games with repetition is ' + str(avgDoubleByTohelt5 / rounds_to_predict))
print(
    'double by Expectancy of variance Best of 10 games with repetition is ' + str(avgDoubleByTohelt10 / rounds_to_predict))

print(
    'double by Expectancy of variance Best of 3 games with no repetition is ' + str(avgDoubleByToheltDif3 / rounds_to_predict))
print(
    'double by Expectancy of variance Best of 5 games with no repetition is ' + str(avgDoubleByToheltDif5 / rounds_to_predict))
print(
    'double by Expectancy of variance Best of 10 games with no repetition is ' + str(avgDoubleByToheltDif10 / rounds_to_predict))
