'''
Created on Dec 10, 2012

@author: James Renfro
'''
from django.test import TestCase
from vm.v1.viewmodels import Receipt, Serializer
from vm.v1.test.endpoint import ExampleEndpoint

import uuid

class ExampleReceipt(object):
    
    def create(self, to_consume=True, sent=True, child=False):
        receipt = Receipt()
        receipt.receipt_id = 'be13a0c1-9a75-41f9-9ccf-f026e2b84c4d'
        if sent:
            receipt.dispatched_on = '2012-10-13 21:49:07.162630+00:00Z'
            receipt.dispatched_by = 'Twilio REST API'
            receipt.status = 'dispatched'
        else:
            receipt.dispatched_on = None
            receipt.dispatched_by = None
            receipt.status = 'pending'
        receipt.retries = 0
        receipt.endpoint = ExampleEndpoint().create(to_consume=to_consume, confirmed=sent)
        
        if not to_consume:
            receipt.created = '2012-11-13 21:49:07.162630+00:00'
            receipt.last_modified = '2012-11-13 21:49:07.162630+00:00'
            
        return receipt 
        