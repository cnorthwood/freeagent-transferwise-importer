import datetime
import requests


class BorderlessAccount:
    _HOST = 'https://api.transferwise.com'

    def __init__(self, api_token):
        self._api_token = api_token

    def get_transactions(self, account_id, currency, since=None):
        if since is None:
            since = datetime.datetime(2019, 1, 1, 0, 0, 0)
        response = self._make_request(f'v1/borderless-accounts/{account_id}/statement.json', params={
            'currency': currency,
            'intervalStart': since.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'intervalEnd': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        })
        response.raise_for_status()
        for transaction in response.json()['transactions']:
            yield transaction

    def get_account_id_and_currencies(self):
        response = self._make_request('v1/borderless-accounts', params={ 'profileId': self._get_profile_id() })
        response.raise_for_status()
        account = next(account for account in response.json())
        return account['id'], [balance['currency'] for balance in account['balances']]

    def _get_profile_id(self):
        response = self._make_request('v1/profiles')
        response.raise_for_status()
        return next(profile['id'] for profile in response.json() if profile['type'] == 'business')

    def _make_request(self, endpoint, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = f'Bearer {self._api_token}'
        return requests.get(f'{self._HOST}/{endpoint}', *args, **kwargs)
