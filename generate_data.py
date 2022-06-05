''' ################################################ IMPORTS ################################################ '''
import pandas as pd
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import functions as f

''' ################################################ DEFINE FILENAME ################################################ '''
filename = 'Child 6'

''' ################################################ DEFINING (RANDOM) VALUES NEEDED FOR INPUT ################################################ '''
shop_list_1 = ['AH 1208 Utrecht', 'DIRK VDBROEK FIL3489', 'Jumbo Leidsche Rijn'] # 0.5 tot 3 euro
shop_list_2 = ['Bakkerij t Stoepje', 'Jamin', 'Snackbar Pieters'] # 1 tot 4 euro
shop_list_3 = ['Intertoys', 'ETOS 3297', 'Intratuin Utrecht'] # 4 tot 12 euro
shop_list_4 = ['H&M', 'Zara', 'Game Mania', 'Mediamarkt', 'de Bijenkorf', 'The Sting089'] # 5 tot 35 euro 
shop_list_5 = ['Pathe Utrecht'] # 9 tot 15 euro
shop_list_6 = ['Playstation store'] # 10, 25, 40, 50 of 60 euro

df = pd.DataFrame(columns=['date', 'account', 'other_account', 'name', 'balance_after_transaction', 'transaction_value'])
account = f.random_iban()
parent = f.random_name()
parent_account = f.random_iban()
format = '%Y-%m-%d'
end_date = datetime.now().date()
start_date = end_date - relativedelta(years=2) #year-month-day
end_date = end_date - relativedelta(days=1)
start_date = f.parsed_date(str(start_date))
end_date = f.parsed_date(str(end_date))
allowance = random.choice(['weekly', 'bi-weekly', 'monthly']) # none, weekly, bi-weekly, monthly
if allowance == 'weekly':
    allowance_amount = random.randint(2, 4)
elif allowance == 'bi-weekly':
    allowance_amount = random.randint(4, 8)
else:
    allowance = 'monthly'
    allowance_amount = random.randint(8, 16)
    allowance_day = random.randint(1, 28)
birth_date = f.random_date(start_date, end_date)
if random.randint(0, 1) == 1:
    chore_based_income = random.randint(1, 3) # how often does the child get paid for chores per month
else:
    chore_based_income = 0
report_cards = random.randint(0, 3) # how often does the child get a report card
spending = random.choice(['low', 'medium', 'high']) # low, high or medium
shop_list_1 = f.business_list(shop_list_1)
shop_list_2 = f.business_list(shop_list_2)
shop_list_3 = f.business_list(shop_list_3)
shop_list_4 = f.business_list(shop_list_4)
shop_list_5 = f.business_list(shop_list_5)
shop_list_6 = f.business_list(shop_list_6)
    
''' ################################################ ADDING ALLOWANCE ################################################ '''
if allowance != 'none':
    df = f.add_allowance(df, account, allowance, parent, parent_account, allowance_amount, start_date)
else:
    pass

''' ################################################ ADDING CHORES ################################################ '''
if chore_based_income > 0:
    df = f.add_chores(df, account, parent, parent_account, chore_based_income, start_date)
else:
    pass

''' ################################################ ADDING BIRTHDAY GIFTS ################################################ '''
df = f.birthday_money(df, birth_date, account, parent, parent_account, start_date, end_date)

''' ################################################ ADDING BIRTHDAY GIFTS ################################################ '''
df = f.add_reportcardmoney(df, report_cards, account, parent, parent_account, start_date, end_date)

''' ################################################ ADDING SPENDING ################################################ '''
if spending == 'low':
    df = f.add_spendings(df, 86, account, start_date, end_date, shop_list_1, shop_list_2, shop_list_3, shop_list_4, shop_list_5, shop_list_6)
elif spending == 'medium':
    df = f.add_spendings(df, 110, account, start_date, end_date, shop_list_1, shop_list_2, shop_list_3, shop_list_4, shop_list_5, shop_list_6)
else:
    df = f.add_spendings(df, 133, account, start_date, end_date, shop_list_1, shop_list_2, shop_list_3, shop_list_4, shop_list_5, shop_list_6)

''' ################################################ SORTING DATAFRAME BY DATE ################################################ '''
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')
df = df.reset_index(drop=True)

''' ################################################ ADDING BALANCE AFTER TRANSACTION ################################################ '''
for index, row in df.iterrows():
    if index != 0:
        df.loc[index, 'balance_after_transaction'] = df.loc[index-1, 'balance_after_transaction'] + df.loc[index, 'transaction_value']
    else:
        df.loc[index, 'balance_after_transaction'] = round(random.uniform(40.00, 70.00), 2) + df.loc[index, 'transaction_value']

''' ################################################ EXPORTING FILE ################################################ '''
filepath = 'transaction_files/' + filename + '.csv'

df.to_csv (filepath, sep=';', index = False, header=True)

''' ################################################ PRINTING RESULTS ################################################ '''
print(f'DataFrame exported, file at: {filepath}')
print(f'DataFrame shape: {df.shape}')