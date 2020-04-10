from Persistent.Data import _BettingStats  # 1
from Persistent.Data import _teamsGoalsScoredReceived  # 2
from Persistent.Data import _teamsGoalsScoredReceivedNormal  # 3
from Persistent.Data import _combineStanding  # 4
from Persistent.Data import _combineGoalsAadStanding  # 5
from Persistent.Data import _GetCorrentRound  # 6
from Persistent.Data import _UpcomingBettingOddsWithAPI  # 7
from Persistent.Data import _updateFiles  # 8
import os

# [ Serie , PremierLeague , Bundesliga , Laliga ]
League = "Serie"

years = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# years = [5]


for year in years:

    startYear = year
    endYear = startYear + 1
    startYear_C = startYear
    endYear_C = endYear

    if League == "Bundesliga":
        _round = 34
    else:
        _round = 38

    if startYear < 10:
        startYear_C = "0" + str(startYear)
    if endYear < 10:
        endYear_C = "0" + str(endYear)

    _updateFiles.run(League, startYear_C, endYear_C)
    _BettingStats.run(League, _round, startYear, endYear)
    _teamsGoalsScoredReceived.run(League, _round, startYear, endYear)
    _teamsGoalsScoredReceivedNormal.run(League, _round, startYear, endYear)
    _combineStanding.run(League, _round, startYear, endYear)
    _combineGoalsAadStanding.run(League, _round, startYear, endYear)
    # _GetCorrentRound.run(League,_round)    #TODO : only for prdicet
    # _UpcomingBettingOddsWithAPI.run(League,_round) #TODO : only for prdicet
    _updateFiles.combineToFinal(League, startYear, endYear)
    _updateFiles.cleanAllFile(League, startYear, endYear)

    os.remove(League + "-" + str(startYear_C) + "-" + str(endYear_C) + ".csv")

    print("Finished the run successfully !!!")
    print("Finished the run successfully !!!")
    print("Finished the run successfully !!!")
    print("Finished the run successfully !!!")
