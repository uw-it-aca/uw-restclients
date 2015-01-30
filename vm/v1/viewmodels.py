try:
    from collections import OrderedDict
except Exception:
    from ordereddict import OrderedDict

from datetime import datetime
from dateutil import parser, tz
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
try:
    from django.utils.encoding import smart_text
    smart_unicode = smart_text
except Exception:
    from django.utils.encoding import smart_unicode
from django.utils.timezone import utc

import re
import simplejson as json
import logging
import six
from six import with_metaclass

# Get an instance of a logger
logger = logging.getLogger(__name__)


def parse_iso_8601(s):
    return parser.parse(s).astimezone(tz.tzutc())


class Field(object):

    def __init__(self, dictionary_key=None, ordinal=0, attribute_name=None, model_attribute=None, comparable=True, produceable=True, consumable=True, optional=False, blank=False, extended=False, modelizable=True):
        self.dictionary_key = dictionary_key
        self.ordinal = ordinal
        self.attribute_name = attribute_name
        self.model_attribute = model_attribute
        self.comparable = comparable
        self.produceable = produceable
        self.consumable = consumable
        self.optional = optional
        self.blank = blank
        self.extended = extended
        self.modelizable = modelizable
        
    def __cmp__(self, other):
        
        if self is not None and other is not None:

            if hasattr(self, 'ordinal') and hasattr(other, 'ordinal'):
                if self.ordinal < other.ordinal:
                    return -1
                if self.ordinal > other.ordinal:
                    return 1
        
        return 0

    # Python3 - __cmp__ is ignored for sorting.
    def __lt__(self, other):
        if self is not None and other is not None:
            if hasattr(self, 'ordinal') and hasattr(other, 'ordinal'):
                if self.ordinal < other.ordinal:
                    return True
        return False


    def from_model_attribute(self, model):
        if not self.modelizable:
            return None
        
        return getattr(model, self.model_attribute)
 
    def from_object_literal(self, value):
        return value
    
    def to_model_attribute(self, value):
        return value
    
    def to_object_literal(self, value):
        return value
    
    def validate(self, obj, invalid_fields):
        if self.consumable and not self.optional:
            value = getattr(obj, self.attribute_name)
            if not value or value is None or value == '' or isinstance(value, Field):
                invalid_fields[self.dictionary_key] = 'Field is required'
 
class BooleanField(Field):
       
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)
        
    def from_model_attribute(self, model):
        if not self.modelizable:
            return None
        
        value = getattr(model, self.model_attribute)
   
        if value is None:
            return False
   
        return bool(value)
   
class DateField(Field):
    
    def from_model_attribute(self, model):
        value = getattr(model, self.model_attribute)
        return value
    
    def from_object_literal(self, value):
        if value is not None:
            try:
                return parser.parse(value).astimezone(tz.tzutc())
            except ValueError:
                pass
            except TypeError:
                pass

        return None
        
    def to_model_attribute(self, value):
        return value 
    
    def to_object_literal(self, value):
        if value is not None and isinstance(value, datetime):
            return value.replace(tzinfo = utc).isoformat('T')
        return None
    
#    def validate(self, obj, invalid_fields):
#        if self.consumable:
#            try:
#                value = getattr(obj, self.attribute_name)
#                if value is not None and not isinstance(value, Field):
#                    parser.parse(value).astimezone(tz.tzutc())
#                    invalid_fields[self.dictionary_key] = 'Field is required'
#            except AttributeError:
#                pass
        
class LastModifiedDateField(DateField):
    
    def __init__(self, *args, **kwargs):
        kwargs['consumable'] = False
        kwargs['comparable'] = False
        super(LastModifiedDateField, self).__init__(*args, **kwargs)  
            
class ExtendedDateField(DateField):
    
    def __init__(self, *args, **kwargs):
        kwargs['extended'] = True
        kwargs['consumable'] = False
        kwargs['comparable'] = False
        super(ExtendedDateField, self).__init__(*args, **kwargs)            
            
class IntegerField(Field):
    
    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
    
    def from_model_attribute(self, model):
        value = getattr(model, self.model_attribute)
        if value is None:
            return 0
        return value
        
    def from_object_literal(self, value):
        if value is None:
            return 0
        return int(value)
    
    def to_model_attribute(self, value):
        return value
    
