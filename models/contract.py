from datetime import datetime
from utils.data_handler import DataHandler
import uuid

class Contract:
    @staticmethod
    def create(buyer_id, seller_id, quantity_mw, price_per_mw, 
               duration_months, start_date):
        handler = DataHandler('contracts.json')
        contracts = handler.load()
        
        contract = {
            'contract_id': str(uuid.uuid4()),
            'buyer_id': buyer_id,
            'seller_id': seller_id,
            'quantity_mw': float(quantity_mw),
            'price_per_mw': float(price_per_mw),
            'duration_months': int(duration_months),
            'start_date': start_date,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',  # pending, active, completed, cancelled
            'government_notified': False
        }
        
        contracts.append(contract)
        handler.save(contracts)
        
        return contract['contract_id']
    
    @staticmethod
    def get_user_contracts(user_id):
        handler = DataHandler('contracts.json')
        contracts = handler.load()
        return [c for c in contracts if c['buyer_id'] == user_id or c['seller_id'] == user_id]
    
    @staticmethod
    def approve_contract(contract_id, user_id):
        handler = DataHandler('contracts.json')
        contracts = handler.load()
        
        for contract in contracts:
            if contract['contract_id'] == contract_id:
                if contract['seller_id'] == user_id and contract['status'] == 'pending':
                    contract['status'] = 'active'
                    contract['government_notified'] = True
                    handler.save(contracts)
                    return True
        return False
    
    @staticmethod
    def get_all_contracts():
        handler = DataHandler('contracts.json')
        return handler.load()
