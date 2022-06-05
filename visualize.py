from dash import dash, dcc, html, Input, Output, State
from datetime import datetime
import plotly.express as px
import pandas as pd
import model as predict

filename = 'Child 5'
goal_amount = 1200
goal_date = '2023-09-01'
current_date = datetime.now().date()


file = 'transaction_files/' + filename + '.csv'

df = pd.read_csv(file, sep=';')

df.drop(columns=['account', 'other_account', 'name', 'transaction_value'], axis=1, inplace=True)
df.rename(columns = {'balance_after_transaction':'balance'}, inplace = True)

# Change date from str to datetime, make it the index
df['date'] = pd.to_datetime(df['date'] , format= '%Y-%m-%d')
df = df.set_index('date')

# Change dates to weeks with mean balance of that week and fill empty weeks with the value of the week before (as it stayed the same)
df = df.resample('W-MON', label='left').mean()
df = df.fillna(method='ffill')
df = df.reset_index()

# Determine the current amount
current_amount = round(df['balance'].iloc[-1], 2)

app = dash.Dash()

#layout of application
app.layout = html.Div(className='container', children=[
    #Div for App
    html.Div(className='Saving goal', children=[
        html.H2(children = "Are you going to reach your goal?"),
        html.P(children = "Provide a goal date yyyy-mm-dd, goal amount (numbers only) and the Child you want the results from"),
        dcc.Input(id='Date', value=str(current_date), type='text'),
        dcc.Input(id='Goal_amount', value=str(current_amount), type='number'),
        dcc.Input(id='Child', value='Child 5', type='text'),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='result_message', children=[
            # html.P(className='big', children = "Current amount " + str(current_amount))
        ]),
        html.Div(id='Here_the_result', children =[]),
    ])
])

# Callback when values are submitted
@app.callback(
    [Output(component_id='Here_the_result', component_property='children')],
    [Input('submit-val', 'n_clicks')],
    [State('Date', 'value'), State('Goal_amount', 'value'), State('Child', 'value')]
)
# function that updates the results, as input it takes the click on the submit button, the target date, target amount and user (child)
def update_children(n_clicks, Date, Goal_amount, Child):
    n_clicks = int(n_clicks)
    if n_clicks is None:
        return dash.no_update
    else:
        # goal amount from str to float
        Goal_amount = float(Goal_amount)

        # The model is called (was inported as predict, containing only one function: result, as input it takes the user (child), goal amount and target date
        # It returns the new dataframe, a note (the feedback message), the current amount, predicted amount and predicted date
        df,note,current_amount,predicted_amount,predicted_date = predict.result(Child, Goal_amount, Date)

        # prints result to terminal
        print(f'received results')
        print(f'Note: {note}')
        print(f'current_amount: {current_amount}')
        print(f'predicted_amount: {predicted_amount}')
        print(f'predicted_date: {predicted_date}')

        # Save results as a string sentence to communicate to the front end.
        result = [f'Received results: {note}, predicted amount: {str(predicted_amount)}, predicted date {str(predicted_date)}']

        # Returns the result to the app, by printing this in the Div
        return result

if __name__ == '__main__':
    app.run_server(debug=True)