class ExtendedField(Field):
    
    def __init__(self, *args, **kwargs):
        kwargs['extended'] = True
        kwargs['consumable'] = False
        kwargs['comparable'] = False
        super(ExtendedField, self).__init__(*args, **kwargs)
        
class MessageTypeField(Field):
    
    def __init__(self, *args, **kwargs):
        super(MessageTypeField, self).__init__(*args, **kwargs)
    
    def from_model_attribute(self, model):
        if not self.modelizable:
            return None
        
        value = getattr(model, self.model_attribute)
        if value is None:
            return ''
        return value.surrogate_id

    def to_model_attribute(self, value):
        return None
         
class NetIdField(Field):
    
    def __init__(self, *args, **kwargs):
        super(NetIdField, self).__init__(*args, **kwargs)
    
    def from_model_attribute(self, model):
        value = getattr(model, self.model_attribute)
        if value is None:
            return ''
        return value.surrogate_id

    def to_model_attribute(self, value):
        return None
         
class LowerCaseField(Field):
    
    def to_model_attribute(self, value):
        if value and value is not None:
            return value.lower()
        return value
     
class UriField(Field):
    
    def __init__(self, *args, **kwargs):
        #kwargs['extended'] = True
        kwargs['produceable'] = False
        kwargs['consumable'] = False
        kwargs['comparable'] = False
        super(UriField, self).__init__(*args, **kwargs)

class ViewModelField(Field):
    
    def __init__(self, *args, **kwargs):
        self.view_model_type = kwargs.pop('view_model_type', None)
        kwargs['blank'] = True
        kwargs['consumable'] = False
        super(ViewModelField, self).__init__(*args, **kwargs)

class ViewModelBase(type):
    
    def __new__(cls, name, bases, dictionary):
        view_model = type.__new__(cls, name, bases, dictionary)
        
        view_model.fields = list()
        for name in dir(view_model):
            if isinstance(name, str):
                value = getattr(view_model, name)
                if isinstance(value, Field):
                    if value.attribute_name is None:
                        value.attribute_name = name
                    if value.model_attribute is None:
                        value.model_attribute = name
                    
                    view_model.fields.append(value)
        
        view_model.fields.sort()
        return view_model
    

class ViewModel(with_metaclass(ViewModelBase)):
    __metaclass__ = ViewModelBase
    
    def __init__(self, *args, **kwargs):                
        object_literal = kwargs.pop('object_literal', None)
        model = kwargs.pop('model', None)

        if object_literal is not None:
            self.from_object_literal(object_literal)
        elif model is not None:
            self.from_model(model)

    def __eq__(self, other):
        
        for f in self.fields:
            if f.comparable:
                v1 = getattr(self, f.attribute_name, None)
                v2 = getattr(other, f.attribute_name, None)
                
                if v1 is not None and isinstance(v1, Field):
                    v1 = None
                if v2 is not None and isinstance(v2, Field):
                    v2 = None
                
                if v1 is None and v2 is None:
                    continue
                
                if v1 is None or v2 is None or v1 != v2:
                    logger.debug('Model not equal because %s != %s', v1, v2)
                    return False
            
        return True

    def __ne__(self, other):
        
        return not self.__eq__(other)
        
    def to_model(self, model):
        for f in self.fields:
            value = getattr(self, f.attribute_name)
            if f.consumable and f.modelizable and value and value is not None and not isinstance(value, Field):
                attribute_value = f.to_model_attribute(value)
                if attribute_value is not None:
                    setattr(model, f.model_attribute, attribute_value)
        return model
            
    def from_model(self, model):
        for f in self.fields:
            if f.produceable:
                value = f.from_model_attribute(model)
                if not isinstance(value, bool) and not isinstance(value, int) and not value:
                    value = None
                if isinstance(f, ViewModelField):
                    instance = f.view_model_type(model=value)
                    setattr(self, f.attribute_name, instance)
                else:
                    setattr(self, f.attribute_name, value)
                    
        return self
            
    def from_object_literal(self, object_literal):
        if object_literal is not None:
            try:
                object_literal = object_literal[self.model_name]
            except KeyError:
                pass
            except TypeError:
                pass
            
            for f in self.fields:
                value = object_literal.get(f.dictionary_key)
                if not isinstance(f, ViewModelField):
                    setattr(self, f.attribute_name, f.from_object_literal(value))
                elif f.view_model_type is not None and value is not None:
                    instance = f.view_model_type()
                    instance.from_object_literal(value)
                    setattr(self, f.attribute_name, instance)
        return self

    def get_last_modified(self):
        if not self.last_modified or isinstance(self.last_modified, Field):
            return None
        return self.last_modified
    
    def to_object_literal(self, partial=False, child=False):
        dictionary = OrderedDict()
                            
        for f in self.fields:
            value = getattr(self, f.attribute_name)
            if not isinstance(value, bool) and not isinstance(value, int) and not value:
                value = None
            elif isinstance(value, Field):
                value = None
            elif isinstance(value, str) and value == '':
                value = None
            
            if value is None:
                show_blank = not child and not f.blank
                if partial and f.extended:
                    show_blank = False
                if not f.produceable:
                    show_blank = False
                    
                if show_blank:
                    if isinstance(f, BooleanField):
                        dictionary[f.dictionary_key] = False 
                    elif isinstance(f, IntegerField):
                        dictionary[f.dictionary_key] = 0
                    else:
                        dictionary[f.dictionary_key] = None
            else:
                if isinstance(f, ViewModelField):
                    dictionary[f.dictionary_key] = value.to_object_literal(partial=partial, child=True) 
                elif not child or not f.extended:
                    dictionary[f.dictionary_key] = f.to_object_literal(value)
        
        return dictionary

    def to_display_object_literal(self, partial=False):
        wrapper = OrderedDict()
        wrapper[self.model_name] = self.to_object_literal(partial=partial)
        return wrapper

    def validate(self):
        invalid_fields = {}
        for f in self.fields:
            f.validate(self, invalid_fields)
    
        return invalid_fields

