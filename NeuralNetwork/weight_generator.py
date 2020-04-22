import datetime
import numpy as np


#calculate the delta in days between current system thime to the match date and return the diff in years
def weight_calculator(dataframe):
    weights=[]
    for row in dataframe:
        record_date = datetime.datetime.strptime(row, '%Y-%m-%d %H:%M:%S')
        #print('delta: {} '.format((datetime.datetime.now()-record_date).days/365))
        weights.append(calculate_weight((datetime.datetime.now()-record_date).days/365))
    return np.array(weights)


def calculate_weight(x,test=0):
    import math
    #sigmod function
    # a - will be an parameter to shift the critical point to the relative round which the league begin in
    # b - significant multiplier - controling how many week will pass until getting full weight (working backword also in the same amount)
    #x - diff in years from current time to the date the match took place
    b=-2.4
    a=-3.6
    if test==1 or x<0.2:return 1
    else: return 1/(1+math.pow(math.e,a-b*x))
