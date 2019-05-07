FreeAgent Transferwise Importer
===============================

A small script to import Transferwise transactions into FreeAgent as bank
transactions.

This will create bank accounts in FreeAgent with the names of "TransferWise USD
account", etc, and then upload statements to FreeAgent when run against those
bank accounts.

How to use
----------

1. Copy config.ini.sample to config.ini and then alter the values within.
2. Create a Transferwise API token: https://transferwise.com/user/settings.
   You should create one with 'read only' privileges. This goes in the
   api_token part of the config.ini
3. Create a Freeagent app, place the OAuth identifier and secret in
   config.ini.
4. Follow https://dev.freeagent.com/docs/quick_start to get a refresh token
   for config.ini (remember to remove sandbox from the URLs), and add that
   to your config.ini.
5. `python3 -mfreeagent_transferwise_importer`
