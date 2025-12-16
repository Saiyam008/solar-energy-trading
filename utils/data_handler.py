import json
import os
from datetime import datetime, timedelta
import random

class DataHandler:
    def __init__(self, filename):
        self.data_dir = 'data'
        self.filepath = os.path.join(self.data_dir, filename)
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return []
    
    def save(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

def initialize_data():
    """Initialize all data files with sample data"""
    
    # Initialize users
    users_handler = DataHandler('users.json')
    if not os.path.exists(users_handler.filepath):
        users = [
            {
                'id': 'buyer1',
                'username': 'buyer_demo',
                'password': 'buyer123',
                'user_type': 'buyer',
                'company_name': 'Gujarat Textile Mills',
                'capacity_mw': 50,
                'location': 'Ahmedabad, Gujarat',
                'balance': 5000000.0,
                'email': 'buyer@gtm.com'
            },
            {
                'id': 'seller1',
                'username': 'seller_demo',
                'password': 'seller123',
                'user_type': 'seller',
                'company_name': 'Solar Power Gujarat Ltd',
                'capacity_mw': 500,
                'location': 'Gandhinagar, Gujarat',
                'balance': 10000000.0,
                'email': 'seller@spgl.com'
            },
            {
                'id': 'seller2',
                'username': 'green_energy',
                'password': 'green123',
                'user_type': 'seller',
                'company_name': 'Green Energy Solutions',
                'capacity_mw': 300,
                'location': 'Pune, Maharashtra',
                'balance': 8000000.0,
                'email': 'contact@greenenergy.com'
            },
            {
                'id': 'buyer2',
                'username': 'pharma_buyer',
                'password': 'pharma123',
                'user_type': 'buyer',
                'company_name': 'Pharma Industries Ltd',
                'capacity_mw': 30,
                'location': 'Hyderabad, Telangana',
                'balance': 3000000.0,
                'email': 'procurement@pharma.com'
            }
        ]
        users_handler.save(users)
    
    # Initialize orders
    orders_handler = DataHandler('orders.json')
    if not os.path.exists(orders_handler.filepath):
        orders_handler.save([])
    
    # Initialize trades with historical data
    trades_handler = DataHandler('trades.json')
    if not os.path.exists(trades_handler.filepath):
        trades = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(100):
            trade_time = base_time + timedelta(hours=i*6)
            trades.append({
                'trade_id': f'trade_{i}',
                'buy_order_id': f'order_b_{i}',
                'sell_order_id': f'order_s_{i}',
                'buyer_id': 'buyer1' if i % 2 == 0 else 'buyer2',
                'seller_id': 'seller1' if i % 3 == 0 else 'seller2',
                'quantity_mw': random.uniform(5, 50),
                'price_per_mw': random.uniform(7.5, 10.5),
                'total_amount': 0,  # Will be calculated
                'timestamp': trade_time.isoformat(),
                'status': 'completed'
            })
            trades[-1]['total_amount'] = trades[-1]['quantity_mw'] * trades[-1]['price_per_mw']
        
        trades_handler.save(trades)
    
    # Initialize contracts
    contracts_handler = DataHandler('contracts.json')
    if not os.path.exists(contracts_handler.filepath):
        contracts = [
            {
                'contract_id': 'contract_1',
                'buyer_id': 'buyer1',
                'seller_id': 'seller1',
                'quantity_mw': 100,
                'price_per_mw': 9.0,
                'duration_months': 12,
                'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
                'created_at': datetime.now().isoformat(),
                'status': 'active',
                'government_notified': True
            }
        ]
        contracts_handler.save(contracts)
    
    # Initialize market data
    market_handler = DataHandler('market_data.json')
    if not os.path.exists(market_handler.filepath):
        market_data = {
            'current_price': 9.2,
            'last_updated': datetime.now().isoformat(),
            'volume_today': 1250.5,
            'high_24h': 10.1,
            'low_24h': 8.9,
            'change_24h': 0.3
        }
        market_handler.save(market_data)
