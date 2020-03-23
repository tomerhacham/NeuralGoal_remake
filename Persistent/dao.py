# Data Access Objects:
# All of these are meant to be singletons
from .dto import *
import pandas as pd

class main_table:
    def __init__(self, conn):
        self._conn = conn
        self.name = "main_table"

    def insert(self, match):
        self._conn.execute("""
               INSERT INTO main_table (match_id,leauge,date,
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
        [match.match_id,match.leauge,match.date,
        match.home_team_name,match.away_team_name,
        match.home_team_rank,match.away_team_rank,
        match.home_team_scored,match.away_team_scored,
        match.home_team_received,match.away_team_received,
        match.home_att,match.away_att,
        match.home_def,match.away_def,
        match.home_mid,match.away_mid,
        match.home_odds_n,match.draw_odds_n,match.away_odds_n])
        self._conn.commit()

    def update(self, date,home_team_name,away_team_name,result):
        c = self._conn.cursor()
        c.execute("""
              UPDATE main_table SET result=(?) WHERE date=(?) AND home_team_name=(?) AND away_team_name=(?) AND result=NULL
          """, [result,date,home_team_name,away_team_name])
        self._conn.commit()

    def select_by_league_name(self,league,as_dataframe=True):
        query="""
                SELECT * FROM main_table WHERE leauge=(?)
                """
        parameters=[league]
        if as_dataframe==True:
            return return_as_dataframe(query,self._conn,parameters)
        else:
            return return_as_tuple(query,self._conn,parameters)

    #@param: league= the league of the game
    #@param: date= from date until 'NOW'
    #@return: return the matched from @league that has took plave between @date to 'NOW'
    def select_by_date(self,league,date,as_dataframe=True):
        query="""
            SELECT * FROM main_table WHERE leauge=(?) AND date<=DATE('NOW') AND date>=(?)
            """
        parameters = [league,date]
        if as_dataframe==True:
            return return_as_dataframe(query,self._conn,parameters)
        else:
            return return_as_tuple(query,self._conn,parameters)


class upcomig_games:
    def __init__(self, conn):
        self._conn = conn
        self.name = "upcoming_games"

    def insert(self, match):
        self._conn.execute("""
               INSERT INTO upcoming_games (match_id,leauge,date,
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
        [match.match_id,match.leauge,match.date,
        match.home_team_name,match.away_team_name,
        match.home_team_rank,match.away_team_rank,
        match.home_team_scored,match.away_team_scored,
        match.home_team_received,match.away_team_received,
        match.home_att,match.away_att,
        match.home_def,match.away_def,
        match.home_mid,match.away_mid,
        match.home_odds_n,match.draw_odds_n,match.away_odds_n])
        self._conn.commit()

    def update(self, date,home_team_name,away_team_name,result):
        c = self._conn.cursor()
        c.execute("""
              UPDATE upcoming_games SET result=(?) WHERE date=(?) AND home_team_name=(?) AND away_team_name=(?) AND result=NULL
          """, [result,date,home_team_name,away_team_name])
        self._conn.commit()

    def select_by_league_name(self,league,as_dataframe=True):
        query="""
            SELECT * FROM upcoming_games WHERE leauge=(?)
            """
        parameters=[league]
        if as_dataframe==True:
            return return_as_dataframe(query,self._conn,parameters)
        else:
            return return_as_tuple(query,self._conn,parameters)

    #@param: league= the league of the game
    #@param: date= from date until 'NOW'
    #@return: return the matched from @league that has took plave between @date to 'NOW'
    def select_by_date(self,league,date,as_dataframe=True):
        query="""
            SELECT * FROM upcoming_games WHERE leauge=(?) AND date<=DATE('NOW') AND date>=(?)
            """
        parameters=[league,date]
        if as_dataframe==True:
            return return_as_dataframe(query,self._conn,parameters)
        else:
            return return_as_tuple(query,self._conn,parameters)

class odds_details:
    def __init__(self, conn):
        self._conn = conn
        self.name = "odds_details"

    def insert(self, match_odds):
        self._conn.execute("""
               INSERT INTO odds_details (match_id,home_odds,draw_odds,away_oods,home_oods_plus1,away_odds_plus1)
                                    VALUES (?,?,?,?,?,?)
                                    """,
        [match_odds.match_id,match_odds.home_odds,match_odds.draw_odds,match_odds.away_oods,match_odds.home_oods_plus1,match_odds.away_odds_plus1])
        self._conn.commit()

    def select_by_match_id(self,match_id,as_dataframe=True):
        query="""
            SELECT * FROM odds_details WHERE match_id=(?) AND
            """
        parameters=[match_id]
        if as_dataframe==True:
            return return_as_dataframe(query,self._conn,parameters)
        else:
            return return_as_tuple(query,self._conn,parameters)

def return_as_dataframe(command,connection,parameters=None):
    if parameters is None:
        return pd.read_sql_query(command,connection)
    else:
        return pd.read_sql_query(command,connection,params=parameters)

def return_as_tuple(command,connection,parameters=None):
    c = connection.cursor()
    if parameters is None:
        c.execute(command)
    else:
        c.execute(command,parameters)
    return c.fetchall()

