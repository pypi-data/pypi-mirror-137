import pandas as pd
import datetime as dt


def create_series_from_data_points(data_points):
    """
    creates a pandas Series from a dict of data points containing keys 'date' and 'value'

    :param data_points:
    :return:
    """

    date_format = '%Y-%m-%d'
    dates = [dt.datetime.strptime(data_point['date'], date_format) for data_point in data_points]

    data = pd.Series(index=dates, dtype='float64')

    for data_point in data_points:
        date = dt.datetime.strptime(data_point['date'], date_format)
        data.loc[date] = data_point['value']

    return data.sort_index()


def validate_date_format(date, format):
    """
    returns True if date respects the format

    :param date: str representing a date
    :param format: datetime compatible date format str
    :return:
    """

    try:
        dt.datetime.strptime(date, format)
    except ValueError:
        return False
    return True


def create_dataframe_from_indicators(indicators):
    """
    creates a pandas Dataframe from a list of dicts of indicators

    :param indicators:
    :return:
    """

    dict_list = []
    time_step_list = ['Day', 'Week', 'Month', 'Quarter', 'Year']

    for indicator in indicators:
        indicator_dict = {
            'pk': indicator['pk'],
            'name': indicator['name'],
            'increasing': indicator['increasing'],
        }
        for time_step in time_step_list:
            data_set = [data_set for data_set in indicator['data_sets'] if data_set['time_step'] == time_step[0]][0]
            indicator_dict[time_step] = 'Unavailable'
            if data_set['writable']:
                indicator_dict[time_step] = 'Writable'
            if data_set['aggregated']:
                indicator_dict[time_step] = 'Aggregated'

        dict_list.append(indicator_dict)

    return pd.DataFrame.from_dict(dict_list)