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

#region Calculate Nodes
def CalculateNodesInFirstLayer(n, m):
    return math.sqrt(n * (m + 2)) + 2 * math.sqrt(n / (m + 2)) - 1
def CalculateNodesInSecondLayer(n, m):
    return m * math.sqrt(n / (m + 2)) - 1
#endregion

#region Calculating accuracy tools
def training_predict(model, x_test,y_test): #prediction for test phase
    #print("# Make Prediction in Training mode")
    prediction = model.predict_proba(x_test)
    y_pred = pd.DataFrame(prediction)
    columns_names = y_test.columns
    y_pred.columns=columns_names
    return calculate_accuracy(y_test,y_pred)
   # return binary_classification_with_prob_threshold(y_test,y_pred,threshold,verbose)

def binary_classification_with_prob_threshold(y_test,y_pred, threshold):
    #binary_prediction = (y_pred>threshold)
    #acc = calculate_accuracy(y_test, binary_prediction,verbose)
    cm,acc = calculate_accuracy(y_test, y_pred,)
    return cm, acc

def calculate_accuracy(y_test,y_pred):
    from sklearn.metrics import accuracy_score
    import numpy as np
    cm =get_confustion_metrix(y_test,y_pred)
    acc = accuracy_score(y_test.idxmax(axis=1),y_pred.idxmax(axis=1))
    print (cm)
    print ("Accuracy: ",acc )
    return cm,acc

def get_confustion_metrix(target_test,target_predicts):
    from sklearn.metrics import multilabel_confusion_matrix,confusion_matrix
    #target_predicts = pd.DataFrame(target_predicts)
    #columns_names = target_test.columns
    #target_predicts.columns=columns_names
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.argmax(axis=1))
    #return confusion_matrix(target_test.idxmax(axis=1), target_predicts.idxmax(axis=1))
    target_predicts=target_predicts.idxmax(axis=1)
    target_test=target_test.idxmax(axis=1)
    return confusion_matrix(target_test,target_predicts)
    #return multilabel_confusion_matrix(target_test, target_predicts)

def binarize_prediction(y_pred):
    for index, row in y_pred.iterrows():
        max = row.idxmax()
        y_pred[index][0]=0
        y_pred[index][1]=0
        y_pred[index][2]=0
        y_pred[index][max]=1

#params prediction - numpy array of the prediction
def prediction_to_excel(self, prediction,path):
    import pandas as pd
    from datetime import date
    df = pd.DataFrame(prediction)
    file = path+'prediction_'+self.model_name+"_"+str(date.today())+'.xlsx'
    df.to_excel(file, index=False)
#endregion

#region model buildings
def build_2_dec_layer():
    name='desc-2-layers'
    model = Sequential()
    model.add(Dense(input_dim=x_train.shape[1], units=math.ceil(CalculateNodesInFirstLayer(x_train.shape[1],3)), kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=math.ceil(CalculateNodesInSecondLayer(x_train.shape[1],3)), kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=3, kernel_initializer='uniform', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model,name

def build_full_3_layer():
    name='full-3-layers'
    model = Sequential()
    model.add(Dense(input_dim=x_train.shape[1], units=32, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=32, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=32, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=3, kernel_initializer='uniform', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model,name

def build_full_2_layer():
    name='full-2-layers'
    model = Sequential()
    model.add(Dense(input_dim=x_train.shape[1], units=32, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=32, kernel_initializer='uniform', activation='relu'))
    model.add(Dense(units=3, kernel_initializer='uniform', activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model,name

def build_big_dec_2_power_layers():
    name='big_dec_2_power_layers'
    model=Sequential()
    model.add(Dense(units=256,input_dim=x_train.shape[1]))
    model.add(Activation('relu'))
    model.add(Dense(units=128))
    model.add(Activation('relu'))
    model.add(Dense(units=32))
    model.add(Activation('relu'))
    model.add(Dense(units=3))
    model.add(Activation("softmax"))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 
    return model,name
#endregion

#region log
def makeLog(filename,df, conf_metrix, acc):
    import numpy as np
    with open('{}.txt'.format(filename), 'w+') as f:
        f.write(np.array2string(conf_metrix, separator=', '))
        f.write('\n'+str(df.groupby('result').size())+'\n')
        f.write('accuracy: {}'.format(acc))
        f.close()

#endregion

def list_to_csv(list):
    import csv
    with open('accuracy_list.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list)

#region data
rp= Repository()
df=rp.main_table.select_all(as_dataframe=True)
#df=rp.main_table.select_by_league_name_last_seasons(league='Serie')
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
x=sc.fit_transform(x)
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=2,shuffle=True)
#endregion


functions=  [build_2_dec_layer, build_full_2_layer, build_full_3_layer, build_big_dec_2_power_layers]
#functions=  [build_big_dec_2_power_layers]
#model,name=build_2_dec_layer()
#del,name=build_full_2_layer()
#model,name=build_full_3_layer()
#model,name=build_big_dec_2_power_layers()
for function in functions:
    model,name=function()
    model.fit(x_train, y_train, batch_size=10, epochs=100, validation_data=(x_test,y_test))
    cm,acc =training_predict(model,x_test,y_test)
    makeLog(name+' scailing',df,cm,acc)
#thresholds_acc=pd.DataFrame(columns=['threshold','accuracy'])
#threshold=0.5
#for i in range (0,50):
#    mat, acc = training_predict(model,x_test,y_test,threshold,1)
#    thresholds_acc=thresholds_acc.append({'threshold':threshold,'accuracy':acc},ignore_index=True)
#    threshold=threshold+0.01
#thresholds_acc.to_csv('{}.csv'.format(name))