class ListViewModel(object):
    
    def __init__(self, *args, **kwargs):                
        object_literal = kwargs.pop('object_literal', None)
        models = kwargs.pop('models', None) 
        total = kwargs.pop('total', None)
        query_params = kwargs.pop('query_params', None)
        self.view_models = list()
        if object_literal is not None:
            self.from_object_literal(object_literal)
        elif models is not None:
            self.from_models(models)
        self.total = total
        self.query_params = query_params
    
    def __eq__(self, other):
        
        for i in range(len(self.view_models)):
            m1 = self.view_models[i]
            if i < len(other.view_models):
                m2 = other.view_models[i]
            else:
                m2 = None
                
            if m1 != m2:
                return False
            
        return True

    def __ne__(self, other):
        
        return not self.__eq__(other)
    
    def add(self, view_model):
        self.view_models.append(view_model)

    def get_first_view_model(self):
        if not self.view_models or isinstance(self.view_models, Field) or len(self.view_models) <= 0:
            return None
        return self.view_models[0]

    def from_models(self, models):
        if models is not None:
            for model in models:
                view_model = self.view_model_type(model=model)
                self.view_models.append(view_model)

    def from_object_literal(self, object_literal):
        if object_literal is not None:
            try:
                object_literal = object_literal[self.model_name]
            except KeyError:
                object_literal = object_literal
            except TypeError:
                object_literal = object_literal
                        
            for item in object_literal:
                view_model = self.view_model_type(object_literal=item)
                self.view_models.append(view_model)
                
        return self

    def to_object_literal(self, channel_model=None, partial=False, child=True):
        list_of_dictionaries = list()
        if self.view_models is not None: 
            for view_model in self.view_models:
                if view_model is not None:
                    list_of_dictionaries.append(view_model.to_object_literal(partial=partial, child=child))

        return list_of_dictionaries;
     
    def to_display_object_literal(self, total=None, query_params=None, partial=False):
        wrapper = OrderedDict()
        wrapper[self.model_name] = self.to_object_literal(partial=partial)
        if query_params is not None:
            wrapper['QueryParams'] = query_params
        elif self.query_params is not None:
            wrapper['QueryParams'] = self.query_params
        if total is not None:
            wrapper['TotalCount'] = total
        elif self.total is not None:
            wrapper['TotalCount'] = self.total
        return wrapper
        
