# import requests
# from bs4 import BeautifulSoup
#
# def run(leagueName):
#
#     baseUrl = 'https://www.winner.co.il/mainbook/sport-%D7%9B%D7%93%D7%95%D7%A8%D7%92%D7%9C/'
#     url = ''
#     if leagueName == "Serie":
#         url = baseUrl + 'ep-איטליה/ep-איטלקית-ראשונה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "PremierLeague":
#         url = baseUrl + 'ep-אנגליה/ep-פרמייר-ליג?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Bundesliga":
#         url = baseUrl + ''
#     if leagueName == "Laliga":
#         url = baseUrl + 'ep-ספרד/ep-ספרדית-ראשונה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Ligue1":
#         url = baseUrl + 'ep-צרפת/ep-צרפתית-ראשונה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Jupiler":
#         url = baseUrl + 'ep-בלגיה/ep-בלגית-ראשונה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Eredivisie":
#         url = baseUrl + 'ep-הולנד/ep-הולנדית-שניה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Scotish":
#         url = baseUrl + 'ep-פורטוגל/ep-פורטוגלית-שניה?date=all&marketTypePeriod=1%7C100'
#     if leagueName == "Portugal":
#         url = baseUrl + 'ep-סקוטלנד/ep-סקוטית-פרמייר-ליג?date=all&marketTypePeriod=1%7C100'
#
#     table = []
#     agent = {"user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
#     #gamesOddsPerLeague = requests.get(url,headers=agent)
#     url = 'https://www.bet365.com/#/AC/B1/C1/D13/E51761579/F2/'
#     gamesOddsPerLeague = requests.get(url,headers=agent)
#     gamesPage = gamesOddsPerLeague.content
#     # .find("",{"":""})
#     urlForNextRound = BeautifulSoup(gamesPage, "html.parser")
#     #urlForNextRound = BeautifulSoup(gamesPage, "html.parser")#.find("div",{"class":"content_wrapper"})#.find("div",{"class":"mPanel"})#.find("div",{"class":"content"}).find("ul",{"id":"mainbook_event_paths"}).find("div",{"class":"market_type-content rollup-content"}).find_all("div",{"class":"rollup event_date rollup-down"})
#     for gamesDay in urlForNextRound:
#         gamesInThisDay = gamesDay.find("div",{"div":"event_path-content"}).find_all("div",{"":""})
#         for game in gamesInThisDay:
#
#             gameStats = game.find("table",{"":""}).find("tr",{"":""}).find_all("td",{"":""})
#             gameOdds = gameStats[2].find("tbody",{"":""}).find("tr",{"":""}).find_all("td",{"":""})
#             homeTeamName = gameOdds[0].find("div",{"class":"title"}).find("span",{"class":"name ellipsis outcomedescription"}).text
#             homeTeamName = gameOdds[2].find("div",{"class":"title"}).find("span",{"class":"name ellipsis outcomedescription"}).text
#
#             homeTeamOdds = gameOdds[0].find("div",{"class":"title"}).find("span",{"class":"formatted_price"}).text
#             drawOdds = gameOdds[1].find("div",{"class":"title"}).find("span",{"class":"formatted_price"}).text
#             awayTeamOdds = gameOdds[2].find("div",{"class":"title"}).find("span",{"class":"formatted_price"}).text

