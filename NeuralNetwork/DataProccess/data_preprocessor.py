import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def train_preprocess(df, test_and_split=False, test_size=0.2):
    x = df.loc[:, 'home_team_rank':'away_odds_n']
    y = df.loc[:, 'result':]
    labelencoder = LabelEncoder()
    y['result'] = labelencoder.fit_transform(y['result'])  # X:2 ,2:1, 1:0
    print('#result label Encoding')
    le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
    print(le_name_mapping)
    y = pd.get_dummies(y['result'], prefix="result")

    #region scaling
    # sc = MinMaxScaler()
    # x=x.loc[:,'home_team_rank':'away_odds_n']
    # x=sc.fit_transform(x)
    #endregion
    if test_and_split:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2, shuffle=True)
        return  x_train, x_test, y_train, y_test
    else:
        x,y

def prediction_preprocess(upcoming_df):
    return upcoming_df.loc[:, 'home_team_rank':'away_odds_n']

def swap_columns(features):
    swap_columns_content(features, 'league_name', 'home_team_name')
    swap_columns_content(features, 'home_team_name', 'away_team_name')
    swap_columns_names(features)

def swap_columns_content(df, c1, c2):
    df['temp'] = df[c1]
    df[c1] = df[c2]
    df[c2] = df['temp']
    df.drop(columns=['temp'], inplace=True)

def swap_columns_names(df):
    col_list=list(df)
    col_list[0],col_list[1]=col_list[1],col_list[0]
    col_list[1],col_list[2]=col_list[2],col_list[1]
    df.columns=col_list