class DictionaryViewModel(ViewModel):

    def __init__(self): 
        self.view_models = list()
    
    def __eq__(self, other):
        
        name_value_map = {}
        for view_model in self.view_models:
            name_value_map[view_model.name] = view_model.value
        
        for view_model in other.view_models:
            value = name_value_map[view_model.name]
            if value == view_model.value:
                del name_value_map[view_model.name]
                
        if len(name_value_map) > 0:
            return False
        
        return True

    def __ne__(self, other):
        
        return not self.__eq__(other)
    
    def add(self, view_model):
        self.view_models.append(view_model)

    def from_object_literal(self, object_literal):
        if six.PY2:
            items = object_literal.iteritems
        else:
            items = object_literal.items
        for k, v in items():
            self.add(ParameterDetailViewModel(k,v))
        return self

    def to_object_literal(self, partial=False, child=True):
        dictionary = OrderedDict()
        if self.view_models is not None: 
            for view_model in self.view_models:
                dictionary[view_model.name] = view_model.value
        
        return dictionary

class Endpoint(ViewModel):

    model_name = 'Endpoint'
    view_name = 'endpoint-detail'

    endpoint_id = Field('EndpointID', 1, optional=True)
    endpoint_uri = UriField('EndpointURI', 2)
    endpoint_address = Field('EndpointAddress', 3)
    carrier = Field('Carrier', 4, optional=True)
    protocol = LowerCaseField('Protocol', 5)
    user = NetIdField('SubscriberID', 6, optional=True)
    owner = NetIdField('OwnerID', 7)
    status = Field('Status', 8, optional=True, comparable=False, consumable=False)
    active = BooleanField('Active', 9, consumable=False)
    created = ExtendedDateField('Created', 11)
    last_modified = LastModifiedDateField('LastModified', 12)
    modified_by = ExtendedField('ModifiedBy', 13)
    
    def get_endpoint_id(self):
        if not self.endpoint_id or isinstance(self.endpoint_id, Field):
            return None
        return self.endpoint_id
    
    def get_owner_net_id(self):
        if not self.owner or isinstance(self.owner, Field):
            return None
        return self.owner
    
    def get_user_net_id(self):
        if not self.user or isinstance(self.user, Field):
            return None
        return self.user
    
    def get_endpoint_address(self):
        if self.protocol is not None:
            if self.protocol.lower() == 'sms':
                regex1 = re.compile('^\+1\d{10}$')
                regex2 = re.compile('^\d{3}\-\d{3}-\d{4}$')
                regex3 = re.compile('^\(\d{3}\)\d{3}-\d{4}$')
                phone_number = smart_unicode(self.endpoint_address)
        
                if regex1.search(phone_number):
                    return phone_number
                
                if regex2.search(phone_number):
                    return "+1{0}{1}{2}".format(phone_number[0:3], phone_number[4:7], phone_number[8:12])
                
                if regex3.search(phone_number):
                    return "+1{0}{1}{2}".format(phone_number[1:4], phone_number[5:8], phone_number[9:13])
      
        return self.endpoint_address
    
    def validate(self):
        invalid_fields = ViewModel.validate(self)
        
        if self.protocol is not None: 
            if self.protocol.lower() == 'email':
                try:
                    validate_email(self.endpoint_address)
                except ValidationError:
                    invalid_fields['EndpointAddress'] = 'Invalid format for an email address'
            elif self.protocol.lower() == 'sms':
                regex1 = re.compile('^\+1\d{10}$')
                regex2 = re.compile('^\d{3}\-\d{3}-\d{4}$')
                regex3 = re.compile('^\(\d{3}\)\d{3}-\d{4}$')
                phone_number = smart_unicode(self.endpoint_address)
                if not regex1.search(phone_number) and not regex2.search(phone_number) and not regex3.search(phone_number):
                    invalid_fields['EndpointAddress'] = 'Invalid format for a phone number; should be one or these: +###########, ###-###-####, or (###)###-####'

        return invalid_fields

class EndpointList(ListViewModel):
    
    model_name = 'Endpoints' 
    view_model_type = Endpoint
    
