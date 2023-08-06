import pandas as pd

def calculate_stat_summary(df, column):
    """Creates summary information about the 
       covid cases in each province of Canada

    Parameters
    ----------
    df : pandas.DataFrame
        Pandas DataFrame containing covid data to summary.
    column : string
        column name, specifying which column to summarize.
        the data type of the column must be numeric.

    Returns
    -------
    pandas.DataFrame
        pandas DataFrame containing summary information.

    Examples
    --------
    >>> calculate_stat_summary(covid_df, 'cases')
    >>> calculate_stat_summary(covid_df, 'cumulative_deaths')
    """


    # Check input dataframe validity
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Invalid argument type: df must be a pandas DataFrame")
    elif len(df) == 0:
        raise ValueError("Argument value error: df must contain at least one row of data")
    elif not ('province' in df.columns):
        raise ValueError("Argument value error: df must contain province columns")

    columns = list(df.columns)

    for i in range(len(columns)):
        if columns[i].startswith('date'):
            date_col = columns[i]
            break

    # Check column name validity
    if not isinstance(column, str):
        raise TypeError("Invalid argument type: column must be a string")
    elif column not in columns:
        raise ValueError("The column name does not exist in the dataframe,\
                        Choose a valid column name")

    # Check the data type of the column
    if not (df[column].dtype == 'int64' or df[column].dtype == 'float64'):
        raise TypeError("Invalid argument type: this column must be numeric")

    # Select the up to date information of each province
    df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y')
    start_date = df.loc[df[date_col].argmin(), date_col]
    end_date = df.loc[df[date_col].argmax(), date_col]
    columns = [date_col, 'province'] + [column]
    summary = df[df[date_col] == end_date][columns].sort_values('province')

    # Summarize the min, max and mean of the selected summary column
    min_value = []
    max_value = []
    mean_value = []
    std = []
    count = []
    percentile_25 = []
    percentile_50 = []
    percentile_75 = []
    
    for i in range(len(summary)):
        province = summary.iloc[i, 1]
        summ = df[df['province'] == province][column].describe()
        min_value.append(int(summ[3]))
        max_value.append(int(summ[7]))
        mean_value.append(int(summ[1]))
        percentile_25.append(int(summ[4]))
        percentile_50.append(int(summ[5]))
        percentile_75.append(int(summ[6]))
        std.append(int(summ[2]))
        count.append(int(summ[0]))

    summary['min'] = min_value
    summary['max'] = max_value
    summary['mean'] = mean_value
    summary['25%'] = percentile_25
    summary['50%'] = percentile_50
    summary['75%'] = percentile_75
    summary['std'] = std
    summary['count'] = count
    summary['start_date'] = start_date
    
    return(summary)