import keras, math,os,logging
from keras.models import Sequential
from keras.layers import Dense, Dropout
from NeuralNetwork import batch_size_calc,weight_generator
from keras.callbacks import TensorBoard
import time

LOGGIN_NAME ="ann-{}".format((int)(time.time()))
tensorboard = TensorBoard(log_dir='logs\\{}'.format(LOGGIN_NAME))

class neuralnet():
    model = None
    cls=None
    input=0
    output=0
    batch_size=0
    nodesinfirstlayer=None
    nodesinsecondlayer=None
    best_parameters=None
    best_accuracy=None

    def __init__(self,input_dim,tf_verbose=3):
        self.input=input_dim
        self.output=int(3)
        self.nodesinfirstlayer = math.ceil(self.CalculateNodesInFirstLayer(self.input,self.output))
        self.nodesinsecondlayer = math.ceil(self.CalculateNodesInSecondLayer(self.input,self.output))
        self.build()
        set_tf_loglevel(tf_verbose)

    #region Calculationg number of nodes in layers
    def CalculateNodesInFirstLayer(self, n,m):
        return math.sqrt(n*(m+2)) + 2*math.sqrt(n/(m+2))-1

    def CalculateNodesInSecondLayer(self, n,m):
        return m*math.sqrt(n/(m+2))-1

    #endregion
    #region Model Essence
    def build(self, optimizer='adam'):
        self.model=Sequential()
        self.model.add(Dense(units=256,input_dim=x_train.shape[1]))
        self.model.add(Activation('relu'))
        self.model.add(Dense(units=128))
        self.model.add(Activation('relu'))
        self.model.add(Dense(units=32))
        self.model.add(Activation('relu'))
        self.model.add(Dense(units=3))
        self.model.add(Activation("softmax"))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 
        return self.model

    def train(self,x,y,_epochs):
        self.model.fit(x,y, batch_size=10, epochs=_epochs)
     
    def evaluate(self,x_test,y_test):
        weights, x_test = self.get_weights(x_test)
        # Evaluate the model on the test data using `evaluate`
        print('# Evaluate on test data')
        #score, acc = self.model.evaluate(x_test, y_test,batch_size=self.batch_size,sample_weight=weights)
        score, acc = self.model.evaluate(x_test, y_test,batch_size=self.batch_size)
        print('Test score:', score)
        print('Test accuracy:', acc)

    def get_weights(self, x):
        weights = weight_generator.weight_calculator(x['date'])
        x = x.loc[:, 'home_team_rank':'away_odds_n']
        return weights, x

    def predict(self,x,verbose=0): #return array of prediction per the features
        if(verbose<1):
            print ("# Generate Prediction")
        return self.model.predict_proba(x)

    def training_predict(self,feature_test,target_true,threshold,verbose): #prediction for test phase
        print("# Make Prediction in Training mode")
        prediction = self.predict(feature_test,verbose=1)
        return self.binary_classification_with_prob_threshold(target_true=target_true,target_predicts=prediction,threshold=threshold,verbose=0)


    #endregion
    #region Calculating accuracy tools
    def binary_classification_with_prob_threshold(self, target_true,target_predicts, threshold,verbose=1):
        binary_prediction = (target_predicts>threshold)
        acc = self.calculate_accuracy(target_true, binary_prediction,verbose=verbose)
        return binary_prediction,acc

    def calculate_accuracy(self,target_true,target_predicts,verbose=1):
        from sklearn.metrics import accuracy_score
        if(verbose==1):
            print (self.get_confustion_metrix(target_true,target_predicts))
            print ("Accuracy: ", accuracy_score(target_true,target_predicts))
        return accuracy_score(target_true,target_predicts)

    def get_confustion_metrix(self,target_test,target_predicts):
        from sklearn.metrics import confusion_matrix
        return confusion_matrix(target_test.argmax(axis=1), target_predicts.argmax(axis=1))

    #params prediction - numpy array of the prediction
    def prediction_to_excel(self, prediction,path):
        import pandas as pd
        from datetime import date
        df = pd.DataFrame(prediction)
        file = path+'prediction_'+self.model_name+"_"+str(date.today())+'.xlsx'
        df.to_excel(file, index=False)
    #endregion

def set_tf_loglevel(level):
    if level >= logging.FATAL:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    if level >= logging.ERROR:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    if level >= logging.WARNING:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
    else:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    logging.getLogger('tensorflow').setLevel(level)

def print_plot(history):
    import matplotlib.pyplot as plt
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()