class Job(ViewModel):
    
    model_name = 'Job'
    view_name = 'job-detail'
    
    job_id = Field('JobID', 1, optional=True)
    job_uri = UriField('JobURI', 2)
    job_type = LowerCaseField('JobType', 3)
    execution_type = LowerCaseField('ExecutionType', 4, optional=True)
    created = ExtendedDateField('Created', 11)
    last_modified = LastModifiedDateField('LastModified', 12)
    modified_by = ExtendedField('ModifiedBy', 13)
    
class JobList(ListViewModel):
    
    model_name = 'Jobs'
    view_model_type = Job
    
class ParameterDetailViewModel(ViewModel):
    
    name = Field('Name', 1)
    value = Field('Value', 2)
    
    def __init__(self, name=None, value=None):
        super(ParameterDetailViewModel, self).__init__(self, object_literal=None, model=None)
        self.name = name
        self.value = value
        
    def __eq__(self, other):
        
        if self.name == other.name and self.value == other.value:
            return True
        return False
    
    def __ne__(self, other):    
        return not self.__eq__(other)
    
    
    def to_object_literal(self):
        dictionary = OrderedDict()
        k = getattr(self, 'name')
        v = getattr(self, 'value')
        if k and v and not isinstance(k, Field) and not isinstance(v, Field):
            dictionary[k] = v
        
        return dictionary
    
class Channel(ViewModel):
        
    model_name = 'Channel'
    view_name = 'channel-detail'
        
    channel_id = Field('ChannelID', 1, optional=True)
    channel_uri = UriField('ChannelURI', 2)
    surrogate_id = Field('SurrogateID', 3)
    type = Field('Type', 4, model_attribute='channel_type')
    name = Field('Name', 5)
    tags = ViewModelField('Tags', 6, view_model_type=DictionaryViewModel, produceable=False)
    description = Field('Description', 8, optional=True)
    expires = DateField('Expires', 10, optional=True, comparable=False)
    created = ExtendedDateField('Created', 11)
    last_modified = LastModifiedDateField('LastModified', 12)
    modified_by = ExtendedField('ModifiedBy', 13)

    def get_channel_id(self):
        if not self.channel_id or isinstance(self.channel_id, Field):
            return None
        return self.channel_id

    def add_tag(self, name, value):
        if not self.tags or isinstance(self.tags, ViewModelField):
            self.tags = DictionaryViewModel()
        tag = ParameterDetailViewModel(name, value)
        self.tags.add(tag)
        return tag
    
    def get_tags(self):
        if not self.tags or isinstance(self.tags, ViewModelField):
            return None
        return self.tags.view_models
    
class ChannelList(ListViewModel):
    
    model_name = 'Channels'  
    view_model_type = Channel     

class Subscription(ViewModel):
    
    model_name = 'Subscription'
    view_name = 'subscription-detail'
     
    subscription_id = Field('SubscriptionID', 1, optional=True)
    subscription_uri = UriField('SubscriptionURI', 2)
    subscription_type = Field('SubscriptionType', 3, optional=True, blank=True)
    channel = ViewModelField('Channel', 4, view_model_type=Channel)
    endpoint = ViewModelField('Endpoint', 5, view_model_type=Endpoint)
    created = ExtendedDateField('Created', 11)
    last_modified = LastModifiedDateField('LastModified', 12)
    modified_by = ExtendedField('ModifiedBy', 13)

    def get_subscription_id(self):
        if not self.subscription_id or isinstance(self.subscription_id, Field):
            return None
        return self.subscription_id

    def get_channel(self):
        if not self.channel or isinstance(self.channel, ViewModelField):
            return None
        return self.channel
    
    def get_endpoint(self):
        if not self.endpoint or isinstance(self.endpoint, ViewModelField):
            return None
        return self.endpoint

class SubscriptionList(ListViewModel):
    
    model_name = 'Subscriptions'  
    view_model_type = Subscription     
    
    
