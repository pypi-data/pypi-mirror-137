
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexmodel.models.datastore.user_models import User
from trexmodel.models.datastore.merchant_models import Outlet, MerchantAcct
from trexlib.utils.string_util import random_number, is_not_empty
import logging, json
from trexmodel import conf
from datetime import datetime
from trexmodel.models.datastore.product_models import ProductCatalogue
from trexmodel.models.datastore.model_decorators import model_transactional
from google.api_core.operations_v1.operations_client_config import config

logger = logging.getLogger('model')


class POSSetting(BaseNModel,DictModel):
    '''
    merchant_acct as ancestor
    '''
    pos_name                = ndb.StringProperty(required=True)
    activation_code         = ndb.StringProperty(required=True)
    activated               = ndb.BooleanProperty(required=True, default=False)
    assigned_outlet         = ndb.KeyProperty(name="assigned_outlet", kind=Outlet)
    #assigned_catalogue      = ndb.KeyProperty(name="assigned_outlet", kind=ProductCatalogue)
    created_datetime        = ndb.DateTimeProperty(required=True, auto_now_add=True)
    activated_datetime      = ndb.DateTimeProperty(required=False)
    
    dict_properties = ['pos_name', 'activation_code', 'activated', 'assigned_outlet_key', 'activated_datetime', 'created_datetime']
    
    @property
    def assigned_outlet_key(self):
        return self.assigned_outlet.urlsafe().decode('utf-8')
    
    @property
    def assigned_outlet_entity(self):
        return Outlet.fetch(self.assigned_outlet_key)
    
    @property
    def merchant_acct_entity(self):
        return self.assigned_outlet_entity.merchant_acct_entity
    
    @staticmethod
    def create(pos_name, merchant_acct, assign_outlet):
        activation_code = random_number(16)
        checking_activation_pos_setting = POSSetting.get_by_activation_code(activation_code)
        regenerate_activation_code = False
        
        if checking_activation_pos_setting:
            regenerate_activation_code = True
        
        while(regenerate_activation_code):
            activation_code = random_number(16)
            checking_activation_pos_setting = POSSetting.get_by_activation_code(activation_code)
            if checking_activation_pos_setting==None:
                regenerate_activation_code = False
            
        
        pos_setting = POSSetting(
                                parent                  = merchant_acct.create_ndb_key(),
                                pos_name                = pos_name,
                                activation_code         = activation_code,
                                assigned_outlet         = assign_outlet.create_ndb_key(),
                                
                                )
        
        pos_setting.put()
        return pos_setting
    
    @staticmethod
    def update(pos_setting_key, pos_name, assigned_outlet):
        pos_setting                         = POSSetting.fetch(pos_setting_key)
        pos_setting.pos_name                = pos_name
        pos_setting.assigned_outlet         = assigned_outlet.create_ndb_key()
        pos_setting.put()
        
        return pos_setting
    
    @staticmethod
    def get_by_activation_code(activation_code):
        pos_setting = POSSetting.query(POSSetting.activation_code ==activation_code).get()
        return pos_setting
    
    @staticmethod
    def list_by_merchant_account(merchant_acct, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = POSSetting.query(ancestor=merchant_acct.create_ndb_key())
        
        return POSSetting.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_by_merchant_acct(merchant_acct):
        if merchant_acct:
            query = POSSetting.query(ancestor=merchant_acct.create_ndb_key())
        else:
            query = POSSetting.query()
        
        return POSSetting.count_with_condition_query(query)
    
    @staticmethod
    def list_by_merchant_account_and_assigned_outlet(merchant_acct, assigned_outlet, offset=0, limit=conf.PAGINATION_SIZE, start_cursor=None, return_with_cursor=False):
        query = POSSetting.query(ndb.AND(
                        POSSetting.assigned_outlet==assigned_outlet.create_ndb_key()
                        ),ancestor=merchant_acct.create_ndb_key())
        
        return POSSetting.list_all_with_condition_query(query, offset=offset, limit=limit, start_cursor=start_cursor, return_with_cursor=return_with_cursor)
    
    @staticmethod
    def count_by_merchant_account_and_assigned_outlet(merchant_acct, assigned_outlet):
        query = POSSetting.query(ndb.AND(
                        POSSetting.assigned_outlet==assigned_outlet.create_ndb_key()
                        ),ancestor=merchant_acct.create_ndb_key())
        
        return POSSetting.count_with_condition_query(query)
        
    @staticmethod
    def activate(activation_code):
        checking_pos_setting = POSSetting.get_by_activation_code(activation_code)
        if checking_pos_setting:
            checking_pos_setting.activated          = True
            checking_pos_setting.activated_datetime = datetime.utcnow()
            checking_pos_setting.put()
            return True
        else:
            return False
        
    @staticmethod
    def remove_by_activation_code(activation_code):
        checking_pos_setting = POSSetting.get_by_activation_code(activation_code)
        if checking_pos_setting:
            checking_pos_setting.delete()
            return True
        else:
            return False
        
    @property
    def setting(self):
        merchant_acct = MerchantAcct.fetch(self.parent_key)
        return {
                'activation_code'   : self.activation_code,
                'pos_name'          : self.pos_name,
                'company_name'      : merchant_acct.company_name,
                'outlet_key'        : self.assigned_outlet_key,
                'account_id'        : self.parent_key,
                'api_key'           : merchant_acct.api_key,
                'logo_image_url'    : merchant_acct.logo_public_url,
                'account_settings'  : merchant_acct.account_settings,
                }
        
        
class POSCatalogue(BaseNModel,DictModel):
    '''
    merchant_acct as ancestor
    '''
    assigned_catalogue      = ndb.KeyProperty(name="assigned_catalogue", kind=ProductCatalogue)        
    assigned_outlet_list    = ndb.JsonProperty()
    
    is_publish              = ndb.BooleanProperty(default=False)
    
    created_datetime        = ndb.DateTimeProperty(required=True, auto_now_add=True)
    modified_datetime       = ndb.DateTimeProperty(required=False, auto_now=True)
    
    dict_properties = ['assigned_catalogue_key', 'assigned_outlet_list', 'is_publish']
    
    @property
    def assigned_catalogue_key(self):
        return self.assigned_catalogue.urlsafe().decode('utf-8')
    
    @staticmethod
    def list_by_merchant_acct(merchant_acct):
        return POSCatalogue.query(ancestor = merchant_acct.create_ndb_key()).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod
    @model_transactional(desc='POSCatalogue.create')
    def create(assigned_catalogue_key, merchant_acct, assigned_outlet_key_list=[]):
        if assigned_outlet_key_list:
            
            
            assigned_catalogue = ProductCatalogue.fetch(assigned_catalogue_key)
            if assigned_catalogue: 
                
                outlet_catalogue = POSCatalogue(
                                                                parent                  = merchant_acct.create_ndb_key(),
                                                                assigned_catalogue      = assigned_catalogue.create_ndb_key(),
                                                                assigned_outlet_list    = assigned_outlet_key_list,
                                                                )
                
                outlet_catalogue.put()
                
                return outlet_catalogue
                
            else:
                raise Exception('Invalid catalogue data')
                
                
        else:
            raise Exception('Missing assign outlet')    
        
    
    @staticmethod
    @model_transactional(desc='POSCatalogue.udpate')
    def update(pos_assigned_outlet_key, assigned_catalogue_key, assigned_outlet_key_list=[]):
        if is_not_empty(pos_assigned_outlet_key):
            outlet_catalogue = POSCatalogue.fetch(pos_assigned_outlet_key)
            if outlet_catalogue:
                assigned_catalogue = ProductCatalogue.fetch(assigned_catalogue_key)
                if assigned_catalogue:
                    outlet_catalogue.assigned_catalogue    = assigned_catalogue.create_ndb_key()
                    outlet_catalogue.assigned_outlet_list  = assigned_outlet_key_list
                    
                    outlet_catalogue.put()
                    
                    
                else:
                    raise Exception('Invalid catalogue data')
            else:
                raise Exception('Invalid pos assign catalogue data')
        else:
            raise Exception('POS assign catalogue key is empty')
    
    @model_transactional(desc='POSCatalogue.publish')   
    def publish(self):
        self.is_publish          = True
        assigned_catalogue_key  = self.assigned_catalogue.urlsafe().decode('utf-8')
        
        for outlet_key in self.assigned_outlet_list:
            Outlet.assign_catalogue_to_outlet(outlet_key, assigned_catalogue_key)
        
        self.put()
        
    @model_transactional(desc='POSAssignedCatalogue.unpublish')    
    def unpublish(self):
        self.is_publish          = False
        
        for outlet_key in self.assigned_outlet_list:
            Outlet.remove_catalogue_from_outlet(outlet_key)
        
        self.put()
        
class DinningTableSetup(BaseNModel,DictModel):
    name                    = ndb.StringProperty(required=True)
    table_list              = ndb.StringProperty(required=True)
    assigned_outlet_list    = ndb.JsonProperty()
    is_publish              = ndb.BooleanProperty(default=False)
    modified_datetime       = ndb.DateTimeProperty(auto_now=True)
    
    
    dict_properties = ['name', 'table_list', 'assigned_outlet_list', 'is_publish']
    
    @staticmethod
    def create(name, table_list, assigned_outlet_key_list, merchant_acct):
        dinning_table_setup = DinningTableSetup(
                                        parent                  = merchant_acct.create_ndb_key(),
                                        name                    = name, 
                                        is_publish              = False,
                                        table_list              = table_list,
                                        assigned_outlet_list    = assigned_outlet_key_list,
                                        )
        dinning_table_setup.put()
        return dinning_table_setup
    
    @staticmethod
    def update(dinning_table_setup, name, table_list, assigned_outlet_key_list):
        dinning_table_setup.name                    = name
        dinning_table_setup.table_list              = table_list
        dinning_table_setup.assigned_outlet_list    = assigned_outlet_key_list
        dinning_table_setup.is_publish              = False
        dinning_table_setup.put()
    
    @staticmethod    
    def remove(dinning_table_setup):
        dinning_table_setup.delete()
        
    @model_transactional(desc='DinningTableSetup.publish')   
    def publish(self):
        self.is_publish          = True  
          
        for outlet_key in self.assigned_outlet_list:
            Outlet.assign_dinning_table_setup_to_outlet(outlet_key, self.table_list)
        
        self.put()
            
    @model_transactional(desc='DinningTableSetup.unpublish')   
    def unpublish(self):
        self.is_publish          = True  
          
        for outlet_key in self.assigned_outlet_list:
            Outlet.remove_dinning_table_setup_from_outlet(outlet_key)
            
        self.put()         
        
    @staticmethod
    def list_by_merchant_acct(merchant_acct):
        return DinningTableSetup.query(ancestor = merchant_acct.create_ndb_key()).fetch(limit=conf.MAX_FETCH_RECORD)
        
class DinningOption(BaseNModel,DictModel):
    name                    = ndb.StringProperty(required=True)  
    is_archive              = ndb.BooleanProperty(default=False) 
    modified_datetime       = ndb.DateTimeProperty(auto_now=True) 
    archived_datetime       = ndb.DateTimeProperty(required=False) 
    
    dict_properties = ['name','is_archive']
    
    @staticmethod
    def create(name, merchant_acct):
        dinning_option = DinningOption(
                                        parent  = merchant_acct.create_ndb_key(),
                                        name    = name,
                                        )
        dinning_option.put()
        return dinning_option
    
    @staticmethod
    def update(dinning_option, name):
        dinning_option.name       = name
        dinning_option.put()
        
    @staticmethod
    def list_by_merchant_acct(merchant_acct):
        return DinningOption.query(ndb.AND(DinningOption.is_archive==False), ancestor = merchant_acct.create_ndb_key()).fetch(limit=conf.MAX_FETCH_RECORD)
    
    @staticmethod    
    def archive(dinning_option):
        dinning_option.is_archive = True
        dinning_option.archived_datetime = datetime.utcnow()
        dinning_option.put()   
            
        