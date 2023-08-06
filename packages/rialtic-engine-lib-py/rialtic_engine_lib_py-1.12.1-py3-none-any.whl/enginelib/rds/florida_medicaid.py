from typing import Set

from enginelib.errors import Error
from enginelib.rds.client import db_client, db_name


class FloridaMedicaid:
    @staticmethod
    def codes_on_fl_mcd_dme_fee_schedule(transaction_id: str) -> Set[str]:
        # noinspection SqlResolve
        query = f'''
        SELECT code
        FROM {db_name}.mcd_fl
        WHERE "policy" = 'Durable Medical Equipment';'''
        records, err = db_client.GetReferenceData(transactionId=transaction_id, query=query)
        if err:
            raise Error(f'Failed to fetch data from the "FL MCD DME Fee Schedule" reference data set: {err}')
        return {record['code'] for record in (records or list())}