class Receipt(ViewModel):
    
    model_name = 'Receipt'
    view_name = 'receipt-detail'
    
    receipt_id = Field('ReceiptID', 1, optional=True)
    #receipt_uri = UriField('ReceiptURI', 2)
    surrogate_id = Field('SurrogateID', 2)
    status = Field('Status', 3)
    dispatched_on = DateField('DispatchedOn', 4, consumable=False, comparable=False)
    dispatched_by = Field('DispatchedBy', 5, consumable=False, comparable=False)
    dispatch_status = Field('DispatchStatus', 6)
    retries = IntegerField('NumberOfRetries', 7)
    endpoint = ViewModelField('Endpoint', 8, view_model_type=Endpoint, optional=True)
    created = ExtendedDateField('Created', 9)
    last_modified = LastModifiedDateField('LastModified', 10)
    modified_by = ExtendedField('ModifiedBy', 11)
    
    def get_endpoint(self):
        if not self.endpoint or isinstance(self.endpoint, ViewModelField):
            return None
        return self.endpoint
    
class ReceiptList(ListViewModel):
    
    model_name = 'Receipts'
    view_model_type = Receipt
    
    def to_object_literal(self, channel_model=None, partial=False, child=True):
        list_of_dictionaries = list()
        if self.view_models is not None: 
            for view_model in self.view_models:
                if view_model is not None:
                    list_of_dictionaries.append(view_model.to_object_literal(partial=partial, child=False))

        return list_of_dictionaries;
        
class MessageType(ViewModel):
    
    model_name = 'MessageType'
    view_name = 'message-type-detail'
     
    message_type_id = Field('MessageTypeID', 1, optional=True)
    message_type_uri = UriField('MessageTypeURI', 2)
    surrogate_id = Field('SurrogateID', 3)
    content_type = Field('ContentType', 4)
    destination_id = Field('DestinationID', 5)
    destination_type = Field('DestinationType', 6)
    sender = Field('From', 7)
    to = Field('To', 8)
    subject = Field('Subject', 9)
    body = Field('Body', 10)
    short = Field('Short', 11)
    created = ExtendedDateField('Created', 12)
    last_modified = LastModifiedDateField('LastModified', 13)
    modified_by = ExtendedField('ModifiedBy', 14)

class MessageTypeList(ListViewModel):
    
    model_name = 'MessageTypes'  
    view_model_type = MessageType 
    
class Message(ViewModel):
    
    model_name = 'Message'
    view_name = 'message-detail'
    
    message_id = Field('MessageID', 1, optional=True)
    message_uri = UriField('MessageURI', 2)
    message_type = MessageTypeField('MessageType', 3)
    direction = LowerCaseField('Direction', 4)
    subject = Field('Subject', 5)
    body = Field('Body', 6)
    short = Field('Short', 7)
    receipts = ViewModelField('Receipts', 8, view_model_type=ReceiptList, optional=True, produceable=False)
    created = ExtendedDateField('Created', 9)
    last_modified = LastModifiedDateField('LastModified', 10)
    modified_by = ExtendedField('ModifiedBy', 11)
    
    def get_message_id(self):
        if not self.message_id or isinstance(self.message_id, Field):
            return None
        return self.message_id
    
    def add_receipt(self, receipt_view_model):
        if not self.receipts or isinstance(self.receipts, ViewModelField):
            self.receipts = ReceiptList()
        self.receipts.add(receipt_view_model)
        return self.receipts
    
class MessageList(ListViewModel):
    
    model_name = 'Messages'
    view_model_type = Message
   
class Dispatch(ViewModel):
    
    model_name = 'Dispatch'
    view_name = 'dispatch-detail'
    
    dispatch_id = Field('DispatchID', 1, optional=True)
    dispatch_uri = UriField('DispatchURI', 2)
    message_type = MessageTypeField('MessageType', 3, modelizable=False, produceable=False)
    message = ViewModelField('Message', 4, view_model_type=Message)
    content = Field('Content', 5, comparable=False)
    directive = LowerCaseField('Directive', 6, optional=True)
    recipients = IntegerField('NumberOfRecipients', 7, consumable=False)
    locked = BooleanField('Locked', 8, optional=True, modelizable=False)
    lock_id = Field('LockID', 9, optional=True, produceable=False)
    locked_on = Field('LockedOn', 10, optional=True, produceable=False)
    locked_by = Field('LockedBy', 11, optional=True, produceable=False)
    last_modified = LastModifiedDateField('LastModified', 11)
    
    def get_content(self):
        if not self.content or isinstance(self.content, Field):
            return None
        return self.content
    
    def get_message(self):
        if not self.message or isinstance(self.message, ViewModelField):
            return None
        return self.message
    
    def get_message_type(self):
        if not self.message_type or isinstance(self.message_type, MessageTypeField):
            return None
        return self.message_type
    
    
