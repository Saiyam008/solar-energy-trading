from flask_login import UserMixin
from utils.data_handler import DataHandler

class User(UserMixin):
    def __init__(self, user_id, username, password, user_type, company_name, 
                 capacity_mw, location, balance, email):
        self.id = user_id
        self.username = username
        self.password = password
        self.user_type = user_type  # 'buyer' or 'seller'
        self.company_name = company_name
        self.capacity_mw = capacity_mw
        self.location = location
        self.balance = balance
        self.email = email
    
    @staticmethod
    def get_by_id(user_id):
        handler = DataHandler('users.json')
        users = handler.load()
        
        for user in users:
            if user['id'] == user_id:
                return User(
                    user['id'], user['username'], user['password'],
                    user['user_type'], user['company_name'], 
                    user['capacity_mw'], user['location'], 
                    user['balance'], user['email']
                )  # FIXED: Added closing parenthesis
        return None
    
    @staticmethod
    def authenticate(username, password):
        handler = DataHandler('users.json')
        users = handler.load()
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                return User(
                    user['id'], user['username'], user['password'],
                    user['user_type'], user['company_name'], 
                    user['capacity_mw'], user['location'], 
                    user['balance'], user['email']
                )  # FIXED: Added closing parenthesis
        return None
    
    def update_balance(self, amount):
        handler = DataHandler('users.json')
        users = handler.load()
        
        for user in users:
            if user['id'] == self.id:
                user['balance'] += amount
                self.balance = user['balance']
                break
        
        handler.save(users)
        return self.balance
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type,
            'company_name': self.company_name,
            'capacity_mw': self.capacity_mw,
            'location': self.location,
            'balance': self.balance,
            'email': self.email
        }  # FIXED: Added closing brace
