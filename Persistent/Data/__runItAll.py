from Persistent.Data import _BettingStats  # 1
from Persistent.Data import _teamsGoalsScoredReceived  # 2
from Persistent.Data import _teamsGoalsScoredReceivedNormal  # 3
from Persistent.Data import _combineStanding  # 4
from Persistent.Data import _combineGoalsAadStanding  # 5
from Persistent.Data import _GetCorrentRound  # 6
#from Persistent.Data import _UpcomingBettingOddsWithAPI  # 7
from Persistent.Data import _updateFiles  # 8
from Persistent.Data import newLeagueValidation  # for adding new leagues
import os

# [ Serie , PremierLeague , Bundesliga , Laliga , Ligue1 , Jupiler ,  Eredivisie ]
League = "PremierLeague"

#years = [5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
years = [19]

for year in years:
    #try:
    startYear = year
    endYear = startYear + 1
    startYear_C = startYear
    endYear_C = endYear

    if League == "Bundesliga" or "Eredivisie":
        _round = 34
    elif League == "Jupiler":
        if startYear <= 8:
            _round = 34
        else:
            _round = 30
    else:
        _round = 38

    if startYear < 10:
        startYear_C = "0" + str(startYear)
    if endYear < 10:
        endYear_C = "0" + str(endYear)

    # TODO : FOR NEW LEAGUE
    # listOfNotFound = []
    # listOfNamesToConvert = []
    # for year in range(5,20):
    #     newLeagueValidation.run("Eredivisie",year,year+1,"N1")
    #     if year != 7:
    #         listOfNotFound.extend(newLeagueValidation.validate("Eredivisie",year,year+1))
    # for Gyear in range(5, 20):
    #     listOfNamesToConvert.extend(newLeagueValidation.getAllNames("ned-eredivisie-", Gyear, Gyear + 1))
    #  print(list(set(listOfNotFound)))
    # print(list(set(listOfNamesToConvert)), sep='\n')
    # TODO : END OF NEW LEAGUE

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
    #except:
    #    print(str(startYear) + " redo")
    #    continue
