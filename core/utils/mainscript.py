from core.utils.rest.dwapi import datawiz, datawiz_auth

import datetime
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format


def clean_date(x):
    d = datetime.datetime.strptime(x, '%Y-%m-%d')
    new_d = d.strftime('%d-%m-%Y')
    return new_d





def mainscript(start_date, log = 'test1@mail.com', pas = '1qaz'):

    try:
        dw = datawiz.DW(API_KEY=log, API_SECRET=pas)
        date_to = start_date
        date_from = start_date - datetime.timedelta(days=1)

        ##  TABLE BY CATEGORY

        df = dw.get_categories_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty', 'receipts_qty'],
                                    view_type='raw')

        # CHECK IS DF IS EMPTY -> NO DATA FOR CURRENT DATE
        if df.empty:
            df_cat = f'Отсутствуют данные в системе за <b>{clean_date(str(date_to))}</b>'
            positive, negative = df_cat, df_cat
            return df_cat, positive, negative
        else:

            df['date'] = df['date'].apply(lambda x: clean_date(x))

            new_df = pd.DataFrame(
                df.pivot_table(index=['date'], values=['turnover', 'qty', 'receipts_qty'], aggfunc=sum))
            new_df['Середній чек'] = new_df['turnover'] / new_df['receipts_qty']
            new_df.index.names = ['Показник']
            new_df.rename(columns={'turnover': 'Оборот', 'qty': 'Кількість товарів', 'receipts_qty': 'Кількість чеків'},
                          inplace=True)

            df_cat = new_df[['Оборот', 'Кількість товарів', 'Кількість чеків', 'Середній чек']].sort_index(
                ascending=0).T
            df_cat['Різниця в %'] = ((df_cat.loc[:, clean_date(str(date_to))] - df_cat.loc[:, clean_date(
                str(date_from))]) / df_cat.loc[:, clean_date(str(date_from))]).mul(100).round(2)
            df_cat['Різниця'] = df_cat.loc[:, clean_date(str(date_to))] - df_cat.loc[:, clean_date(str(date_from))]

            ## PRODUCTS TRANDES

            df = dw.get_products_sale(date_from=date_from, date_to=date_to, by=['turnover', 'qty'], view_type='raw')
            df['date'] = df['date'].apply(lambda x: clean_date(x))

            df_new = df.groupby(['name', 'date']).sum().reset_index()
            df_new.drop(columns=['product'], inplace=True)

            qty = pd.pivot_table(df_new, index='name', values='qty', columns='date', aggfunc=np.sum,
                                 fill_value=0).reset_index().rename_axis(None, axis=1)
            turnover = pd.pivot_table(df_new, index='name', values='turnover', columns='date', aggfunc=np.sum,
                                      fill_value=0).reset_index().rename_axis(None, axis=1)

            qty['Зміна кількості продаж'] = qty.loc[:, clean_date(str(date_to))] - qty.loc[:,
                                                                                   clean_date(str(date_from))]
            turnover['Зміна обороту'] = turnover.loc[:, clean_date(str(date_to))] - turnover.loc[:,
                                                                                    clean_date(str(date_from))]

            merged = pd.merge(qty, turnover, on='name')
            merged.rename(columns={'name': 'Назва товару'}, inplace=True)

            merged = merged[['Назва товару', 'Зміна кількості продаж', 'Зміна обороту']].sort_values('Зміна обороту',
                                                                                                     ascending=True).reset_index(
                drop=True)

            positive = merged[merged['Зміна обороту'] > 0].sort_values('Зміна обороту', ascending=False).reset_index(
                drop=True)
            negative = merged[merged['Зміна обороту'] < 0].sort_values('Зміна обороту', ascending=True).reset_index(
                drop=True)

            # CONVER DATA AND RETURN
            df_cat = df_cat.to_html(classes="table table-bordered df-tables")
            positive = positive.to_html(classes="table table-bordered df-tables")
            negative = negative.to_html(classes="table table-bordered df-tables")

            return df_cat, positive, negative

    # IF WRONG PASSWORD OR LOGIN WAS SEND
    except:
        df_cat = '<b>Был введен неправильный пароль или логин для работы с API.</b>'
        positive, negative = df_cat, df_cat
        return df_cat, positive, negative
