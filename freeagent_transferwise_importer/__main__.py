import csv
import datetime
from configparser import ConfigParser
from io import StringIO

from freeagent_transferwise_importer.freeagent import FreeAgent
from freeagent_transferwise_importer.transferwise import BorderlessAccount

config = ConfigParser()
config.read("config.ini")

transferwise = BorderlessAccount(**config["transferwise"])
freeagent = FreeAgent(**config["freeagent"])

account_id, currencies = transferwise.get_account_id_and_currencies()
for currency in currencies:
    bank_account_id, last_updated = freeagent.get_or_create_bank_account(currency)
    transactions = transferwise.get_transactions(account_id, currency, last_updated)
    statement_file = StringIO()
    statement_csv = csv.writer(statement_file)
    for transaction in transactions:
        statement_csv.writerow(
            [
                datetime.datetime.strptime(
                    transaction["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%d/%m/%Y"),
                transaction["amount"]["value"],
                transaction["details"]["description"],
            ]
        )
        statement_csv.writerow(
            [
                datetime.datetime.strptime(
                    transaction["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).strftime("%d/%m/%Y"),
                transaction["totalFees"]["value"],
                f'Fee for {transaction["details"]["description"]}',
            ]
        )
    statement = statement_file.getvalue()
    if statement:
        freeagent.add_transactions(bank_account_id, statement)
    statement_file.close()
