from keras.callbacks import TensorBoard
from keras.layers.core import Dense,Activation,Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow import keras
import tensorflow as tf

df = pd.read_csv('itally_full_dates.csv')
x=df.loc[:,'date':'away_odds_n']
y = df.loc[:, 'result':]

labelencoder = LabelEncoder()
y['result'] = labelencoder.fit_transform(y['result'])  # X:2 ,2:1, 1:0
print('#result label Encoding')
le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
print(le_name_mapping)

y = pd.get_dummies(y['result'], prefix="result")

sc = StandardScaler()
x=x.loc[:,'home_team_rank':'away_odds_n']
x=sc.fit_transform(x)


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=2)

model=Sequential()
model.add(LSTM(units=x_train.shape[1],return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100,return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(3))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
NAME = "LSTM-{}".format((int)(time.time()))
# print(NAME)
tensorboard = TensorBoard(log_dir='logs\\LSTM\\{}'.format(NAME))
model.fit(x, y, batch_size=10, epochs=10, validation_data=(x_test,y_test), callbacks=[tensorboard])
score, acc = model.evaluate(x_test,y_test,verbose=0)
print('score:{}'.format(score))
print('accuracy:{}'.format(acc))


