import datetime

import requests


class FreeAgent:
    _HOST = 'https://api.freeagent.com'

    def __init__(self, client_id, client_secret, refresh_token):
        response = requests.post(
            f'{self._HOST}/v2/token_endpoint',
            auth=(client_id, client_secret),
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            },
        )
        response.raise_for_status()
        self._access_token = response.json()['access_token']

    def get_or_create_bank_account(self, currency):
        response = self._make_request('v2/bank_accounts')
        response.raise_for_status()
        for bank_account in response.json()['bank_accounts']:
            if bank_account['name'] == f'TransferWise {currency} Account':
                return bank_account['url'], datetime.datetime.fromisoformat(bank_account['latest_activity_date'])
        else:
            response = requests.post(
                f'{self._HOST}/v2/bank_accounts',
                json={
                    'bank_account': {
                        'name': f'TransferWise {currency} Account',
                        'currency': currency,
                        'opening_balance': 0
                    },
                },
                headers={'Authorization': f'Bearer {self._access_token}'},
            )
            response.raise_for_status()
            return response.headers['Location'], None

    def add_transactions(self, account_id, transactions):
        response = requests.post(
            f'{self._HOST}/v2/bank_transactions/statement',
            headers={'Authorization': f'Bearer {self._access_token}'},
            params={'bank_account': account_id},
            data={"statement": transactions},
        )
        response.raise_for_status()

    def _make_request(self, endpoint, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = f'Bearer {self._access_token}'
        return requests.get(f'{self._HOST}/{endpoint}', *args, **kwargs)
