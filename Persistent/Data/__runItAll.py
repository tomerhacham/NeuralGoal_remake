from Persistent.Data import _BettingStats  # 1
from Persistent.Data import _teamsGoalsScoredReceived  # 2
from Persistent.Data import _teamsGoalsScoredReceivedNormal  # 3
from Persistent.Data import _combineStanding  # 4
from Persistent.Data import _combineGoalsAadStanding  # 5
from Persistent.Data import _GetCorrentRound  # 6
from Persistent.Data import _UpcomingBettingOddsWithAPI  # 7
from Persistent.Data import _updateFiles  # 8
from Persistent.Data import _UpcomingFromWinner
from Persistent.Data import newLeagueValidation  # for adding new leagues
from Persistent.Data.utils import getRoundPerLeague
import os

#leagues = ["Serie", "PremierLeague", "Bundesliga", "Laliga", "Ligue1", "Jupiler", "Eredivisie" , "Scotish" , "Portugal"]



leagues = ["Ligue1"]

#years = [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
years = [20]


for League in range(len(leagues)):
    for year in range(len(years)):
        startYear = years[year]
        endYear = startYear + 1
        startYear_C = startYear
        endYear_C = endYear

        league = str(leagues[League])
        _round = getRoundPerLeague(league,startYear)

        if startYear < 10:
            startYear_C = "0" + str(startYear)
        if endYear < 10:
            endYear_C = "0" + str(endYear)

        # # TODO : FOR NEW LEAGUE
        # listOfNotFound = []
        # listOfNamesToConvert = []
        # for year in range(5,20):
        #     newLeagueValidation.run("Scotish",year,year+1,"SC0")
        #     if year != 7:
        #         listOfNotFound.extend(newLeagueValidation.validate("Scotish",year,year+1))
        # for Gyear in range(5, 20):
        #     listOfNamesToConvert.extend(newLeagueValidation.getAllNames("sco-premiership-", Gyear, Gyear + 1))
        # print(list(set(listOfNotFound)))
        # print(list(set(listOfNamesToConvert)), sep='\n')
        # # TODO : END OF NEW LEAGUE



        # # Download All games until the current round from https://www.football-data.co.uk/
        # _updateFiles.run(league, startYear_C, endYear_C)
        # #
        # # {League name}-20-21-Final-Stats
        # _BettingStats.run(league, _round, startYear, endYear)
        #
        # # standing-20-21
        # _teamsGoalsScoredReceived.run(league, _round, startYear, endYear)
        #
        # # standing-8-9-AVG
        # _teamsGoalsScoredReceivedNormal.run(league, _round, startYear, endYear)
        #
        # # standing-8-9-Teams
        # _combineStanding.run(league, _round, startYear, endYear)
        #
        # # {League}-8-9-Goals-AVG3
        # _combineGoalsAadStanding.run(league, _round, startYear, endYear)


        #_GetCorrentRound.run(league,startYear)
        #_UpcomingBettingOddsWithAPI.run(league)
        _UpcomingFromWinner.run(league)



        # _updateFiles.combineToFinal(league, startYear, endYear)
        # _updateFiles.cleanAllFile(league, startYear, endYear)

        # os.remove(league + "-" + str(startYear_C) + "-" + str(endYear_C) + ".csv")

        print("Finished the run successfully !!!")
        print("Finished the run successfully !!!")
        print("Finished the run successfully !!!")
        print("Finished the run successfully !!!")

