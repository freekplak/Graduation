''' ################################################ IMPORTS ################################################ '''
import pandas as pd
import random
import math
from datetime import datetime, timedelta
import dateutil.rrule as dr
import dateutil.parser as dp
import dateutil.relativedelta as drel

format = '%Y-%m-%d'

''' ################################################ LIST WITH NAMES, SHOPS AND IBANs ################################################ '''
person_names = [
    'Menno Vredenburg',
    'Dirk Baars',
    'Anne Van Slyke',
    'Wolter Doorn',
    'Petrus Vandenberg',
    'Bert Provine',
    'Annemarie Meuse',
    'Helga Mox',
    'Truus Van Dell',
    'Tineke Vliet',
    'Petunia Lis',
    'Johannes Rosenkranz',
    'Joop Redig',
    'Jos Stammen',
    'Bram Spoon',
    'Walter Bolmer',
    'Hanneke Leber',
    'Liesbeth Van Schaik',
    'Gesina De Graaf',
    'Mariska Vandersloot',
    'Jacoba Lindert',
    'Maurits Busker',
    'Quirijn Stam',
    'Remco Kooy',
    'Wilco Wassenaar',
    'Charlotte Venner',
    'Petronella Sieren',
    'Elke Slager',
    'Ilse Sant'
]
IBANs = [
    'NL66RABO3526558027',
    'NL98INGB1415694826', 
    'NL17RABO4115845937', 
    'NL57RABO4787393871', 
    'NL69RABO9966705163', 
    'NL67ABNA1965265332', 
    'NL32ABNA4438120233', 
    'NL33INGB8694892022', 
    'NL13ABNA4388522244', 
    'NL98ABNA5831335380', 
    'NL50INGB7082086296', 
    'NL08RABO7568468658', 
    'NL49INGB5406040774', 
    'NL38INGB3675462129', 
    'NL24INGB5924436675', 
    'NL67ABNA1070230618',
    'NL18INGB9657789273',
    'NL05RABO8181091612',
    'NL60RABO7711638558', 
    'NL92ABNA6770096250', 
    'NL36INGB9481673421', 
    'NL18INGB8743112544', 
    'NL03ABNA5732787127', 
    'NL09RABO9999810888', 
    'NL87INGB9688157082',
    'NL68ABNA9548056305', 
    'NL13ABNA7434587830', 
    'NL20RABO7577249270', 
    'NL07INGB9788055427', 
    'NL80RABO3777087823', 
    'NL85INGB4031638493', 
    'NL07ABNA8849764685', 
    'NL95INGB4636681924',
    'NL84ABNA1158470533'
]

''' ################################################ FUNCTIONS ################################################ '''
def parsed_date(date_string):
    d=dp.parse(date_string)

    return d
    
def random_date(start_date, end_date):
    res_dates = [start_date]
  
    while start_date != end_date:
        start_date += timedelta(days=1)
        res_dates.append(start_date)

    return random.choice(res_dates)

def random_iban():
    if not IBANs:
        IBAN = 'NO IBAN'
    else:
        random.shuffle(IBANs)
        IBAN = IBANs.pop()
    
    return IBAN

def random_name():
    if not person_names:
        name = 'NO NAME'
    else:
        random.shuffle(person_names)
        name = person_names.pop()
    
    return name

def add_allowance(df, account, allowance, parent, parent_account, allowance_amount, start_date):
    if allowance == 'weekly':
        # weekly on sunday's
        rr = dr.rrule(dr.WEEKLY, byweekday=drel.SU(1), dtstart=start_date, count=104)
        rr = [d.strftime(format) for d in rr]
    elif allowance == 'bi-weekly':
        # bi-weekly on sunday's
        rr = dr.rrule(dr.WEEKLY,byweekday=drel.SU(1),dtstart=start_date, count=104)
        rr = [d.strftime(format) for d in rr[::2]]
    else:
        # Monthly on the 25th
        rr = dr.rrule(dr.MONTHLY,bymonthday=25, dtstart=start_date, count=24)
        rr = [d.strftime(format) for d in rr]
    
    for date in rr:
        row = {'date': date, 'account': account, 'other_account': parent_account, 'name': parent, 'balance_after_transaction': 0, 'transaction_value': float(allowance_amount)}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

    return df

