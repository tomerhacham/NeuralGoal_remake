import pandas as pd
league_name=['Bundesliga','PremierLeague']
for name in league_name:
    NAME = '{}-{}-{}-Final-Stats.csv'
    #NAMEavg = 'Serie-{}-{}-Goals-AVG3.csv'
    PATH = 'C:\\Project\\NeuralGoal\\{} stats\\Final\\'
    df = pd.read_csv(PATH.format(name)+NAME.format(name,5,6))
    #avg = pd.read_csv(PATH+NAMEavg.format(5,6))
    for i in range(6,19):
        #avg=avg.loc[:,'Home Team Rank':'Away Team received Goals']
        other =pd.read_csv(PATH.format(name)+NAME.format(name,i,i+1))
        df=df.append(other=other,sort=False)
    df.to_csv('{}_full.csv'.format(name))
import pandas as pd
df = pd.read_csv('Italy_full.csv')
df1 = pd.read_csv('Bundesliga_full.csv')
df2 = pd.read_csv('PremierLeague_full.csv')
df.append(other=[df1,df2],sort=False).to_csv('all_leagues11.csv')
