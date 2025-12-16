import random
from datetime import datetime, timedelta
from utils.data_handler import DataHandler

class MarketSimulator:
    @staticmethod
    def update_market_price():
        """Simulate market price movements"""
        handler = DataHandler('market_data.json')
        data = handler.load()
        
        if not data:
            data = {
                'current_price': 9.0,
                'volume_today': 0,
                'high_24h': 9.0,
                'low_24h': 9.0
            }
        
        # Simulate price movement (random walk with mean reversion)
        change = random.uniform(-0.2, 0.2)
        new_price = data.get('current_price', 9.0) + change
        
        # Keep price within realistic bounds (Rs 7-11)
        new_price = max(7.0, min(11.0, new_price))
        
        data['current_price'] = round(new_price, 2)
        data['last_updated'] = datetime.now().isoformat()
        data['high_24h'] = max(data.get('high_24h', new_price), new_price)
        data['low_24h'] = min(data.get('low_24h', new_price), new_price)
        
        handler.save(data)
        return data
    
    @staticmethod
    def get_market_data():
        handler = DataHandler('market_data.json')
        data = handler.load()
        if not data:
            return MarketSimulator.update_market_price()
        return data
    
    @staticmethod
    def get_price_history(days=30):
        """Generate historical price data"""
        trades_handler = DataHandler('trades.json')
        trades = trades_handler.load()
        
        # Group trades by date and calculate average price
        price_history = {}
        for trade in trades:
            date = trade['timestamp'][:10]  # Get date part
            if date not in price_history:
                price_history[date] = []
            price_history[date].append(trade['price_per_mw'])
        
        # Calculate daily averages
        history = []
        for date, prices in sorted(price_history.items()):
            history.append({
                'date': date,
                'price': round(sum(prices) / len(prices), 2),
                'volume': sum([t['quantity_mw'] for t in trades if t['timestamp'][:10] == date])
            })
        
        return history[-days:]
