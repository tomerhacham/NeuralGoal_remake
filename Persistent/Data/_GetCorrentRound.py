import pandas
import csv
import numpy
from bs4 import BeautifulSoup
import requests

    
def run(leagueName,round):

    sY = 19
    eY = 20 
    path = "standing-" + str(sY) + "-" + str(eY) + "-AVG-Goals.csv"

    teamScore = pandas.read_csv(path)
    MAIN_URL = "https://www.fifaindex.com/teams/fifa"

    def getNameToFifaIndex(nameToChange):

        if nameToChange == "Ein Frankfurt":
            return "Frankfurt&league=19"
        
        if nameToChange == "Bayern Munich":
            return "Bayern&league=19"

        # PremierLeague
        if nameToChange == "Man City":
            return "Manchester City"
        
        if nameToChange == "Man United":
            return "Manchester United"
        
        if nameToChange == "Newcastle":
            return "Newcastle United"
        
        # Serie
        if nameToChange == "Inter":
            return "Inter&league=31"
        
        if nameToChange == "Reggina":
            return "Reggi"
        
        if nameToChange == "Ascoli":
            return "Ascoli&league=31"
        
        if nameToChange == "Bari":
            return "Bari&league=31"
        
        if nameToChange == "Verona":
            return "Hellas"

        #16-17
        if nameToChange == "La Coruna":
            return "RC Deportivo"
        
        if nameToChange == "Sevilla":
            return "Sevilla&league=53"
        
        if nameToChange == "Espanol":
            return "RCD Espanyol"
        
        if nameToChange == "Ath Madrid":
            return "Atlético Madrid"
        
        if nameToChange == "Sociedad":
            return "Sociedad&league=53"
        
        if nameToChange == "Sp Gijon":
            return "Sporting&league=53"
        
        if nameToChange == "Ath Bilbao":
            return "Bilbao"
        
        if nameToChange == "FC Barcelona":
            return "FC Barcelona&league=53"

        return nameToChange

    def getTeamName(nameToFind):
        # Bundesliga
        if nameToFind == "Bayern München":  return "Bayern Munich"
        if nameToFind == "1. FC Köln":  return "FC Koln"
        if nameToFind == "VfL Wolfsburg":  return "Wolfsburg"
        if nameToFind == "Bor. Mönchengladbach":  return "M'gladbach"
        if nameToFind == "Borussia Dortmund":  return "Dortmund"
        if nameToFind == "Hertha BSC":  return "Hertha"
        if nameToFind == "Eintracht Frankfurt":  return "Ein Frankfurt"
        if nameToFind == "1899 Hoffenheim":  return "Hoffenheim"
        if nameToFind == "RB Leipzig":  return "RB Leipzig"
        if nameToFind == "FC Ingolstadt 04":  return "Ingolstadt"
        if nameToFind == "Hamburger SV":  return "Hamburg"
        if nameToFind == "1. FSV Mainz 05":  return "Mainz"
        if nameToFind == "Bayer Leverkusen":  return "Leverkusen"
        if nameToFind == "SC Freiburg":  return "Freiburg"           
        if nameToFind == "FC Schalke 04":  return "Schalke 04"
        if nameToFind == "FC Augsburg":  return "Augsburg"        
        if nameToFind == "SV Darmstadt 98":  return "Darmstadt"
        if nameToFind == "Werder Bremen":  return "Werder Bremen"
        if nameToFind == "Hannover 96": return "Hannover"
        if nameToFind == "VfB Stuttgart": return "Stuttgart"
        if nameToFind == "1. FC Nürnberg": return "Nurnberg"
        if nameToFind == "Fortuna Düsseldorf": return "Fortuna Dusseldorf"
        if nameToFind == "Hansa Rostock": return "Hansa Rostock"
        if nameToFind == "VfL Bochum": return "Bochum"
        if nameToFind == "Arminia Bielefeld": return "Bielefeld"
        if nameToFind == "1. FC Kaiserslautern": return "Kaiserslautern"
        if nameToFind == "MSV Duisburg": return "Duisburg"
        if nameToFind == "Alemannia Aachen": return "Aachen"
        if nameToFind == "Energie Cottbus": return "Cottbus"
        if nameToFind == "Karlsruher SC": return "Karlsruhe"
        if nameToFind == "FC St. Pauli": return "St Pauli"
        if nameToFind == "1. FC Union Berlin": return "Union Berlin"
        if nameToFind == "SpVgg Greuther Fürth": return "Greuther Furth"
        if nameToFind == "Eintracht Braunschweig": return "Braunschweig"
        if nameToFind == "SC Paderborn 07": return "Paderborn"
        # Premier League
        if nameToFind == "Chelsea FC": return "Chelsea"
        if nameToFind == "Manchester United": return "Man United"
        if nameToFind == "Liverpool FC": return "Liverpool"
        if nameToFind == "Arsenal FC": return "Arsenal"
        if nameToFind == "Tottenham Hotspur": return "Tottenham"
        if nameToFind == "Blackburn Rovers": return "Blackburn"
        if nameToFind == "Newcastle United": return "Newcastle"
        if nameToFind == "Bolton Wanderers": return "Bolton"
        if nameToFind == "West Ham United": return "West Ham"
        if nameToFind == "Wigan Athletic": return "Wigan"
        if nameToFind == "Everton FC": return "Everton"
        if nameToFind == "Fulham FC": return "Fulham"
        if nameToFind == "Charlton Athletic": return "Charlton"
        if nameToFind == "Middlesbrough FC": return "Middlesbrough"
        if nameToFind == "Manchester City": return "Man City"
        if nameToFind == "Aston Villa": return "Aston Villa"
        if nameToFind == "Portsmouth FC": return "Portsmouth"
        if nameToFind == "Birmingham City": return "Birmingham"
        if nameToFind == "West Bromwich Albion": return "West Brom"
        if nameToFind == "Sunderland AFC": return "Sunderland"
        if nameToFind == "Reading FC": return "Reading"
        if nameToFind == "Sheffield United": return "Sheffield United"
        if nameToFind == "Watford FC": return "Watford"
        if nameToFind == "Derby County": return "Derby"
        if nameToFind == "Hull City": return "Hull"
        if nameToFind == "Stoke City": return "Stoke"
        if nameToFind == "Burnley FC": return "Burnley"
        if nameToFind == "Wolverhampton Wanderers": return "Wolves"
        if nameToFind == "Blackpool FC": return "Blackpool"
        if nameToFind == "Queens Park Rangers": return "QPR"
        if nameToFind == "Norwich City": return "Norwich"
        if nameToFind == "Swansea City": return "Swansea"
        if nameToFind == "Southampton FC": return "Southampton"
        if nameToFind == "Cardiff City": return "Cardiff"
        if nameToFind == "Crystal Palace": return "Crystal Palace"
        if nameToFind == "Leicester City": return "Leicester"
        if nameToFind == "AFC Bournemouth": return "Bournemouth"
        if nameToFind == "Huddersfield Town": return "Huddersfield"
        if nameToFind == "Brighton & Hove Albion": return "Brighton"

        if nameToFind == "Juventus": return "Juventus"
        if nameToFind == "Inter": return "Inter"
        if nameToFind == "AS Roma": return "Roma"
        if nameToFind == "AC Milan": return "Milan"
        if nameToFind == "Chievo Verona": return "Chievo"
        if nameToFind == "US Palermo": return "Palermo"
        if nameToFind == "AS Livorno": return "Livorno"
        if nameToFind == "Empoli FC": return "Empoli"
        if nameToFind == "Parma FC": return "Parma"
        if nameToFind == "ACF Fiorentina": return "Fiorentina"
        if nameToFind == "Ascoli Calcio": return "Ascoli"
        if nameToFind == "Udinese Calcio": return "Udinese"
        if nameToFind == "Sampdoria": return "Sampdoria"
        if nameToFind == "Reggina Calcio": return "Reggina"
        if nameToFind == "Cagliari Calcio": return "Cagliari"
        if nameToFind == "AC Siena": return "Siena"
        if nameToFind == "Lazio Roma": return "Lazio"
        if nameToFind == "FC Messina": return "Messina"
        if nameToFind == "US Lecce": return "Lecce"
        if nameToFind == "Treviso FBC": return "Treviso"
        if nameToFind == "Atalanta": return "Atalanta"
        if nameToFind == "Calcio Catania": return "Catania"
        if nameToFind == "Torino FC": return "Torino"
        if nameToFind == "SSC Napoli": return "Napoli"
        if nameToFind == "Genoa CFC": return "Genoa"
        if nameToFind == "Bologna FC": return "Bologna"
        if nameToFind == "AS Bari": return "Bari"
        if nameToFind == "AC Cesena": return "Cesena"
        if nameToFind == "Novara Calcio": return "Novara"
        if nameToFind == "Pescara Calcio": return "Pescara"
        if nameToFind == "Sassuolo Calcio": return "Sassuolo"
        if nameToFind == "Hellas Verona": return "Verona"
        if nameToFind == "Frosinone Calcio": return "Frosinone"
        if nameToFind == "Carpi FC": return "Carpi"
        if nameToFind == "FC Crotone": return "Crotone"
        if nameToFind == "Benevento Calcio": return "Benevento"
        if nameToFind == "SPAL 2013 Ferrara": return "Spal"
        if nameToFind == "Parma Calcio 1913": return "Parma"
        if nameToFind == "Brescia Calcio": return "Brescia"
        # La Liga
        if nameToFind == "Real Madrid": return "Real Madrid"
        if nameToFind == "FC Barcelona": return "Barcelona"
        if nameToFind == "Atlético Madrid": return "Ath Madrid"
        if nameToFind == "Sevilla FC": return "Sevilla"
        if nameToFind == "Villarreal CF": return "Villarreal"
        if nameToFind == "Real Sociedad": return "Sociedad"
        if nameToFind == "Athletic Bilbao": return "Ath Bilbao"
        if nameToFind == "Espanyol Barcelona": return "Espanol"
        if nameToFind == "CD Alavés": return "Alaves"
        if nameToFind == "SD Eibar": return "Eibar"
        if nameToFind == "Málaga CF": return "Malaga"
        if nameToFind == "Valencia CF": return "Valencia"
        if nameToFind == "Celta Vigo": return "Celta"
        if nameToFind == "UD Las Palmas": return "Las Palmas"
        if nameToFind == "Real Betis": return "Betis"
        if nameToFind == "Deportivo La Coruña": return "La Coruna"
        if nameToFind == "CD Leganés": return "Leganes"
        if nameToFind == "Sporting Gijón": return "Sp Gijon"
        if nameToFind == "CA Osasuna": return "Osasuna"
        if nameToFind == "Granada CF": return "Granada"
        if nameToFind == "Getafe CF": return "Getafe"
        if nameToFind == "Girona FC": return "Girona"
        if nameToFind == "Levante UD": return "Levante"
        if nameToFind == "Real Valladolid": return "Valladolid"
        if nameToFind == "SD Huesca": return "Huesca"
        if nameToFind == "Rayo Vallecano": return "Vallecano"
        if nameToFind == "RCD Mallorca": return "Mallorca"
        # ligue1
        if nameToFind == "Olympique Lyon": return "Lyon"
        if nameToFind == "Girondins Bordeaux": return "Bordeaux"
        if nameToFind == "Lille OSC": return "Lille"
        if nameToFind == "RC Lens": return "Lens"
        if nameToFind == "Olympique Marseille": return "Marseille"
        if nameToFind == "AJ Auxerre": return "Auxerre"
        if nameToFind == "Stade Rennes": return "Rennes"
        if nameToFind == "OGC Nice": return "Nice"
        if nameToFind == "Paris Saint-Germain": return "Paris SG"
        if nameToFind == "AS Monaco": return "Monaco"
        if nameToFind == "Le Mans UC 72": return "Le Mans"
        if nameToFind == "AS Nancy": return "Nancy"
        if nameToFind == "AS Saint-Étienne": return "St Etienne"
        if nameToFind == "FC Nantes": return "Nantes"
        if nameToFind == "FC Sochaux": return "Sochaux"
        if nameToFind == "Toulouse FC": return "Toulouse"
        if nameToFind == "ESTAC Troyes": return "Troyes"
        if nameToFind == "AC Ajaccio": return "Ajaccio"
        if nameToFind == "RC Strasbourg": return "Strasbourg"
        if nameToFind == "FC Metz": return "Metz"
        if nameToFind == "FC Lorient": return "Lorient"
        if nameToFind == "Valenciennes FC": return "Valenciennes"
        if nameToFind == "CS Sedan": return "Sedan"
        if nameToFind == "SM Caen": return "Caen"
        if nameToFind == "Grenoble Foot 38": return "Grenoble"
        if nameToFind == "Le Havre AC": return "Le Havre"
        if nameToFind == "US Boulogne": return "Boulogne"
        if nameToFind == "Montpellier HSC": return "Montpellier"
        if nameToFind == "Stade Brest": return "Brest"
        if nameToFind == "AC Arles-Avignon": return "Arles"
        if nameToFind == "Dijon FCO": return "Dijon"
        if nameToFind == "Évian Thonon Gaillard": return "Evian Thonon Gaillard"
        if nameToFind == "Stade Reims": return "Reims"
        if nameToFind == "EA Guingamp": return "Guingamp"
        if nameToFind == "GFC Ajaccio": return "Ajaccio GFCO"
        if nameToFind == "Angers SCO": return "Angers"
        if nameToFind == "Amiens SC": return "Amiens"
        if nameToFind == "Nîmes Olympique": return "Nimes"
        if nameToFind == "SC Bastia": return "Bastia"
        # Jupiler
        if nameToFind == "RSC Anderlecht": return "Anderlecht"
        if nameToFind == "Standard Liège": return "Standard"
        if nameToFind == "Club Brugge KV": return "Club Brugge"
        if nameToFind == "KAA Gent": return "Gent"
        if nameToFind == "KRC Genk": return "Genk"
        if nameToFind == "Germinal Beerschot": return "Germinal"
        if nameToFind == "SV Zulte Waregem": return "Waregem"
        if nameToFind == "Sporting Lokeren": return "Lokeren"
        if nameToFind == "FC Brussels": return "FC Brussels"
        if nameToFind == "KVC Westerlo": return "Westerlo"
        if nameToFind == "Sporting Charleroi": return "Charleroi"
        if nameToFind == "KSV Roeselare": return "Roeselare"
        if nameToFind == "Excelsior Mouscron": return "Mouscron"
        if nameToFind == "Cercle Brugge": return "Cercle Brugge"
        if nameToFind == "Sint-Truidense VV": return "St Truiden"
        if nameToFind == "KSK Beveren": return "Beveren"
        if nameToFind == "Lierse SK": return "Lierse"
        if nameToFind == "RAA La Louviéroise": return "Louvieroise"
        if nameToFind == "RAEC Mons": return "Bergen"
        if nameToFind == "KV Mechelen": return "Mechelen"
        if nameToFind == "FCV Dender EH": return "Dender"
        if nameToFind == "KV Kortrijk": return "Kortrijk"
        if nameToFind == "AFC Tubize": return "Tubize"
        if nameToFind == "AS Eupen": return "Eupen"
        if nameToFind == "Beerschot AC": return "Germinal"
        if nameToFind == "Oud-Heverlee Leuven": return "Oud-Heverlee Leuven"
        if nameToFind == "Waasland-Beveren": return "Waasland-Beveren"
        if nameToFind == "KV Oostende": return "Oostende"
        if nameToFind == "Royal Mouscron-Péruwelz": return "Mouscron-Peruwelz"
        if nameToFind == "Royal Excel Mouscron": return "Mouscron"
        if nameToFind == "Royal Antwerp FC": return "Antwerp"
        if nameToFind == "Royal Excel Mouscron Péruwelz": return "Mouscron"

    def getLastScoredGoals(teamName,leagueName,Cround):
        scoredGaols = teamScore.loc[Cround,teamName + " scored"]
        return scoredGaols

    def getLastRecivedGoals(teamName,leagueName,Cround):
        scoredGaols = teamScore.loc[Cround,teamName + " received"]
        return scoredGaols
    
    table = []

    _round = round

    _le = ""
    if leagueName == "Bundesliga":
        _le = "bundesliga-"
    elif leagueName == "Laliga":
        _le = "esp-primera-division-"
    elif leagueName == "PremierLeague":
        _le = "eng-premier-league-"
    elif leagueName == "Serie":
        _le = "ita-serie-a-"
    elif leagueName == "Ligue1":
        _le = "fra-ligue-1-"
    elif leagueName == "Jupiler":
        if int(sY) <= 10:
            _le = "bel-jupiler-league-"
        elif int(sY) <= 12:
            _le = "bel-jupiler-pro-league-"
        elif int(sY) <= 16:
            _le = "bel-eerste-klasse-"
        else:
            _le = "bel-eerste-klasse-a-"

    if leagueName == "Laliga" and sY == "16":
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag_2/".format(sY,eY))
    else:
        data = requests.get("https://www.worldfootball.net/schedule/" + _le + "20{}-20{}-spieltag/".format(sY,eY))
    teamData = data.content
    games = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[0].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})
    standing = BeautifulSoup(teamData,"html.parser").find_all("div",{"class":"box"})[1].find("table",{"class":"standard_tabelle"}).find_all("tr",{"":""})

    standing_teams = []

    for team in standing:
        try:
            data = team.find("a",{"":""})
            teams_name = data.text
            team_name = getTeamName(teams_name)
            standing_teams.append(team_name)
        except:
            continue
    
    gameCounter = 0
    for teams in games:
        try:
            d = {}
            data = teams.find_all("td",{"":""})
            data = teams.find_all("a",{"":""})
            homeTeam = data[0].text
            AwayTeam = data[1].text
            homeTeam = getTeamName(homeTeam)
            AwayTeam = getTeamName(AwayTeam)

            d["Home Team"] = homeTeam
            d["Away Team"] = AwayTeam
            d["Home Team Rank"] = int(standing_teams.index(homeTeam)) + 1
            d["Away Team Rank"] = int(standing_teams.index(AwayTeam)) + 1
            d["Home Team Scored Goals"] = getLastScoredGoals(homeTeam,str(leagueName),int(_round)-2)
            d["Home Team Received Goals"] = getLastRecivedGoals(homeTeam,str(leagueName),int(_round)-2)
            d["Away Team Scored Goals"] = getLastScoredGoals(AwayTeam,str(leagueName),int(_round)-2)
            d["Away Team Received Goals"] = getLastRecivedGoals(AwayTeam,str(leagueName),int(_round)-2)
            
            homeTeam = getNameToFifaIndex(homeTeam)
            AwayTeam = getNameToFifaIndex(AwayTeam)
            urlHomeTeam = MAIN_URL + str(sY) + "/?name=" + homeTeam
            urlAwayTeam = MAIN_URL + str(sY) + "/?name=" + homeTeam

            dataHomeTeam = requests.get(urlHomeTeam)
            dataHomeTeamContenet = dataHomeTeam.content
            
            dataAwayTeam = requests.get(urlAwayTeam)
            dataAwayTeamContenet = dataAwayTeam.content

            try:    
                homeTeamData= BeautifulSoup(dataHomeTeamContenet,"html.parser")
                awayTeamData= BeautifulSoup(dataAwayTeamContenet,"html.parser")
            except:
                print("EXCEPTION " + homeTeam + " " + AwayTeam)
                continue

            d["Home ATT"] = homeTeamData.find("td",{"data-title":"ATT"}).text
            d["Away ATT"] = awayTeamData.find("td",{"data-title":"ATT"}).text
            d["Home DEF"] = homeTeamData.find("td",{"data-title":"DEF"}).text
            d["Away DEF"] = awayTeamData.find("td",{"data-title":"DEF"}).text
            d["Home MID"] = homeTeamData.find("td",{"data-title":"MID"}).text
            d["Away MID"] = awayTeamData.find("td",{"data-title":"MID"}).text

            # tomer
            d["Home win Odds Bet365"] = ""
            d["Draw Odds not Bet365"] = ""
            d["Away win Odds Bet365"] = ""
            
            # idan
            d["Home win Odds Winner"] = "" #_homeWinOdds
            d["Draw Odds not Winner"] = "" #_drawOdds
            d["Away win Odds Winner"] = "" #_awayWinOdds

            d["Home win Odds Winner +1"] = "" #_homeWinOdds
            d["Draw Odds not Winner +1"] = "" #_drawOdds
            d["Away win Odds Winner +1"] = "" #_awayWinOdds

            table.append(d)
            gameCounter = gameCounter + 1
        except:
            continue


    df = pandas.DataFrame(table)
    df.to_csv(leagueName + "NextRoundToPredict.csv")
    