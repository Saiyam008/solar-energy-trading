---
title: Solar Energy Trading Platform
emoji: ☀️
colorFrom: yellow
colorTo: red
sdk: docker
pinned: false
license: mit
---

# ☀️ Solar Energy Trading Platform

Peer-to-Peer renewable energy marketplace for India, compliant with CERC regulations.

## Features

- 🔄 **Real-time Trading**: Live order matching and execution
- 📊 **Interactive Charts**: Price trends, volume analysis, market depth
- 🤝 **P2P Contracts**: Direct bilateral agreements between buyers and sellers
- 💰 **Cost Savings**: Trade at ₹9/MW instead of government rates (₹7-11/MW)
- 📝 **Government Compliant**: All contracts are government-notified

## Demo Login Credentials

### Buyer Account
- **Username:** `buyer_demo`
- **Password:** `buyer123`
- **Company:** Gujarat Textile Mills (50 MW capacity)

### Seller Account
- **Username:** `seller_demo`
- **Password:** `seller123`
- **Company:** Solar Power Gujarat Ltd (500 MW capacity)

## How It Works

1. **Login** with buyer or seller credentials
2. **View Dashboard** to see market overview and statistics
3. **Trade** on the live trading platform with order book and charts
4. **Create Contracts** for long-term P2P energy agreements
5. **Track** all your orders, trades, and contracts

## Technical Stack

- **Backend:** Flask, Python 3.9
- **Data Storage:** JSON-based (file system)
- **Charts:** Plotly.js
- **UI:** Bootstrap 5, Font Awesome

## Regulatory Compliance

Based on:
- Central Electricity Regulatory Commission (CERC) guidelines
- Karnataka P2P Solar Trading regulations
- Open Access trading norms (NOAR)

## Future Enhancements

For production deployment:
- Payment gateway integration (Razorpay/Paytm)
- CERC/SLDC API integration
- Blockchain for transaction transparency
- Real-time market data from IEX India
- SMS/Email notifications

---

**Note:** This is a demonstration platform with dummy data. All transactions are simulated.
