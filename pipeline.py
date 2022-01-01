import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.2f}'.format
from bs4_scrape import Scrape

def df_pipe(game_dict):
    """
    Performs dataframe cleaning and processing from bs4_scrape so the final dataframe is ready for processing in ML
    """
    # game_dict = Scrape.scrape(game_title_input)
    df = pd.DataFrame.from_dict(game_dict, orient='index').transpose()
    df.dropna(subset=['game_regular_price','game_date','game_actual_price','sale_duration'], inplace=True)
    df[['game_title','game_release_date']] = df[['game_title','game_release_date']].fillna(method='ffill')
    # Remove sale_duration from game_date column
    df['game_date'] = df.apply(lambda row: row['game_date'].replace(str(row['sale_duration']),''), axis=1)
    # Change to appropriate data types
    df['game_title'] = df.game_title.astype('str')
    df['game_date'] = pd.to_datetime(df['game_date'])
    df['game_store_name'] = df.game_store_name.astype('str')
    df['game_regular_price'] = df.game_regular_price.str.replace('$','').astype(float)
    df['game_actual_price'] = df.game_actual_price.str.replace('$','').astype(float)
    df['game_release_date'] = pd.to_datetime(df.game_release_date)
    # Remove outliers
    df = df.loc[df['game_regular_price'] < df.game_regular_price.quantile(0.995)]
    df = df.loc[df['game_actual_price'] < df.game_actual_price.quantile(0.995)]
    # Filter by store
    df = df.loc[df['game_store_name'] == 'Steam']

    # Create new rows to account sales price during duration and days when game was not on sale
    today = pd.to_datetime(pd.datetime.today()).floor('D')
    dates = pd.date_range(df.game_date.min(), today, name='game_date').date

    # Normalize dates
    df.loc[:, ('game_date')] = pd.to_datetime(df.game_date).dt.date

    # Drop duplicate dates since this is by days. More prone to duplicated dates
    df.drop_duplicates(subset=['game_date'], keep='first', inplace=True)

    # Has all dates up until today
    df_1 = df.set_index('game_date').sort_index().reindex(dates, method='ffill')

    # Merged df and df_1 to combine the missing dates with df
    df_sale_check = pd.merge(df_1,
                             df['game_date'],
                             left_on='game_date',
                             right_on='game_date',
                             how='left',
                             indicator=True)

    # Days that were not add on sale should not be indicative of a sales
    # game_actual_price should be the same as game_regular_price
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'game_actual_price')] = df_sale_check.loc[(df_sale_check._merge == 'left_only', 'game_regular_price')]
    # There should be no sale_duration, game_stores_name, sale_duration_number, sale_duration_unit, end_date, and days_to_add
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'sale_duration')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'game_stores_name')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'sale_duration_number')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'sale_duration_unit')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'end_date')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only', 'days_to_add')] = None
    df_sale_check.loc[(df_sale_check._merge == 'left_only')]
    # Concat the missing days df to the working df
    df_final = pd.concat([df, df_sale_check.loc[(df_sale_check._merge == 'left_only')]]).set_index('game_date').sort_index()

    return df_final