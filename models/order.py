from datetime import datetime
from utils.data_handler import DataHandler
import uuid

class Order:
    def __init__(self, order_id, user_id, order_type, quantity_mw, 
                 price_per_mw, status, created_at, executed_at=None, 
                 matched_order_id=None):
        self.order_id = order_id
        self.user_id = user_id
        self.order_type = order_type  # 'buy' or 'sell'
        self.quantity_mw = quantity_mw
        self.price_per_mw = price_per_mw
        self.status = status  # 'pending', 'executed', 'cancelled'
        self.created_at = created_at
        self.executed_at = executed_at
        self.matched_order_id = matched_order_id
    
    @staticmethod
    def create(user_id, order_type, quantity_mw, price_per_mw):
        handler = DataHandler('orders.json')
        orders = handler.load()
        
        order = {
            'order_id': str(uuid.uuid4()),
            'user_id': user_id,
            'order_type': order_type,
            'quantity_mw': float(quantity_mw),
            'price_per_mw': float(price_per_mw),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'executed_at': None,
            'matched_order_id': None
        }
        
        orders.append(order)
        handler.save(orders)
        
        # Try to match order
        Order.match_orders()
        
        return order['order_id']
    
    @staticmethod
    def match_orders():
        """Match buy and sell orders based on price and quantity"""
        handler = DataHandler('orders.json')
        orders = handler.load()
        
        pending_buys = [o for o in orders if o['status'] == 'pending' and o['order_type'] == 'buy']
        pending_sells = [o for o in orders if o['status'] == 'pending' and o['order_type'] == 'sell']
        
        # Sort: buy orders by price (descending), sell orders by price (ascending)
        pending_buys.sort(key=lambda x: x['price_per_mw'], reverse=True)
        pending_sells.sort(key=lambda x: x['price_per_mw'])
        
        trades_made = []
        
        for buy_order in pending_buys:
            for sell_order in pending_sells:
                # Match condition: buy price >= sell price
                if (buy_order['price_per_mw'] >= sell_order['price_per_mw'] and 
                    buy_order['status'] == 'pending' and 
                    sell_order['status'] == 'pending'):
                    
                    # Execute trade at the sell price (lower price benefits buyer)
                    trade_price = sell_order['price_per_mw']
                    trade_quantity = min(buy_order['quantity_mw'], sell_order['quantity_mw'])
                    
                    # Create trade record
                    trade = Order.execute_trade(buy_order, sell_order, trade_quantity, trade_price)
                    trades_made.append(trade)
                    
                    # Update order quantities
                    buy_order['quantity_mw'] -= trade_quantity
                    sell_order['quantity_mw'] -= trade_quantity
                    
                    # Update order status
                    if buy_order['quantity_mw'] == 0:
                        buy_order['status'] = 'executed'
                        buy_order['executed_at'] = datetime.now().isoformat()
                    
                    if sell_order['quantity_mw'] == 0:
                        sell_order['status'] = 'executed'
                        sell_order['executed_at'] = datetime.now().isoformat()
                    
                    break
        
        handler.save(orders)
        return trades_made
    
    @staticmethod
    def execute_trade(buy_order, sell_order, quantity, price):
        """Execute a trade between buyer and seller"""
        from models.user import User
        
        trade_handler = DataHandler('trades.json')
        trades = trade_handler.load()
        
        trade = {
            'trade_id': str(uuid.uuid4()),
            'buy_order_id': buy_order['order_id'],
            'sell_order_id': sell_order['order_id'],
            'buyer_id': buy_order['user_id'],
            'seller_id': sell_order['user_id'],
            'quantity_mw': quantity,
            'price_per_mw': price,
            'total_amount': quantity * price,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        trades.append(trade)
        trade_handler.save(trades)
        
        # Update user balances
        buyer = User.get_by_id(buy_order['user_id'])
        seller = User.get_by_id(sell_order['user_id'])
        
        if buyer and seller:
            buyer.update_balance(-trade['total_amount'])
            seller.update_balance(trade['total_amount'])
        
        return trade
    
    @staticmethod
    def get_user_orders(user_id):
        handler = DataHandler('orders.json')
        orders = handler.load()
        return [o for o in orders if o['user_id'] == user_id]
    
    @staticmethod
    def get_pending_orders():
        handler = DataHandler('orders.json')
        orders = handler.load()
        return [o for o in orders if o['status'] == 'pending']
    
    @staticmethod
    def cancel_order(order_id, user_id):
        handler = DataHandler('orders.json')
        orders = handler.load()
        
        for order in orders:
            if order['order_id'] == order_id and order['user_id'] == user_id:
                if order['status'] == 'pending':
                    order['status'] = 'cancelled'
                    handler.save(orders)
                    return True
        return False
