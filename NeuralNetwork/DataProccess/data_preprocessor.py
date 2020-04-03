import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from NeuralNetwork import weight_generator as generator


def preprocess(dataset, test_and_split=False, test_size=0.2):
    labelencoder = LabelEncoder()
    league_encoder = LabelEncoder()
    features=dataset.loc[:, 'league_name':'away_odds_n']
    #features=dataset
    swap_columns(features)
    features=features.loc[:,'league_name':'away_odds_n']
    #features=features.loc[:,'home_team_name':'away_odds_n']
    targets=dataset.loc[:,'result':]
    #league_encoder.fit(features['league'])
    #features['home_team_name']=team_encoder.transform(features['home_team_name'])
    features['league_name']=league_encoder.fit_transform(features['league_name'])
    targets['result'] = labelencoder.fit_transform(targets['result'])  # X:2 ,2:1, 1:0

    print('#result label Encoding')
    le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
    print(le_name_mapping)

    print('#league label Encoding')
    le1_name_mapping = dict(zip(league_encoder.classes_, league_encoder.transform(league_encoder.classes_)))
    print(le1_name_mapping)


    target= pd.get_dummies(targets['result'], prefix="result")
    features=pd.get_dummies(features, columns=['league_name'],prefix="league")
    #features=pd.get_dummies(features, columns=['away_team_name'],prefix="away_name")


    #sc = StandardScaler()
    #features=features.loc[:,'home_team_rank':'away_odds_n']
    #features=sc.fit_transform(features)

    if test_and_split:
       x_train, x_test, y_train, y_test = train_test_split(features, target,test_size=test_size, random_state=0,shuffle=True)
       return x_train, x_test, y_train, y_test,
    else:
        return features, target
        #generator.weight_calculator(features['date'])


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
