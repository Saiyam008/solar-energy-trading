// Calculate total amount
document.getElementById('quantity').addEventListener('input', calculateTotal);
document.getElementById('price').addEventListener('input', calculateTotal);

function calculateTotal() {
    const quantity = parseFloat(document.getElementById('quantity').value) || 0;
    const price = parseFloat(document.getElementById('price').value) || 0;
    const total = quantity * price;
    document.getElementById('totalAmount').textContent = '₹' + total.toFixed(2);
}

// Handle order form submission
document.getElementById('orderForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/trading/place_order', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error);
    });
});

// Cancel order function
function cancelOrder(orderId) {
    if (confirm('Are you sure you want to cancel this order?')) {
        fetch(`/trading/cancel_order/${orderId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert('Error: ' + data.message);
            }
        });
    }
}

// Auto-refresh market data every 5 seconds
setInterval(function() {
    fetch('/trading/market_data')
        .then(response => response.json())
        .then(data => {
            // Update current price with flash effect
            const priceElement = document.getElementById('currentPrice');
            const oldPrice = parseFloat(priceElement.textContent.replace('₹', ''));
            const newPrice = data.market_data.current_price;
            
            if (oldPrice !== newPrice) {
                priceElement.textContent = '₹' + newPrice.toFixed(2);
                priceElement.classList.add('price-flash');
                setTimeout(() => priceElement.classList.remove('price-flash'), 1000);
            }
            
            // Update order book
            updateOrderBook(data.pending_orders);
            
            // Update recent trades
            updateRecentTrades(data.recent_trades);
        })
        .catch(error => console.error('Error fetching market data:', error));
}, 5000);

function updateOrderBook(orders) {
    const tbody = document.getElementById('orderBookTable');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    orders.forEach(order => {
        const row = tbody.insertRow();
        row.className = order.order_type === 'buy' ? 'table-success' : 'table-danger';
        
        row.innerHTML = `
            <td><span class="badge bg-${order.order_type === 'buy' ? 'success' : 'danger'}">${order.order_type.toUpperCase()}</span></td>
            <td>${order.quantity_mw.toFixed(2)}</td>
            <td>₹${order.price_per_mw.toFixed(2)}</td>
        `;
    });
}

function updateRecentTrades(trades) {
    const tbody = document.getElementById('recentTradesTable');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    trades.slice(0, 20).forEach(trade => {
        const row = tbody.insertRow();
        const time = trade.timestamp.substring(11, 16);
        
        row.innerHTML = `
            <td>${time}</td>
            <td>${trade.quantity_mw.toFixed(1)}</td>
            <td>₹${trade.price_per_mw.toFixed(2)}</td>
        `;
    });
}
