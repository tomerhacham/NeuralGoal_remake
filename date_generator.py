import pandas as pd
from datetime import date
from datetime import datetime, timedelta

#d = datetime.today() - timedelta(days=10)

df = pd.read_csv('italy_full.csv')
date =date.today()
counter=0

for i in range(df.shape[0] - 1, -1, -1):
    df.at[i, 'date'] = date
    counter=counter+1
    if counter%10==0:
        date=date-timedelta(days=10)
        counter=0
df.to_csv('itally_full_dates.csv')
