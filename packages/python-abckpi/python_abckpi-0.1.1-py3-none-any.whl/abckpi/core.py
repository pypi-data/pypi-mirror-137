import requests
import time

from .utils import create_series_from_data_points, validate_date_format, create_dataframe_from_indicators


def refresh_token_interceptor(func):
    def wrapper(instance, *args,**kwargs):
        if time.time() > instance.access_token_expiration:
            instance._get_tokens()
        return func(instance, *args,**kwargs)

    return wrapper


class Instance:

    host_url = None
    username = None
    refresh_token = None
    access_token = None
    access_token_expiration = None
    access_token_duration = 5 * 60  # 5 minutes

    def __init__(self, username, password, host_url='app.abckpi.com'):
        """
        Create the ABCKPI Instance by requesting acess tokens associated to the user account
        """

        self.username = username
        self.password = password
        self.host_url = host_url

        try:
            self._get_tokens()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            print(e)

    def _get_tokens(self):
        """

        request the access and refresh tokens from the api

        :return: No return. The tokens ar
        """
        try:
            token_url = f"https://{self.host_url}/auth/token/"
            auth_data = {
                'username': self.username,
                'password': self.password
            }
            token_response = requests.post(token_url, data=auth_data)

            token_response.raise_for_status()

        except Exception as e:
            print(e)
            return None
        else:
            auth_tokens = token_response.json()
            self.access_token = auth_tokens['access']
            self.refresh_token = auth_tokens['refresh']
            self.access_token_expiration = time.time() + self.access_token_duration

    @refresh_token_interceptor
    def _get(self, path, params=None):
        """
        generic _get request to the ABCKPI Instance

        :param path: the path of the request
        :param params: the parameters of the request (optional)
        :return: a dict containing the response to the request
        """

        headers = {'Authorization': f'Bearer {self.access_token}'}
        target_url = f"https://{self.host_url}/{path}"
        response = requests.get(target_url, headers=headers, params=params)
        if response.status_code != 200:
            raise ConnectionError(response.text)

        return response.json()

    @refresh_token_interceptor
    def post(self, path, data, params=None):
        """
        generic post request to the ABCKPI Instance

        :param path: the path of the request
        :param data: the data of the request
        :param params: the parameters of the request (optional)
        :return: a dict containing the response to the request
        """

        headers = {'Authorization': f'Bearer {self.access_token}'}
        target_url = f"https://{self.host_url}/{path}"
        response = requests.post(target_url, headers=headers, data=data, params=params)
        if response.status_code != 200:
            raise ConnectionError(response.text)

        return response.json()

    @refresh_token_interceptor
    def patch(self, path, data, params=None):
        """
        generic post request to the ABCKPI Instance

        :param path: the path of the request
        :param data: the data of the request
        :param params: the parameters of the request (optional)
        :return: a dict containing the response to the request
        """

        headers = {'Authorization': f'Bearer {self.access_token}'}
        target_url = f"https://{self.host_url}/{path}"
        response = requests.patch(target_url, headers=headers, data=data, params=params)
        if response.status_code != 200:
            raise ConnectionError(response.text)

        return response.json()

    def get_current_user(self):
        """
        retrieves the active organization associated to the account used to create the ABCKPI Instance

        :return: a dict containing the user information
        """

        path = 'user/current_user/'

        return self._get(path)

    def get_organization(self):
        """
        retrieves the active organization associated to the account used to create the ABCKPI Instance

        :return: a dict containing information on the active organization
        """

        user = self.get_current_user()
        active_organization = [member['organization'] for member in user['organization_memberships'] if member['active']]

        if len(active_organization) == 0:
            raise AttributeError(f"Current user {self.username} has no active organization")

        path = f'user/organization/'
        organizations = self._get(path)
        return [org for org in organizations if org['pk'] == active_organization[0]][0]

    def get_indicators(self, return_type='list'):
        """
        retrieves the list of all indicators

        :return: depending on 'return_type', either a list of dicts or pandas DataFrame
        """

        path = 'indicator/indicator/'
        indicators = self._get(path)

        if len(indicators) > 0:
            if return_type == 'list':
                return indicators
            elif return_type == 'pandas':
                return create_dataframe_from_indicators(indicators)
        else:
            return None

    def get_datasets(self):
        """
        retrieves the list of all datasets

        :return: a list of dicts
        """

        path = 'data_set/data_set/'

        return self._get(path)

    def search_datasets(self, indicator_pk, time_step, data_type):
        """
        returns the dataset corresponding to an indicator, a time step and a type

        :param indicator_pk: the primary key of the indicator for which datasets are to be returned
        :param time_step: time step of the dataset (in 'D', 'W', 'M', 'Q', 'Y')
        :param data_type: type of the dataset (can be either 'A' for actual or 'O' for objective)
        :return: a list of dicts
        """

        path = 'data_set/data_set_search/'

        parameters = {
            'indicator': indicator_pk,
            'time_step': time_step,
            'type': data_type,
        }

        return self._get(path, params=parameters)

    def get_data_points(self, indicator_pk, time_step, data_type, date=None, return_type='list'):
        """
        returns the data points corresponding to an indicator, a time step and a type

        :param indicator_pk: the primary key of the indicator for which datasets are to be returned
        :param time_step: time step of the dataset (in 'D' for day, 'W' for week, 'M' for month, 'Q' for quarter,
         'Y' for year)
        :param data_type: type of the dataset (can be either 'A' for actual or 'O' for objective)
        :param date: the date corresponding to the first day of the requested period. The date format is 'YYYY/MM/DD'.
         For example, '2022/02/01' corresponds to February 2022. If set to None, returns all the existing data points.
         Defaults to None.
        :param return_type: the data points can be returned as a list of dicts ('list') or as a pandas Series ('pandas',
         requires the optional pandas dependency to be installed). Defaults to 'list'.
        :return: depending on 'return_type', either a list of dict or pandas Series
        """
        path = 'data_set/data_set/'

        data_set = self.search_datasets(indicator_pk, time_step, data_type)

        if date is not None:
            if validate_date_format(date, '%Y-%m-%d'):
                data_points = self._get(f"{path}{data_set['pk']}/{date}")
            else:
                raise ValueError(f"{date} does not have the expected format : YYYY-MM-DD")
        else:
            data_points = self._get(f"{path}{data_set['pk']}")

        if return_type == 'list':
            return data_points[0] if len(data_points) == 1 else data_points
        elif return_type == 'pandas':
            return create_series_from_data_points(data_points)

    def set_data_point(self, indicator_pk, time_step, data_type, date, value):
        """
        Sets the value of a data point corresponding to an indicator, a time step, a data type (Actual or Objective) and
        a date

        :param indicator_pk: the primary key of the indicator for which datasets are to be returned
        :param time_step: time step of the dataset (in 'D', 'W', 'M', 'Q', 'Y')
        :param data_type: type of the dataset (can be either 'A' for actual or 'O' for objective)
        :param date: the date of the data point to be set (format YYYY-MM-DD)
        :param value: the value of the data point to be set
        :return:
        """
        update_path = 'data_set/data_point/update/'
        create_path = 'data_set/data_point/create/'

        data_set = self.search_datasets(indicator_pk, time_step, data_type)

        if validate_date_format(date, '%Y-%m-%d'):
            existing_data_point = list(filter(lambda x: x['date'] == date, data_set['data_points']))
            if len(existing_data_point) > 0:
                updated_data_point = existing_data_point[0]
                updated_data_point['value'] = value
                self.patch(f"{update_path}{updated_data_point['pk']}", updated_data_point)
            else:
                new_data_point = {
                    'data_set': data_set['pk'],
                    'date': date,
                    'value': value
                }
                self.post(create_path, new_data_point)
        else:
            raise ValueError(f"{date} does not have the expected format : YYYY-MM-DD")

