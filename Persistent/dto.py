# Data Transfer Objects:
class match:
    def __init__(self, league, date, round,
                 home_team_name, away_team_name,
                 home_team_rank, away_team_rank,
                 home_team_scored, away_team_scored,
                 home_team_received, away_team_received,
                 home_att, away_att,
                 home_def, away_def,
                 home_mid, away_mid,
                 home_odds_n, draw_odds_n, away_odds_n,
                 result,home_odds_nn,draw_odds_nn,away_odds_nn):
        self.league = league
        self.date = date
        self.round = round
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.home_team_rank = home_team_rank
        self.away_team_rank = away_team_rank
        self.home_team_scored = home_team_scored
        self.away_team_scored = away_team_scored
        self.home_team_received = home_team_received
        self.away_team_received = away_team_received
        self.home_att = home_att
        self.away_att = away_att
        self.home_def = home_def
        self.away_def = away_def
        self.home_mid = home_mid
        self.away_mid = away_mid
        self.home_odds_n = home_odds_n
        self.draw_odds_n = draw_odds_n
        self.away_odds_n = away_odds_n
        self.result = result
        self.home_odds_nn = home_odds_nn
        self.draw_odds_nn = draw_odds_nn
        self.away_odds_nn = away_odds_nn


class match_odds:
    def __init__(self, home_odds, draw_odds, away_odds, home_odds_plus1, away_odds_plus1):
        self.home_odds = home_odds
        self.draw_odds = draw_odds
        self.away_odds = away_odds
        self.home_odds_plus1 = home_odds_plus1
        self.away_odds_plus1 = away_odds_plus1
