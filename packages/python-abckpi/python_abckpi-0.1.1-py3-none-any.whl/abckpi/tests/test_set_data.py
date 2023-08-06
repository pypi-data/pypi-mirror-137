import random


def test_set_data(abckpi_instance, indicator_pk):

    value_to_set = random.random() * 1000.
    date_to_set = '2022-01-01'
    abckpi_instance.set_data_point(indicator_pk=indicator_pk,
                                   time_step='M',
                                   data_type='A',
                                   date=date_to_set,
                                   value=value_to_set)

    data_point_date = abckpi_instance.get_data_points(indicator_pk=indicator_pk,
                                                      time_step='M',
                                                      data_type='A',
                                                      date=date_to_set)

    assert data_point_date['value'] == value_to_set