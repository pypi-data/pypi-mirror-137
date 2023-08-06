
def test_get(abckpi_instance):

    path = 'user/current_user/'
    current_user = abckpi_instance._get(path)

    assert isinstance(current_user['pk'], int)


def test_get_current_user(abckpi_instance):

    current_user = abckpi_instance.get_current_user()

    assert isinstance(current_user['pk'], int)


def test_get_organization(abckpi_instance):

    organization = abckpi_instance.get_organization()

    assert isinstance(organization['name'], str)
    assert isinstance(organization['pk'], int)


def test_indicator_list(abckpi_instance):

    indicator_list = abckpi_instance.get_indicators()

    for indicator in indicator_list:
        assert isinstance(indicator['name'], str)
        assert isinstance(indicator['pk'], int)