def add_chores(df, account, parent, parent_account, chore_based_income, start_date):
    month_list = dr.rrule(dr.MONTHLY, bymonthday=1, dtstart=start_date, count=25)
    month_list = [d.strftime(format) for d in month_list]

    for i in range(len(month_list)-1):
        for x in range(chore_based_income):
            sdate = parsed_date(month_list[i])
            edate = parsed_date(month_list[i+1])
            date = random_date(sdate, edate)
            amount = round(random.uniform(1.00, 5.00), 0)
            row = {'date': date, 'account': account, 'other_account': parent_account, 'name': parent, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
    
    return df

def list_of_yearly_dates(the_date, counts, sdate, edate):
    result_list = dr.rrule(dr.YEARLY, dtstart=the_date, count=counts)
    result_list = [d.strftime(format) for d in result_list]
    result_list = [date for date in result_list if datetime.strptime(date, format) > sdate and datetime.strptime(date, format) < edate]

    return result_list

def add_reportcardmoney(df, report_cards, account, parent, parent_account, start_date, end_date):
    start_year = start_date.strftime('%Y')

    summer_date = random_date(parsed_date('2022-06-01'), parsed_date('2022-06-30'))
    summer_day = summer_date.strftime('%d')
    summer_month = summer_date.strftime('%m')
    summer_report = parsed_date(start_year + '-' + summer_month + '-' + summer_day)
    summer_report_list = list_of_yearly_dates(summer_report, 3, start_date, end_date)

    april_date = random_date(parsed_date('2022-04-01'), parsed_date('2022-04-30'))
    april_day = april_date.strftime('%d')
    april_month = april_date.strftime('%m')
    april_report = parsed_date(start_year + '-' + april_month + '-' + april_day)
    april_report_list = list_of_yearly_dates(april_report, 3, start_date, end_date)

    fall_date = random_date(parsed_date('2022-09-25'), parsed_date('2022-10-14'))
    fall_day = fall_date.strftime('%d')
    fall_month = fall_date.strftime('%m')
    fall_report = parsed_date(start_year + '-' + fall_month + '-' + fall_day)
    fall_report_list = list_of_yearly_dates(fall_report, 3, start_date, end_date)
    
    if report_cards == 1:
        report_date_list = summer_report_list
        
    elif report_cards == 2:
        report_date_list = summer_report_list + april_report_list

    else:
        report_date_list = summer_report_list + april_report_list + fall_report_list
    
    for date in report_date_list:
        amount = round(random.uniform(10.00, 25.00), 0)
        amount = float(math.ceil(amount / 5) * 5)
        row = {'date': date, 'account': account, 'other_account': parent_account, 'name': parent, 'balance_after_transaction': 0, 'transaction_value': amount}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

        a = random.randint(0,2)
        for i in range(a):
            amount = round(random.uniform(10.00, 25.00), 0)
            amount = float(math.floor(amount / 5) * 5)
            row = {'date': date, 'account': account, 'other_account': random_iban(), 'name': random_name(), 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)

    return df

def birthday_money(df, birth_day, account, parent, parent_account, start_date, end_date):
    birthdays = list_of_yearly_dates(birth_day, 100, start_date, end_date)

    for date in birthdays:
        amount = round(random.uniform(20.00, 50.00), 0)
        amount = float(math.ceil(amount / 5) * 5)
        row = {'date': date, 'account': account, 'other_account': parent_account, 'name': parent, 'balance_after_transaction': 0, 'transaction_value': amount}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)

        a = random.randint(1,5)
        for i in range(a):
            amount = round(random.uniform(10.00, 50.00), 0)
            amount = float(math.floor(amount / 5) * 5)
            row = {'date': date, 'account': account, 'other_account': random_iban(), 'name': random_name(), 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
    
    return df

def business_list(shop_list):
    new_list = []

    for shop in shop_list:
        new_dict = {'shop': shop, 'IBAN': random_iban()}
        new_list.append(new_dict)
    
    return new_list

def add_spendings(df, iterations, account, start_date, end_date, shop_list_1, shop_list_2, shop_list_3, shop_list_4, shop_list_5, shop_list_6):
    for i in range(iterations):
        number = random.randint(1, 85)
        date = random_date(start_date, end_date).strftime(format)

        if number in range (51):
            shop_dict = random.choice(shop_list_1)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = round(random.uniform(-0.50, -3.00), 2)
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # shop_list_1 = ['AH 1208 Utrecht', 'DIRK VDBROEK FIL3489', 'Jumbo Leidsche Rijn'] # 0.5 tot 3 euro
        elif number in range (51, 75):
            shop_dict = random.choice(shop_list_2)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = round(random.uniform(-1.00, -4.00), 2)
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # shop_list_2 = ['Bakkerij t Stoepje', 'Jamin', 'Snackbar Pieters'] # 1 tot 4 euro
        elif number in range (75, 81):
            shop_dict = random.choice(shop_list_3)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = round(random.uniform(-4.00, -12.00), 2)
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # shop_list_3 = ['Intertoys', 'ETOS 3297', 'Intratuin Utrecht'] # 4 tot 12 euro
        elif number == 81 or 82:
            shop_dict = random.choice(shop_list_4)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = round(random.uniform(-5.00, -35.00), 2)
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # shop_list_4 = ['H&M', 'Zara', 'Game Mania', 'Mediamarkt', 'de Bijenkorf', 'The Sting089'] # 5 tot 35 euro 
        elif number == 83 or 84:
            shop_dict = random.choice(shop_list_5)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = round(random.uniform(-9.00, -15.00), 2)
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # 'Pathe Utrecht', 9 - 15
        else:
            shop_dict = random.choice(shop_list_6)
            shop = shop_dict['shop']
            IBAN = shop_dict['IBAN']
            amount = random.choice([-10.00, -25.00, -39.99, -49.99, -59.99])
            row = {'date': date, 'account': account, 'other_account': IBAN, 'name': shop, 'balance_after_transaction': 0, 'transaction_value': amount}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            # 'Playstation store', 10, 25, 40, 50, 60
    return df