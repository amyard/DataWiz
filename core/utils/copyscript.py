from rest.dwapi import datawiz

import datetime
# from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import warnings

pd.options.display.float_format = '{:.2f}'.format



# log = 'test1@mail.com'
# pas = '1qaz'
#
# start_date = datetime.date(2019, 5, 2)


def main(start_date, log = 'test1@mail.com', pas = '1qaz'):

    dw = datawiz.DW(API_KEY=log, API_SECRET=pas)

    def clean_date(x):
        d = datetime.datetime.strptime(x, '%Y-%m-%d')
        new_d = d.strftime('%d-%m-%Y')
        return new_d

    date_to = start_date
    date_from = start_date - datetime.timedelta(days=1)


    ##  TABLE BY CATEGORY

    df = dw.get_categories_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty', 'receipts_qty'], view_type='raw')
    df['date'] = df['date'].apply(lambda x: clean_date(x))

    new_df = pd.DataFrame(df.pivot_table(index=['date'], values=['turnover', 'qty', 'receipts_qty'], aggfunc=sum))
    new_df['Середній чек'] = new_df['turnover'] / new_df['receipts_qty']
    new_df.index.names = ['Показник']
    new_df.rename(columns={'turnover': 'Оборот', 'qty': 'Кількість товарів', 'receipts_qty': 'Кількість чеків'}, inplace=True)

    df_cat = new_df[['Оборот', 'Кількість товарів', 'Кількість чеків', 'Середній чек']].sort_index(ascending=0).T
    df_cat['Різниця в %'] = ((df_cat.iloc[:,-2] - df_cat.iloc[:,-1]) / df_cat.iloc[:, -1]).mul(100).round(2)
    df_cat['Різниця'] = df_cat.iloc[:,-2] - df_cat.iloc[:,-1]

    df_cat = df_cat.to_html(classes="table table-bordered table-hover")


    ## PRODUCTS TRANDES

    df = dw.get_products_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty'], view_type='raw')
    df['date'] = df['date'].apply(lambda x: clean_date(x))

    df_new = df.groupby(['name', 'date']).sum().reset_index()
    df_new.drop(columns=['product'], inplace=True)


    qty = pd.pivot_table(df_new, index='name', values='qty', columns='date', aggfunc=np.sum, fill_value=0).reset_index().rename_axis(None, axis=1)
    turnover = pd.pivot_table(df_new, index='name', values='turnover', columns='date', aggfunc=np.sum, fill_value=0).reset_index().rename_axis(None, axis=1)

    qty['Зміна кількості продаж'] = qty.loc[:,clean_date(str(date_to))] - qty.loc[:,clean_date(str(date_from))]
    turnover['Зміна обороту'] = turnover.loc[:,clean_date(str(date_to))] - turnover.loc[:,clean_date(str(date_from))]

    merged = pd.merge(qty, turnover, on='name')
    merged.rename(columns={'name': 'Назва товару'}, inplace=True)

    merged = merged[['Назва товару', 'Зміна кількості продаж', 'Зміна обороту']].sort_values('Зміна обороту', ascending=True).reset_index(drop=True)

    positive = merged[merged['Зміна обороту'] > 0].sort_values('Зміна обороту', ascending=False).reset_index(drop=True)
    negative = merged[merged['Зміна обороту'] < 0].sort_values('Зміна обороту', ascending=True).reset_index(drop=True)

    positive = positive.to_html(classes="table table-bordered table-hover")
    negative = negative.to_html(classes="table table-bordered table-hover")

    return df_cat, positive, negative

if __name__ == '__main__':
    start_date = datetime.date(2015, 11, 18)
    main(start_date)



####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################




from core.utils.rest.dwapi import datawiz

import datetime
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format




def mainscript(start_date, log = 'test1@mail.com', pas = '1qaz'):

    dw = datawiz.DW(API_KEY=log, API_SECRET=pas)

    def clean_date(x):
        d = datetime.datetime.strptime(x, '%Y-%m-%d')
        new_d = d.strftime('%d-%m-%Y')
        return new_d

    date_to = start_date
    date_from = start_date - datetime.timedelta(days=1)


    ##  TABLE BY CATEGORY

    df = dw.get_categories_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty', 'receipts_qty'], view_type='raw')
    df['date'] = df['date'].apply(lambda x: clean_date(x))

    new_df = pd.DataFrame(df.pivot_table(index=['date'], values=['turnover', 'qty', 'receipts_qty'], aggfunc=sum))
    new_df['Середній чек'] = new_df['turnover'] / new_df['receipts_qty']
    new_df.index.names = ['Показник']
    new_df.rename(columns={'turnover': 'Оборот', 'qty': 'Кількість товарів', 'receipts_qty': 'Кількість чеків'}, inplace=True)

    df_cat = new_df[['Оборот', 'Кількість товарів', 'Кількість чеків', 'Середній чек']].sort_index(ascending=0).T
    df_cat['Різниця в %'] = ((df_cat.iloc[:,-2] - df_cat.iloc[:,-1]) / df_cat.iloc[:, -1]).mul(100).round(2)
    df_cat['Різниця'] = df_cat.iloc[:,-2] - df_cat.iloc[:,-1]

    df_cat = df_cat.to_html(classes="table table-bordered df-tables")


    ## PRODUCTS TRANDES

    df = dw.get_products_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty'], view_type='raw')
    df['date'] = df['date'].apply(lambda x: clean_date(x))

    df_new = df.groupby(['name', 'date']).sum().reset_index()
    df_new.drop(columns=['product'], inplace=True)


    qty = pd.pivot_table(df_new, index='name', values='qty', columns='date', aggfunc=np.sum, fill_value=0).reset_index().rename_axis(None, axis=1)
    turnover = pd.pivot_table(df_new, index='name', values='turnover', columns='date', aggfunc=np.sum, fill_value=0).reset_index().rename_axis(None, axis=1)

    qty['Зміна кількості продаж'] = qty.loc[:,clean_date(str(date_to))] - qty.loc[:,clean_date(str(date_from))]
    turnover['Зміна обороту'] = turnover.loc[:,clean_date(str(date_to))] - turnover.loc[:,clean_date(str(date_from))]

    merged = pd.merge(qty, turnover, on='name')
    merged.rename(columns={'name': 'Назва товару'}, inplace=True)

    merged = merged[['Назва товару', 'Зміна кількості продаж', 'Зміна обороту']].sort_values('Зміна обороту', ascending=True).reset_index(drop=True)

    positive = merged[merged['Зміна обороту'] > 0].sort_values('Зміна обороту', ascending=False).reset_index(drop=True)
    negative = merged[merged['Зміна обороту'] < 0].sort_values('Зміна обороту', ascending=True).reset_index(drop=True)

    positive = positive.to_html(classes="table table-bordered df-tables")
    negative = negative.to_html(classes="table table-bordered df-tables")

    return df_cat, positive, negative