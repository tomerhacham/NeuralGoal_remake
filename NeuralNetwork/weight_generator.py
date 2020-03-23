import datetime


def weight_calculator(dataframe):
    weights=[]
    for row in dataframe:
        record_date = datetime.datetime.strptime(dataframe['date'], '%Y-%m-%d')
        weights.append(calculate_weight( datetime.datetime.now().year-record_date.year))
    return weights


def calculate_weight(x,test=0):
    import math
    #sigmod function
    # a - will be an parameter to shift the critical point to the relative round which the league begin in
    # b - significant multiplier - controling how many week will pass until getting full weight (working backword also in the same amount)
    b=-2.9
    a=-4.7
    if test==1:return 1
    else: return 1/(1+math.pow(math.e,a-b*x))
