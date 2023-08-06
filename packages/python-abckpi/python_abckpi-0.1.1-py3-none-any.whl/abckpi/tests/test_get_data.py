from ..utils import validate_date_format
try:
    import pandas as pd
    is_pandas_installed = True
except ImportError:
    is_pandas_installed = False


def test_search_dataset(abckpi_instance, indicator_pk):
    datasets = abckpi_instance.search_datasets(indicator_pk=indicator_pk,
                                               time_step='M',
                                               data_type='A')

    assert isinstance(datasets['pk'], int)
    assert datasets['time_step'] == 'M'
    assert datasets['type'] == 'A'
    assert datasets['indicator'] == indicator_pk


def test_get_data_points(abckpi_instance, indicator_pk):
    data_points = abckpi_instance.get_data_points(indicator_pk=indicator_pk,
                                                  time_step='M',
                                                  data_type='A')

    for data_point in data_points:
        assert isinstance(data_point['data_set'], int)
        assert validate_date_format(data_point['date'], '%Y-%m-%d')
        assert isinstance(data_point['value'], float)

    example_date = data_points[0]['date']

    data_point_date = abckpi_instance.get_data_points(indicator_pk=indicator_pk,
                                                      time_step='M',
                                                      data_type='A',
                                                      date=example_date)
    assert isinstance(data_point_date['data_set'], int)
    assert validate_date_format(data_point_date['date'], '%Y-%m-%d')
    assert isinstance(data_point_date['value'], float)


def test_get_data_point_pandas(abckpi_instance, indicator_pk):

    if is_pandas_installed:
        data_points = abckpi_instance.get_data_points(indicator_pk=indicator_pk,
                                                      time_step='M',
                                                      data_type='A',
                                                      return_type='pandas')
        assert isinstance(data_points, pd.Series)
    else:
        print('This test cannot run without pandas installed')
