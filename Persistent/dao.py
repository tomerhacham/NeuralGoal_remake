# Data Access Objects:
# All of these are meant to be singletons
from .dto import *


class main_table:
    def __init__(self, conn):
        self._conn = conn
        self.name = "main_table"

    def insert(self, match):
        self._conn.execute("""
               INSERT INTO main_table (league,date,round,
                                    home_team_name,away_team_name,
                                    home_team_rank,away_team_rank,
                                    home_team_scored,away_team_scored,
                                    home_team_received,away_team_received,
                                    home_att,away_att,
                                    home_def,away_def,
                                    home_mid,away_mid,
                                    home_odds_n,draw_odds_n,away_odds_n,result)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """,
                           [match.league, match.date, match.round,
                            match.home_team_name, match.away_team_name,
                            match.home_team_rank, match.away_team_rank,
                            match.home_team_scored, match.away_team_scored,
                            match.home_team_received, match.away_team_received,
                            match.home_att, match.away_att,
                            match.home_def, match.away_def,
                            match.home_mid, match.away_mid,
                            match.home_odds_n, match.draw_odds_n, match.away_odds_n,match.result])
        self._conn.commit()

    def update(self, date, home_team_name, away_team_name, result):
        c = self._conn.cursor()
        c.execute("""
              UPDATE main_table SET result=(?) WHERE date=(?) AND home_team_name=(?) AND away_team_name=(?) AND result=NULL
          """, [result, date, home_team_name, away_team_name])
        self._conn.commit()

    # def find(self, employee_id):
    #    c = self._conn.cursor()
    #   c.execute("""
    #      SELECT * FROM Employees WHERE id = ?
    # """, [employee_id])
    # return Employee(*c.fetchone())

    def select_by_league_name(self, league):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM main_table WHERE leauge=(?)
            """, [league])
        # TODO: make a list of the DTO object
        return c.fetchall()

    # @param: league= the league of the game
    # @param: date= from date until 'NOW'
    # @return: return the matched from @league that has took plave between @date to 'NOW'
    def select_by_date(self, league, date):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM main_table WHERE leauge=(?) AND date<=DATE('NOW') AND date>=(?)
            """, [league, date])
        # TODO: make a list of the DTO object
        return c.fetchall()


class upcoming_games:
    def __init__(self, conn):
        self._conn = conn
        self.name = "upcoming_games"

    def insert(self, match):
        self._conn.execute("""
               INSERT INTO upcoming_games (league,date,round,
                                    home_team_name,away_team_name,
                                    home_team_rank,away_team_rank,
                                    home_team_scored,away_team_scored,
                                    home_team_received,away_team_received,
                                    home_att,away_att,
                                    home_def,away_def,
                                    home_mid,away_mid,
                                    home_odds_n,draw_odds_n,away_odds_n)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """,
                           [match.league, match.date, match.round,
                            match.home_team_name, match.away_team_name,
                            match.home_team_rank, match.away_team_rank,
                            match.home_team_scored, match.away_team_scored,
                            match.home_team_received, match.away_team_received,
                            match.home_att, match.away_att,
                            match.home_def, match.away_def,
                            match.home_mid, match.away_mid,
                            match.home_odds_n, match.draw_odds_n, match.away_odds_n])
        self._conn.commit()

    def update(self, date, home_team_name, away_team_name, result):
        c = self._conn.cursor()
        c.execute("""
              UPDATE upcoming_games SET result=(?) WHERE date=(?) AND home_team_name=(?) AND away_team_name=(?) AND result=NULL
          """, [result, date, home_team_name, away_team_name])
        self._conn.commit()

    # def find(self, employee_id):
    #    c = self._conn.cursor()
    #   c.execute("""
    #      SELECT * FROM Employees WHERE id = ?
    # """, [employee_id])
    # return Employee(*c.fetchone())

    def select_by_league_name(self, league):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM upcoming_games WHERE leauge=(?)
            """, [league])
        # TODO: make a list of the DTO object
        return c.fetchall()

    # @param: league= the league of the game
    # @param: date= from date until 'NOW'
    # @return: return the matched from @league that has took plave between @date to 'NOW'
    def select_by_date(self, league, date):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM upcoming_games WHERE leauge=(?) AND date<=DATE('NOW') AND date>=(?)
            """, [league, date])
        # TODO: make a list of the DTO object
        return c.fetchall()


class odds_details:
    def __init__(self, conn):
        self._conn = conn
        self.name = "odds_details"

    def insert(self, match_odds):
        self._conn.execute("""
               INSERT INTO odds_details (home_odds,draw_odds,away_oods,home_oods_plus1,away_odds_plus1)
                                    VALUES (?,?,?,?,?)
                                    """,
                           [match_odds.match_id, match_odds.home_odds, match_odds.draw_odds, match_odds.away_oods,
                            match_odds.home_oods_plus1, match_odds.away_odds_plus1])
        self._conn.commit()

    def select_by_match_id(self, match_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM odds_details WHERE match_id=(?) AND
            """, [match_id])
        # TODO: make a list of the DTO object
        return c.fetchall()
