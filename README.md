# Simple Garba Kiosk 🎪

## The Cleanest, Simplest Version! ✨

This is a **SUPER CLEAN** Garba ticket booking system with minimal files:

- 📁 **Only 3 essential files**
- 🚀 **Zero complexity**
- 🎯 **Perfect for beginners**

## Files Structure 📁

```
📁 Project (CLEAN!):
├── basic_kiosk.py          # 🎯 Main app (run this!)
├── templates/
│   └── basic_kiosk.html    # 🎨 Single HTML file
├── requirements.txt        # 📦 Only Flask needed
└── README.md              # 📖 This file
```

**That's it! No clutter, no confusion!** 🎉

## Quick Start (30 seconds!) ⚡

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Run the app
```bash
python basic_kiosk.py
```

### Step 3: Open browser
- **Kiosk**: http://localhost:5000/
- **Admin**: http://localhost:5000/admin

**Done!** 🚀

## Features ⚡

### Customer Kiosk:
- 🏠 **Events**: Browse available events
- 🎫 **Book**: Simple booking form  
- ✅ **Check In**: Enter booking ID to check in
- 🔍 **Lookup**: Find booking details

### Admin Dashboard:
- 📊 **Statistics**: Events, bookings, revenue
- 📈 **Real-time data**: Auto-refreshes every 30 seconds
- 🎫 **Event management**: See availability
- 👥 **Booking overview**: Check-in status

## Sample Events 🎭

Pre-loaded with 2 events:
1. **Navratri Night 1** - Sept 15, 2025 - ₹250
2. **Dandiya Special** - Sept 16, 2025 - ₹300

## How It Works 🔧

- ✅ **In-memory storage** (no database complexity)
- ✅ **Simple booking flow**: Choose event → Enter details → Get ID
- ✅ **Easy check-in**: Just enter booking ID
- ✅ **Admin oversight**: Monitor everything in real-time

## Perfect For 🎯

- ✅ **Learning Python/Flask**
- ✅ **Quick demos**  
- ✅ **School projects**
- ✅ **Prototyping**
- ✅ **Understanding web apps**

## Customization 🎨

### Add More Events:
Edit the `events` list in `basic_kiosk.py`:
```python
events = [
    {
        "id": "3",
        "name": "Your New Event",
        "date": "2025-09-20", 
        "time": "8:00 PM",
        "venue": "Your Venue",
        "price": 500,
        "available": 100
    }
]
```

### Change Styling:
Edit the CSS in `templates/basic_kiosk.html`

---

**🎉 Enjoy your super clean Garba kiosk!**

*Minimal files, maximum functionality!* ⚡

## Need Help? 🤔

- **Can't run?** Make sure Python and Flask are installed
- **Port in use?** Change `port=5000` to `port=5001` in `basic_kiosk.py`
- **Admin not working?** Try both `/admin` and `/admin/`

**This is as simple as it gets!** 🚀
