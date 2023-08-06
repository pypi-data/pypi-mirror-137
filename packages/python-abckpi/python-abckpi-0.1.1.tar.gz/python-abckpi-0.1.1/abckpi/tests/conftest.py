import os
import pytest
from dotenv import load_dotenv
from abckpi.core import Instance


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='session')
def abckpi_instance():
    return Instance(username=os.environ.get('ABCKPI_USER'),
                    password=os.environ.get('ABCKPI_PASSWORD'),
                    host_url='staging.abckpi.com')


@pytest.fixture(scope='session')
def indicator_pk(abckpi_instance):
    indicator_list = abckpi_instance.get_indicators()

    return indicator_list[0]['pk']
