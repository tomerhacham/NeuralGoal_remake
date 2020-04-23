from keras.callbacks import TensorBoard
from Persistent.repository import main_table
from Persistent.repository import Repository
from keras.layers.core import Dense,Activation,Dropout
from keras.models import Sequential
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler,RobustScaler,StandardScaler
from NeuralNetwork.neuralnet import neuralnet;
import math

def makeLog(filename,df, conf_metrix, acc):
    import numpy as np
    with open('{}.txt'.format(filename), 'w+') as f:
        f.write(np.array2string(conf_metrix, separator=', '))
        f.write('\n'+str(df.groupby('result').size())+'\n')
        f.write('accuracy: {}'.format(acc))
        f.close()

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
#endregion

an = neuralnet(input_dim=x.shape[1])
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=2,shuffle=True)
an.train(x_train,y_train,200)

cm,acc = training_predict(an.model,x_test,y_test)
makeLog("output",df,cm,acc)
