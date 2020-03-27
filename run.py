from Persistent.repository import Repository
from NeuralNetwork import neuralnet,data_preprocessor,batch_size_calc
from sklearn.model_selection import train_test_split
import pandas as pd


def read_excel():
    import pandas as pd
    from datetime import datetime,timedelta
    df = pd.read_excel('C:\\Users\\Tomer Hacham\\Desktop\\italy.xlsx')
    count_row = df.shape[0]  # gives number of row count
    date = datetime.today()
    counter=0
    for i in range(count_row-1,-1,-1):
        print(df.loc[i])
        df.set_value(i,'date',value=date.strftime( '%Y-%m-%d %H:%M:%S'))
        counter=counter+1
        if counter%10 ==0:
            counter=0
            date=date-timedelta(days=10)
    df.to_excel('italy.xlsx')
    return df

repo = Repository()
#repo.create_tables()
#df = repo.main_table.select_by_league_name('spanish');
df=pd.read_csv('italy.csv')
x_train,x_test,y_train,y_test =data_preprocessor.preprocess(dataset=df,test_and_split=True)
#x_train,x_test,y_train,y_test =train_test_split(x,y,test_size=0.2)
print(x_train.shape[1]-1)
ann= neuralnet.neuralnet(input_dim=x_train.shape[1]-1)
ann.train(x_train,y_train,1000)
#ann.evaluate(x_test,y_test)

