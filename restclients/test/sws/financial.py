from django.test import TestCase
from django.conf import settings
from restclients.sws.financial import get_account_balances_by_regid
import datetime

class SWSFinance(TestCase):
    def test_financial_resource(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            data = get_account_balances_by_regid("9136CCB8F66711D5BE060004AC494FFE")
            self.assertEquals(data.tuition_accbalance, "12345.00")
            self.assertEquals(data.pce_accbalance, "0.00")

            data = get_account_balances_by_regid("FE36CCB8F66711D5BE060004AC494F31")
            self.assertEquals(data.tuition_accbalance, "12345.00")
            self.assertEquals(data.pce_accbalance, "345.00")
