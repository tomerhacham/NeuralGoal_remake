#The Repository
from .dao import *
import sqlite3
import os
import atexit

class Repository():
    #Fields
    conn = None
    main_table= None
    upcoming_games = None
    odds_details=None;
    
    def __init__(self):

        if not os.path.isfile('NeuralGoal.db'):
            db = open('NeuralGoal.db', "w")
            db.close()
            print("Creating Database")
        self.conn = sqlite3.connect('NeuralGoal.db')

        self.main_table = main_table(self.conn)
        self.upcoming_games = upcoming_games(self.conn)
        self.odds_details = odds_details(self.conn)


    def _close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE main_table (
            league             VARCHAR(100)     NOT NULL   ,
            date               DATE      NOT NULL   ,
            round              INTEGER      NOT NULL   ,
            home_team_name      VARCHAR(100)    NOT NULL   ,
            away_team_name      VARCHAR(100)   NOT NULL    ,
            home_team_rank      INTEGER   NOT NULL   ,
            away_team_rank      INTEGER  NOT NULL    ,
            home_team_scored  FLOAT   NOT NULL   ,
            away_team_scored  FLOAT   NOT NULL   ,
            home_team_received  FLOAT   NOT NULL   ,
            away_team_received  FLOAT  NOT NULL    ,
            home_att  INTEGER   NOT NULL   ,
            away_att  INTEGER  NOT NULL    ,
            home_def  INTEGER    NOT NULL  ,
            away_def  INTEGER   NOT NULL   ,
            home_mid  INTEGER  NOT NULL    ,
            away_mid  INTEGER  NOT NULL    ,
            home_odds_n  FLOAT  NOT NULL    ,
            draw_odds_n  FLOAT   NOT NULL   ,
            away_odds_n  FLOAT   NOT NULL   ,
            result  CHAR  NOT NULL    
        );
 
        CREATE TABLE upcoming_games (
            league             VARCHAR(100)          NOT NULL,
            date               DATE        NOT NULL,
            round              INTEGER        NOT NULL,
            home_team_name      VARCHAR(100)      NOT NULL,
            away_team_name      VARCHAR(100)      NOT NULL,
            home_team_rank      INTEGER     NOT NULL,
            away_team_rank      INTEGER     NOT NULL,
            home_team_scored  FLOAT     NOT NULL,
            away_team_scored  FLOAT     NOT NULL,
            home_team_received  FLOAT     NOT NULL,
            away_team_received  FLOAT     NOT NULL,
            home_att  INTEGER     NOT NULL,
            away_att  INTEGER     NOT NULL,
            home_def  INTEGER     NOT NULL,
            away_def  INTEGER     NOT NULL,
            home_mid  INTEGER     NOT NULL,
            away_mid  INTEGER     NOT NULL,
            home_odds_n  FLOAT     NOT NULL,
            draw_odds_n  FLOAT     NOT NULL,
            away_odds_n  FLOAT     NOT NULL
        );
 
        CREATE TABLE odds_details (
            home_odds  FLOAT     NOT NULL,
            draw_odds  FLOAT     NOT NULL,
            away_odds  FLOAT     NOT NULL,
            home_odds_plus1  FLOAT    ,
            away_odds_plus1 FLOAT     

        );
    """)
    #print("creating tabels")
