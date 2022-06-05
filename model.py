import pandas as pd
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt
import pmdarima as pm
import functions as f
import sys

def result(filename, goal_amount, goal_date):

    goal_amount = int(goal_amount)

    goal_date = f.parsed_date(goal_date)
    file = 'transaction_files/' + filename + '.csv'
    df = pd.read_csv(file, sep=';')

    # printing to console
    print(f'inputs: Goal date {goal_date}, goal amount {goal_amount}, file {file}, expecting results soon')

    # Drop columns that are not needed
    df.drop(columns=['account', 'other_account', 'name', 'transaction_value'], axis=1, inplace=True)
    df.rename(columns = {'balance_after_transaction':'balance'}, inplace = True)

    # Change date from str to datetime, make it the index
    df['date'] = pd.to_datetime(df['date'] , format= '%Y-%m-%d')
    df = df.set_index('date')

    # Change dates to weeks with mean balance of that week and fill empty weeks with the value of the week before (as it stayed the same)
    df = df.resample('W-MON', label='left').mean()
    df = df.fillna(method='ffill')

    current_amount = round(df['balance'].iloc[-1], 2)

    if current_amount > goal_amount:
        note = 'you already have enough money '
        predicted_amount = 0
        predicted_date = 0
        return df, note, current_amount, predicted_amount, predicted_date
    else:
        pass

    ''' ######################### SELECTING AND FITTING MODEL ######################### '''
    results = pm.auto_arima(df, seasonal=True, m=12, d=1, D=1, information_criterion='bic', trace=False, error_action='ignore', n_fits=100, stepwise=True)

    i = 1
    predictionlist = [0]

    while predictionlist[-1] < goal_amount:
        predictionlist = results.predict(n_periods = i)
        i += 1
        if i == 521:
            result = 'negative'
            break
        else:
            result = 'positive'
            pass

    print('predictions ready, adding to dataframe')

    future_dates = [df.index[-1] + DateOffset(weeks = x) for x in range(0,i)]
    future_date_df = pd.DataFrame(index = future_dates[1:],columns = df.columns)
    future_date_df["forecast"] = results.predict(n_periods = i-1,dynamic  = True )
    future_df = pd.concat([df,future_date_df])

    print('predictions added, resetting index and selecting result')

    new_df = future_df.reset_index()
    predicted_date = new_df['index'].iloc[-1]
    predicted_amount = round(new_df['forecast'].iloc[-1], 2)

    print(f'have result, result is {result} printing result')
    print(f'current_amount: {current_amount}')
    print(f'predicted_amount: {predicted_amount}')
    print(f'predicted_date: {predicted_date}')
    
    if result == 'negative':
        note = 'It will take more than 10 years, find help'
        print(f'note: {note}')
        return new_df, note, current_amount, predicted_amount, predicted_date
    else:
        if predicted_date > goal_date:
            note = 'You reach the goal after your target date'
            print(f'note: {note}')
            return new_df, note, current_amount, predicted_amount, predicted_date
        elif predicted_date == goal_date:
            note = 'You reach the goal exactly on the date'
            print(f'note: {note}')
            return new_df, note, current_amount, predicted_amount, predicted_date
        else:
            note = 'You reach the goal sooner'
            print(f'note: {note}')
            return new_df, note, current_amount, predicted_amount, predicted_date
    