import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from cassandra.references.load_holidays import load_holidays

def create_dataset(path_csv, delimiter_csv=',', subset_columns=[], rename_columns={}):
    # Read data from a CSV file
    # @on_bad_lines - defines what to do in case a line is not properly formatted
    # @delimiter - specify the delimiter used in CSV
    df = pd.read_csv(path_csv, delimiter=delimiter_csv, on_bad_lines='skip')

    # Get a subset of variables, keep only the ones you need
    if subset_columns:
        df = df[subset_columns]

    # Rename variables in order to follow the same rules across all sources
    # It makes it easier to know what we are looking at
    # Hint: always keep the channel first in the name so it's easier to understand
    if rename_columns:
        df = df.rename(columns=rename_columns)

    return df

def create_data_columns(df, name_date_column, national_holidays_abbreviation = 'IT'):

    # Optional - If not already in datetime, cast your date variable as following
    df[name_date_column] = pd.to_datetime(df[name_date_column])

    # Create a column with number of day in the week
    df['day_week'] = pd.DatetimeIndex(df[name_date_column]).weekday

    df = df.reset_index(drop=True)

    # creating instance of one-hot-encoder
    # creating one column for every
    enc = OneHotEncoder(handle_unknown='ignore')
    enc_df = pd.DataFrame(enc.fit_transform(df[['day_week']]).toarray())
    df = df.join(enc_df)

    df.rename({
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thu',
        4: 'fri',
        5: 'sat',
        6: 'sun'
    }, axis=1, inplace=True)

    # Create a column with week
    df['week'] = df[name_date_column].dt.strftime('%V')
    # Create a column with month
    df['month'] = pd.DatetimeIndex(df[name_date_column]).month
    # Create a column with year
    df['year'] = pd.DatetimeIndex(df[name_date_column]).year

    def data_weekly(row):
        return str(row['week']) + ' - ' + str(int(row['year']))

    # Create a column with number of the week and related year
    df['week_and_year'] = df.apply(lambda row: data_weekly(row), axis=1)

    # for index, row in df.iterrows():
    #   if row['day_week'] == 5 or row['day_week'] == 6:
    #       df.at[index, 'weekend'] = 1
    #   else:
    #       df.at[index, 'weekend'] = 0



    csv_holiday = load_holidays()
    national_holiday = csv_holiday.loc[csv_holiday['country'] == national_holidays_abbreviation]
    national_holiday['ds'] = pd.to_datetime(national_holiday['ds'])
    days_holiday = national_holiday.loc[:, 'ds'].values

    for index, row in df.iterrows():
      if row[name_date_column] in days_holiday:
          df.at[index, 'festivo'] = 1
      else:
          df.at[index, 'festivo'] = 0

    return df







