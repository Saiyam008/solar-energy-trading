from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.order import Order
from models.trade import Trade
from models.contract import Contract
from utils.market_simulator import MarketSimulator
from utils.chart_generator import ChartGenerator

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/buyer')
@login_required
def buyer_dashboard():
    print(f"[DEBUG] Buyer dashboard accessed by: {current_user.username}")
    
    if current_user.user_type != 'buyer':
        return redirect(url_for('dashboard.seller_dashboard'))
    
    market_data = MarketSimulator.get_market_data()
    user_orders = Order.get_user_orders(current_user.id)
    user_trades = Trade.get_user_trades(current_user.id)
    user_contracts = Contract.get_user_contracts(current_user.id)
    
    # Calculate statistics
    total_purchased = sum([t['quantity_mw'] for t in user_trades if t['buyer_id'] == current_user.id])
    total_spent = sum([t['total_amount'] for t in user_trades if t['buyer_id'] == current_user.id])
    avg_price = total_spent / total_purchased if total_purchased > 0 else 0
    
    stats = {
        'total_purchased': round(total_purchased, 2),
        'total_spent': round(total_spent, 2),
        'avg_price': round(avg_price, 2),
        'active_orders': len([o for o in user_orders if o['status'] == 'pending']),
        'active_contracts': len([c for c in user_contracts if c['status'] == 'active'])
    }
    
    return render_template('buyer_dashboard.html', 
                         market_data=market_data,
                         stats=stats,
                         recent_trades=user_trades[:10])

@bp.route('/seller')
@login_required
def seller_dashboard():
    print(f"[DEBUG] Seller dashboard accessed by: {current_user.username}")
    
    if current_user.user_type != 'seller':
        return redirect(url_for('dashboard.buyer_dashboard'))
    
    market_data = MarketSimulator.get_market_data()
    user_orders = Order.get_user_orders(current_user.id)
    user_trades = Trade.get_user_trades(current_user.id)
    user_contracts = Contract.get_user_contracts(current_user.id)
    
    # Calculate statistics
    total_sold = sum([t['quantity_mw'] for t in user_trades if t['seller_id'] == current_user.id])
    total_earned = sum([t['total_amount'] for t in user_trades if t['seller_id'] == current_user.id])
    avg_price = total_earned / total_sold if total_sold > 0 else 0
    
    stats = {
        'total_sold': round(total_sold, 2),
        'total_earned': round(total_earned, 2),
        'avg_price': round(avg_price, 2),
        'active_orders': len([o for o in user_orders if o['status'] == 'pending']),
        'active_contracts': len([c for c in user_contracts if c['status'] == 'active'])
    }
    
    return render_template('seller_dashboard.html', 
                         market_data=market_data,
                         stats=stats,
                         recent_trades=user_trades[:10])

@bp.route('/charts/price')
@login_required
def price_chart():
    chart_json = ChartGenerator.get_price_chart()
    return jsonify({'chart': chart_json})

@bp.route('/charts/volume')
@login_required
def volume_chart():
    chart_json = ChartGenerator.get_volume_chart()
    return jsonify({'chart': chart_json})

@bp.route('/charts/orderbook')
@login_required
def orderbook_chart():
    chart_json = ChartGenerator.get_orderbook_chart()
    return jsonify({'chart': chart_json})
