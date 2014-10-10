from restclients.sws.v4.financial import get_account_balances_by_regid as v4_get_account_balances_by_regid
from restclients.sws.v5.financial import get_account_balances_by_regid as v5_get_account_balances_by_regid
from restclients.sws import use_v5_resources

def get_account_balances_by_regid(*args, **kwargs):
    if use_v5_resources():
        return v5_get_account_balances_by_regid(*args, **kwargs)
    else:
        return v4_get_account_balances_by_regid(*args, **kwargs)