class DispatchList(ListViewModel):
    
    model_name = 'Dispatches'
    view_model_type = Dispatch

class Person(ViewModel):
    
    model_name = 'Person'
    view_name = 'person-detail'
    
    person_id = Field('PersonID', 1, optional=True)
    person_uri = UriField('PersonURI', 2)
    surrogate_id = Field('SurrogateID', 3)
    attributes = ViewModelField('Attributes', 6, view_model_type=DictionaryViewModel, produceable=False)
    default_endpoint = ViewModelField('DefaultEndpoint', 8, view_model_type=Endpoint, produceable=False)
    endpoints = ViewModelField('Endpoints', 9, view_model_type=EndpointList, produceable=False)
    created = ExtendedDateField('Created', 10)
    last_modified = LastModifiedDateField('LastModified', 11)
    modified_by = ExtendedField('ModifiedBy', 12)
    
    def add_attribute(self, name, *options):
        if len(options) > 1:
            logger.debug("just use add_attribute(name, value) for attribute %s" % name)
        value = None
        for option in options:
            if option is not None:
                value = option

        if not self.attributes or isinstance(self.attributes, ViewModelField):
            self.attributes = DictionaryViewModel()

        attribute = ParameterDetailViewModel(name, value)
        self.attributes.add(attribute)
        return attribute
    
    def get_attributes(self):
        if not self.attributes or isinstance(self.attributes, ViewModelField):
            return None
        return self.attributes.view_models
    
    def get_endpoints(self):
        if not self.endpoints or isinstance(self.endpoints, ViewModelField):
            return None
        return self.endpoints.view_models
    
    def get_default_endpoint(self):
        if not self.default_endpoint or isinstance(self.default_endpoint, ViewModelField):
            return None
        return self.default_endpoint
    
    def validate(self):
        invalid_fields = ViewModel.validate(self)
        
        if self.surrogate_id is not None: 
            try:
                validate_email(self.surrogate_id)
            except ValidationError:
                invalid_fields['SurrogateID'] = 'Invalid format for an eduPersonPrincipalName (EPPN)'

        return invalid_fields
    
class PersonList(ListViewModel):
    
    model_name = 'People'
    view_model_type = Person


class MessageSummary(ViewModel):
    
    message_uri = UriField('MessageDetailURI', 1)
    direction = Field('Direction', 2)
    protocol = Field('Protocol', 3)
    content = Field('Content', 6)
    
class MessageSummaryList(ListViewModel):
    
    model_name = 'MessageSummaries'
    view_model_type = MessageSummary

class Activity(ViewModel):
    
    activity_detail_uri = UriField('ActivityDetailURI', 4)
    activity_type = Field('Type', 3)
    description = Field('Description', 4)
    value = Field('Value', 5)
    activity_date = Field('ActivityDate', 6)
    
class ActivityList(ListViewModel):

    model_name = 'Activities'
    view_model_type = Activity
    
class Status(ViewModel):
    
    model_name = 'Status'
    view_name = 'status-detail'
    
    last_success_delay = Field('SecondsToDispatchLastSuccessfulHeartbeat', 1)
    last_success_since = Field('SecondsSinceLastSuccessfulHeartbeat', 2)
    
    last_heartbeat_since = Field('SecondsSinceLastHeartbeat', 3)
    last_heartbeat_status = Field('LastHeartbeatStatus', 4)
    
    number_of_locks = Field('NumberOfLocks', 5)
    last_job = Field('SecondsSinceLastJob', 6)
    last_message = Field('SecondsSinceLastMessage', 7)
    dispatch_queue_size = Field('SizeOfDispatchQueue', 8)
    
    
class Serializer(object):
    
    def deserialize(self, view_model, data, force_consume=True):
        object_literal = json.loads(data, object_pairs_hook=OrderedDict)
        view_model.from_object_literal(object_literal)
        return view_model
        
    def serialize(self, view_model, partial=False):
        return json.dumps(view_model.to_display_object_literal(partial=partial), indent='\t')
    
    
    
