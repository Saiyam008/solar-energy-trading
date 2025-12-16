from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models.order import Order
from models.trade import Trade
from utils.market_simulator import MarketSimulator

bp = Blueprint('trading', __name__, url_prefix='/trading')

@bp.route('/')
@login_required
def trading_page():
    market_data = MarketSimulator.get_market_data()
    pending_orders = Order.get_pending_orders()
    recent_trades = Trade.get_recent_trades(20)
    user_orders = Order.get_user_orders(current_user.id)
    
    return render_template('trading.html',
                         market_data=market_data,
                         pending_orders=pending_orders,
                         recent_trades=recent_trades,
                         user_orders=user_orders)

@bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    try:
        order_type = request.form.get('order_type')
        quantity = float(request.form.get('quantity'))
        price = float(request.form.get('price'))
        
        # Validate order
        if quantity <= 0 or price <= 0:
            return jsonify({'success': False, 'message': 'Invalid quantity or price'})
        
        # Check user type matches order type
        if current_user.user_type == 'buyer' and order_type != 'buy':
            return jsonify({'success': False, 'message': 'Buyers can only place buy orders'})
        
        if current_user.user_type == 'seller' and order_type != 'sell':
            return jsonify({'success': False, 'message': 'Sellers can only place sell orders'})
        
        # Check balance for buyers
        if order_type == 'buy':
            required_amount = quantity * price
            if current_user.balance < required_amount:
                return jsonify({'success': False, 'message': 'Insufficient balance'})
        
        # Check capacity for sellers
        if order_type == 'sell' and quantity > current_user.capacity_mw:
            return jsonify({'success': False, 'message': 'Quantity exceeds your capacity'})
        
        # Create order
        order_id = Order.create(current_user.id, order_type, quantity, price)
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order_id': order_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/cancel_order/<order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    success = Order.cancel_order(order_id, current_user.id)
    
    if success:
        return jsonify({'success': True, 'message': 'Order cancelled successfully'})
    else:
        return jsonify({'success': False, 'message': 'Unable to cancel order'})

@bp.route('/market_data')
@login_required
def get_market_data():
    market_data = MarketSimulator.update_market_price()
    pending_orders = Order.get_pending_orders()
    recent_trades = Trade.get_recent_trades(10)
    
    return jsonify({
        'market_data': market_data,
        'pending_orders': pending_orders,
        'recent_trades': recent_trades
    })
