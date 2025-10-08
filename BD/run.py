from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

events = [
    {
        "id": "1",
        "name": "Navratri Night 1",
        "date": "2025-09-15",
        "time": "7:00 PM",
        "venue": "Community Hall",
        "price": 250,
        "available": 50
    },
    {
        "id": "2", 
        "name": "Dandiya Special",
        "date": "2025-09-16",
        "time": "7:30 PM",
        "venue": "City Center",
        "price": 300,
        "available": 50
    }
]

bookings = []

@app.route('/')
def home():
    return render_template('basic_kiosk.html')

@app.route('/api/events')
def get_events():
    return jsonify({"success": True, "events": events})

@app.route('/api/book', methods=['POST'])
def book_ticket():
    data = request.get_json()
    
    event = next((e for e in events if e["id"] == data["event_id"]), None)
    if not event:
        return jsonify({"success": False, "message": "Event not found"})

    tickets_requested = data["tickets"]
    tickets_available = event["available"]
    
    if tickets_available < tickets_requested:
        if tickets_available == 0:
            return jsonify({
                "success": False, 
                "message": f"Sorry! This event is SOLD OUT. No tickets available.",
                "available": tickets_available
            })
        else:
            return jsonify({
                "success": False, 
                "message": f"Not enough tickets! You requested {tickets_requested} tickets, but only {tickets_available} tickets are available.",
                "available": tickets_available
            })

    booking_id = f"GB{datetime.now().strftime('%m%d')}{len(bookings)+1:03d}"
    booking = {
        "id": booking_id,
        "event_name": event["name"],
        "event_date": event["date"],
        "customer_name": data["name"],
        "customer_phone": data["phone"],
        "tickets": data["tickets"],
        "total": event["price"] * data["tickets"],
        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "checked_in": False
    }
    
    bookings.append(booking)
    event["available"] -= data["tickets"]
    
    return jsonify({
        "success": True, 
        "booking": booking,
        "remaining_tickets": event["available"]
    })

@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.get_json()
    booking_id = data.get("booking_id")
    
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if not booking:
        return jsonify({"success": False, "message": "Booking not found"})
    
    if booking["checked_in"]:
        return jsonify({"success": False, "message": "Already checked in"})
    
    booking["checked_in"] = True
    booking["checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({"success": True, "booking": booking})

@app.route('/api/lookup/<booking_id>')
def lookup_booking(booking_id):
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if not booking:
        return jsonify({"success": False, "message": "Booking not found"})
    
    return jsonify({"success": True, "booking": booking})

@app.route('/admin')
@app.route('/admin/')
def admin():
   
    total_tickets_sold = sum(booking["tickets"] for booking in bookings)
    total_revenue = sum(booking["total"] for booking in bookings)
    checked_in_count = sum(1 for booking in bookings if booking["checked_in"])

    avg_tickets_per_booking = (total_tickets_sold / len(bookings)) if bookings else 0
    avg_revenue_per_booking = (total_revenue / len(bookings)) if bookings else 0
    max_tickets_in_booking = max((booking["tickets"] for booking in bookings), default=0)

    revenue_by_event = {}
    for event in events:
        revenue_by_event[event["id"]] = {"name": event["name"], "tickets_sold": 0, "revenue": 0}
    for booking in bookings:

        for eid, info in revenue_by_event.items():
            if info["name"] == booking["event_name"]:
                info["tickets_sold"] += booking["tickets"]
                info["revenue"] += booking["total"]
                break
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Admin Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #ff6b35;
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.2em;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #ff6b35, #f7931e);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            .section {{
                margin: 30px 0;
            }}
            .section h2 {{
                color: #ff6b35;
                border-bottom: 2px solid #ff6b35;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .item {{
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #ff6b35;
            }}
            .status-pending {{ color: #856404; background: #fff3cd; }}
            .status-checked {{ color: #155724; background: #d4edda; }}
            .nav-links {{
                text-align: center;
                margin-top: 30px;
            }}
            .nav-links a {{
                display: inline-block;
                padding: 12px 25px;
                background: #ff6b35;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                margin: 0 10px;
                font-weight: bold;
                transition: all 0.3s;
            }}
            .nav-links a:hover {{
                background: #e55a2b;
                transform: translateY(-2px);
            }}
            .refresh-btn {{
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
                margin-left: 10px;
            }}
            .refresh-btn:hover {{
                background: #218838;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎪 Simple Admin Dashboard</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{len(events)}</div>
                    <div class="stat-label">Total Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(bookings)}</div>
                    <div class="stat-label">Total Bookings</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{total_tickets_sold}</div>
                    <div class="stat-label">Tickets Sold</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">₹{total_revenue}</div>
                    <div class="stat-label">Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{checked_in_count}</div>
                    <div class="stat-label">Checked In</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📅 Events ({len(events)})</h2>
    """
    
    for event in events:
        sold = event["available"] if "original_capacity" not in event else (event.get("original_capacity", 50) - event["available"])
        html += f"""
                <div class="item">
                    <strong>{event['name']}</strong><br>
                    📅 {event['date']} at {event['time']}<br>
                    📍 {event['venue']}<br>
                    💰 ₹{event['price']} per ticket<br>
                    🎫 Available: {event['available']} tickets
                </div>
        """
    
    html += f"""
            </div>
            
            <div class="section">
                <h2>🎫 Bookings ({len(bookings)})</h2>
    """
    
    if bookings:
        for booking in bookings:
            status_class = "status-checked" if booking["checked_in"] else "status-pending"
            status_text = "✅ Checked In" if booking["checked_in"] else "⏳ Pending Check-in"
            checkin_info = f"<br>🕐 Checked in: {booking['checkin_time']}" if booking["checked_in"] else ""
            
            html += f"""
                <div class="item {status_class}">
                    <strong>#{booking['id']}</strong> - {status_text}<br>
                    👤 {booking['customer_name']} ({booking['customer_phone']})<br>
                    🎭 {booking['event_name']} on {booking['event_date']}<br>
                    🎫 {booking['tickets']} tickets - Total: ₹{booking['total']}<br>
                    📅 Booked: {booking['booked_at']}{checkin_info}
                </div>
            """
    else:
        html += '<div class="item">No bookings yet</div>'
    
    html += f"""
            </div>
            
            <div class="nav-links">
                <a href="/">🏠 Back to Kiosk</a>
                <button class="refresh-btn" onclick="window.location.reload()">🔄 Refresh</button>
            </div>
        </div>
        
        <script>
            // Auto-refresh every 30 seconds
            setTimeout(() => {{
                window.location.reload();
            }}, 30000);
        </script>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎪 SUPER SIMPLE GARBA KIOSK")
    print("="*50)
    print("🚀 Kiosk: http://localhost:5000/")
    print("🔧 Admin: http://localhost:5000/admin")
    print("="*50)
    print("✨ No database needed!")
    print("📁 Everything in one file!")
    print("="*50)
    
    app.run(debug=True, port=5000)
