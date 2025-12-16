import plotly.graph_objs as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from utils.market_simulator import MarketSimulator
from models.trade import Trade

class ChartGenerator:
    @staticmethod
    def get_price_chart():
        """Generate price history chart"""
        history = MarketSimulator.get_price_history(30)
        
        if not history:
            return None
        
        dates = [h['date'] for h in history]
        prices = [h['price'] for h in history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=prices,
            mode='lines+markers',
            name='Price (Rs/MW)',
            line=dict(color='#00D9FF', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='Solar Energy Price Trend (Last 30 Days)',
            xaxis_title='Date',
            yaxis_title='Price (Rs/MW)',
            template='plotly_dark',
            hovermode='x unified',
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    @staticmethod
    def get_volume_chart():
        """Generate volume chart"""
        history = MarketSimulator.get_price_history(30)
        
        if not history:
            return None
        
        dates = [h['date'] for h in history]
        volumes = [h['volume'] for h in history]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates, y=volumes,
            name='Volume (MW)',
            marker=dict(color='#00FF88')
        ))
        
        fig.update_layout(
            title='Trading Volume (Last 30 Days)',
            xaxis_title='Date',
            yaxis_title='Volume (MW)',
            template='plotly_dark',
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
    
    @staticmethod
    def get_orderbook_chart():
        """Generate order book depth chart"""
        from models.order import Order
        
        pending_orders = Order.get_pending_orders()
        
        buy_orders = [o for o in pending_orders if o['order_type'] == 'buy']
        sell_orders = [o for o in pending_orders if o['order_type'] == 'sell']
        
        # Aggregate by price
        buy_depth = {}
        sell_depth = {}
        
        for order in buy_orders:
            price = order['price_per_mw']
            buy_depth[price] = buy_depth.get(price, 0) + order['quantity_mw']
        
        for order in sell_orders:
            price = order['price_per_mw']
            sell_depth[price] = sell_depth.get(price, 0) + order['quantity_mw']
        
        fig = go.Figure()
        
        if buy_depth:
            buy_prices = sorted(buy_depth.keys(), reverse=True)
            buy_volumes = [buy_depth[p] for p in buy_prices]
            fig.add_trace(go.Bar(
                x=buy_prices, y=buy_volumes,
                name='Buy Orders',
                marker=dict(color='#00FF88')
            ))
        
        if sell_depth:
            sell_prices = sorted(sell_depth.keys())
            sell_volumes = [sell_depth[p] for p in sell_prices]
            fig.add_trace(go.Bar(
                x=sell_prices, y=sell_volumes,
                name='Sell Orders',
                marker=dict(color='#FF4444')
            ))
        
        fig.update_layout(
            title='Order Book Depth',
            xaxis_title='Price (Rs/MW)',
            yaxis_title='Quantity (MW)',
            template='plotly_dark',
            barmode='group',
            height=400
        )
        
        return json.dumps(fig, cls=PlotlyJSONEncoder)
