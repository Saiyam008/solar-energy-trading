from utils.data_handler import DataHandler

class Trade:
    @staticmethod
    def get_all_trades():
        handler = DataHandler('trades.json')
        return handler.load()
    
    @staticmethod
    def get_user_trades(user_id):
        handler = DataHandler('trades.json')
        trades = handler.load()
        return [t for t in trades if t['buyer_id'] == user_id or t['seller_id'] == user_id]
    
    @staticmethod
    def get_recent_trades(limit=50):
        handler = DataHandler('trades.json')
        trades = handler.load()
        trades.sort(key=lambda x: x['timestamp'], reverse=True)
        return trades[:limit]
