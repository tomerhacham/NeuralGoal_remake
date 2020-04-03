from sklearn.preprocessing import LabelEncoder

from Persistent.repository import Repository
from NeuralNetwork import neuralnet,data_preprocessor,batch_size_calc
from sklearn.model_selection import train_test_split
import pandas as pd
import keras, math,os,logging
from keras.models import Sequential
from keras.layers import Dense, Dropout
from NeuralNetwork import batch_size_calc,weight_generator
from keras.callbacks import TensorBoard
import time




# region Calculationg number of nodes in layers
def CalculateNodesInFirstLayer(n, m):
    return math.sqrt(n * (m + 2)) + 2 * math.sqrt(n / (m + 2)) - 1

def CalculateNodesInSecondLayer(n, m):
    return m * math.sqrt(n / (m + 2)) - 1

def get_weights(x):
    weights = weight_generator.weight_calculator(x['date'])
    x = x.loc[:, 'home_team_rank':'away_odds_n']
    return weights, x


df=pd.read_csv('all_leagues.csv')
null_columns=df.columns[df.isnull().any()]
print(df[df.isnull().any(axis=1)][null_columns].head())
#print(df.isnull().sum())
#labelencoder = LabelEncoder()

x,y =data_preprocessor.preprocess(dataset=df,test_and_split=False)
#y = df.loc[:, 'result':]
#x=df.loc[:,'home_att':'away_team_received']
#y['result'] = labelencoder.fit_transform(y['result'])  # X:2 ,2:1, 1:0

#print('#result label Encoding')
#le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
#print(le_name_mapping)
#y = pd.get_dummies(y['result'], prefix="result")

print(x.shape[1])
#weight,x=get_weights(x)

decending_layers=[0,1]
hidden_layers=[1,2,3]
layer_sizes=[16,32,64]
batch_sizes=[8,16,32]

#hidden_layer=2
#layer_size=16
#batch_size=8
#mod=0
#mod_name='fully'
for mod in decending_layers:
    if mod==0:
        mod_name='full'
    else:
        mod_name='dec'
    for hidden_layer in hidden_layers:
        for layer_size in layer_sizes:
            for batch_size in batch_sizes:
                NAME = "{}-nw-{}-layer-{}-size-{}-batch-{}".format(mod_name,hidden_layer,layer_size,batch_size,(int)(time.time()))
                #print(NAME)
                tensorboard = TensorBoard(log_dir='logs\\all_leagues\\{}'.format(NAME))

                model = Sequential()
                model.add(Dense(input_dim=x.shape[1], units=layer_size, kernel_initializer='uniform', activation='relu'))

                for l in range(hidden_layer):
                    if mod==1:
                        units=(int)(layer_size/math.ceil((math.pow(2,hidden_layer))))
                    else:
                        units=(int)(layer_size)
                    #print('units:',units)
                    model.add(Dense(units=units, kernel_initializer='uniform', activation='relu'))


                model.add(Dense(units=3, kernel_initializer='uniform', activation='softmax'))
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

                model.fit(x, y, batch_size=batch_size, epochs=200, validation_split=0.25,callbacks=[tensorboard])

