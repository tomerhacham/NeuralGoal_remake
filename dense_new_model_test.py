from keras.callbacks import TensorBoard
from Persistent.repository import main_table
from Persistent.repository import Repository
from keras.layers.core import Dense,Activation,Dropout
from keras.models import Sequential
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler,RobustScaler,StandardScaler
import math

#region calc_nodes
def CalculateNodesInFirstLayer(n, m):
    return math.sqrt(n * (m + 2)) + 2 * math.sqrt(n / (m + 2)) - 1


def CalculateNodesInSecondLayer(n, m):
    return m * math.sqrt(n / (m + 2)) - 1
#endregion
#region Calculating accuracy tools
def training_predict(model, x_test,y_test,threshold,verbose): #prediction for test phase
    print("# Make Prediction in Training mode")
    prediction = model.predict_proba(x_test,verbose=verbose)
    y_pred = pd.DataFrame(prediction)
    columns_names = y_test.columns
    y_pred.columns=columns_names
    return binary_classification_with_prob_threshold(target_true=y_test,target_predicts=y_pred,threshold=threshold,verbose=verbose)

def binary_classification_with_prob_threshold(y_test,y_pred, threshold,verbose=1):
    binary_prediction = (y_pred>threshold)
    acc = calculate_accuracy(y_test, binary_prediction,verbose=verbose)
    return binary_prediction,acc

def calculate_accuracy(y_test,y_pred,verbose=1):
    from sklearn.metrics import accuracy_score
    if(verbose==1):
        print (get_confustion_metrix(y_test,y_pred))
        print ("Accuracy: ", accuracy_score(y_test,y_pred))
    return accuracy_score(y_test,y_pred)

def get_confustion_metrix(target_test,target_predicts):
    from sklearn.metrics import confusion_matrix
    target_predicts = pd.DataFrame(target_predicts)
    columns_names = target_test.columns
    target_predicts.columns=columns_names
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.argmax(axis=1))
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.idxmax(axis=1))
    return confusion_matrix(target_test, target_predicts)

#params prediction - numpy array of the prediction
def prediction_to_excel(self, prediction,path):
    import pandas as pd
    from datetime import date
    df = pd.DataFrame(prediction)
    file = path+'prediction_'+self.model_name+"_"+str(date.today())+'.xlsx'
    df.to_excel(file, index=False)
#endregion

rp= Repository()
df=rp.main_table.select_all(as_dataframe=True)
x=df.loc[:,'home_team_rank':'away_odds_n']
y=df.loc[:, 'result':]

labelencoder = LabelEncoder()
y['result'] = labelencoder.fit_transform(y['result'])  # X:2 ,2:1, 1:0
print('#result label Encoding')
le_name_mapping = dict(zip(labelencoder.classes_, labelencoder.transform(labelencoder.classes_)))
print(le_name_mapping)

y = pd.get_dummies(y['result'], prefix="result")

sc = MinMaxScaler()
#x=x.loc[:,'home_team_rank':'away_odds_n']
#x=sc.fit_transform(x)


x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=2,shuffle=True)

model=Sequential()
#act=PReLU()
model.add(Dense(units=256,input_dim=x_train.shape[1]))
model.add(Activation('relu'))

model.add(Dense(units=128))
model.add(Activation('relu'))

model.add(Dense(units=32))
model.add(Activation('relu'))

#model.add(Dense(units=math.ceil(CalculateNodesInFirstLayer(x_train.shape[1],3)),activation='relu'))
#model.add(Dense(units=math.ceil(CalculateNodesInSecondLayer(x_train.shape[1],3)),activation='relu'))
#model.add(Dropout(0.2))
#model.add(Dense(units=12))
#model.add(Activation('relu'))
#model.add(Dropout(0.25))

model.add(Dense(units=3))
model.add(Activation("softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
NAME = "128-{}".format((int)(time.time()))
# print(NAME)
tensorboard = TensorBoard(log_dir='logs\\acc_explor\\{}'.format(NAME))
#model.fit(x, y, batch_size=10, epochs=100, validation_split=0.2, callbacks=[tensorboard])
#model.fit(x_train, y_train, batch_size=10, epochs=100, validation_data=(x_test,y_test), callbacks=[tensorboard])
model.fit(x_train, y_train, batch_size=10, epochs=10, callbacks=[tensorboard])
#score, acc = model.evaluate(x_test,y_test,verbose=1)
#print('score:{}'.format(score))
#print('accuracy:{}'.format(acc))

print(training_predict(model=model,feature_test=x_test,target_test=y_test,threshold=0.75,verbose=1))


