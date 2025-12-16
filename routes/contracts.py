from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from models.contract import Contract
from models.user import User

bp = Blueprint('contracts', __name__, url_prefix='/contracts')

@bp.route('/')
@login_required
def contracts_page():
    user_contracts = Contract.get_user_contracts(current_user.id)
    all_users = []
    
    # Get list of potential trading partners
    from utils.data_handler import DataHandler
    handler = DataHandler('users.json')
    users = handler.load()
    
    if current_user.user_type == 'buyer':
        all_users = [u for u in users if u['user_type'] == 'seller']
    else:
        all_users = [u for u in users if u['user_type'] == 'buyer']
    
    return render_template('contracts.html',
                         user_contracts=user_contracts,
                         all_users=all_users)

@bp.route('/create', methods=['POST'])
@login_required
def create_contract():
    try:
        partner_id = request.form.get('partner_id')
        quantity = float(request.form.get('quantity'))
        price = float(request.form.get('price'))
        duration = int(request.form.get('duration'))
        start_date = request.form.get('start_date')
        
        if current_user.user_type == 'buyer':
            buyer_id = current_user.id
            seller_id = partner_id
        else:
            buyer_id = partner_id
            seller_id = current_user.id
        
        contract_id = Contract.create(buyer_id, seller_id, quantity, price, duration, start_date)
        
        return jsonify({
            'success': True,
            'message': 'Contract proposal created successfully. Waiting for approval.',
            'contract_id': contract_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@bp.route('/approve/<contract_id>', methods=['POST'])
@login_required
def approve_contract(contract_id):
    success = Contract.approve_contract(contract_id, current_user.id)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Contract approved and government notified'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Unable to approve contract'
        })
