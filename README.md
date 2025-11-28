# 🎓 Profile Draft - Gamification System

A comprehensive Flask-based gamification profile system with course progress tracking, power-ups, prizes, and professional visualizations.

## 🚀 Getting Started

### 1. **Start the Server**
```bash
cd /Users/dhill/Desktop/Profile_Draft
/opt/homebrew/bin/python3 app.py
```

### 2. **Open in Browser**
Navigate to: **http://localhost:5000/**

### 3. **Explore Features**
See **QUICK_START.md** for interactive walkthroughs

---

## ✨ Features

### 📊 Course Progress Tracking
- Three-unit curriculum with real-time progress
- Color-coded status indicators:
  - 🟢 **Green**: 80%+ (Mastered)
  - 🟠 **Orange**: 50-79% (On Track)
  - 🔴 **Red**: <50% (Needs Work)
- Interactive unit cards
- Professional Chart.js visualization in modal

### ⚡ Power-Ups System
- **2x XP Boost** (150 XP): Double XP for 1 hour
- **Streak Shield** (100 XP): Protect streak for 24 hours
- Active power-up badges
- Automatic expiration tracking

### 🏆 Prize Marketplace
- 6 diverse prizes with varying costs
- Real-time XP validation
- Purchase history tracking
- Responsive grid layout

### 💬 UI Feedback System
- Flash notifications (success & error)
- Auto-dismissing messages (5 seconds)
- Smooth animations
- Mobile-friendly

### 🎨 Customizable Profiles
- Theme options: dark, light, neon, sunset
- Frame styles: default, gold, crystal, rainbow
- Cosmetic endpoints ready for UI integration

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.md** | Interactive guide with examples |
| **IMPLEMENTATION_SUMMARY.md** | Complete feature overview |
| **API_ENDPOINTS.md** | Full endpoint reference |
| **app.py** | Flask backend (300 lines) |
| **templates/profile.html** | HTML template with Chart.js (342 lines) |
| **static/profile.css** | Professional dark theme (722 lines) |

---

## 🎮 Try These Actions

1. **Claim Daily Bonus** - +10 XP
2. **Gamble** - Risk 25 XP to win 50 XP (50/50)
3. **Activate Power-Ups** - Boost your level or protect streak
4. **Redeem Prizes** - Spend XP on rewards
5. **Simulate Progress** - Demo the color-changing system
6. **View Chart** - Modal with professional visualization

---

## 🏗️ Project Structure

```
Profile_Draft/
├── app.py                          # Flask backend
├── requirements.txt                # Python dependencies
├── prizes.json                     # Marketplace data
├── templates/
│   └── profile.html               # Main template with Chart.js
├── static/
│   └── profile.css                # Dark theme styling
├── QUICK_START.md                 # Interactive guide
├── IMPLEMENTATION_SUMMARY.md      # Feature overview
├── API_ENDPOINTS.md               # API reference
└── README.md                      # This file
```

---

## 🔌 API Endpoints

### GET
- `/profile` - Main profile page

### POST
- `/claim-reward` - Daily +10 XP bonus
- `/gamble` - Win 50 or lose 25 XP
- `/redeem-prize/<id>` - Purchase prize
- `/activate-power-up/<type>` - Activate power-up
- `/change-cosmetic/<type>/<value>` - Change theme/frame
- `/update-units` - Simulate progress change
- `/add-badge` - Add peer praise badge

See **API_ENDPOINTS.md** for full reference.

---

## 💾 Data Structure

### User Profile (Session)
```python
{
  "username": "Student",
  "scores": 320,              # XP points
  "streak": 5,                # Days
  "minutes_active": 45,       # Last session
  "sessions": 7,              # Total sessions
  "badges": [...],            # Peer praise
  "course_units": [...],      # Progress tracking
  "power_ups": [...],         # Active boosts
  "cosmetics": {...},         # Theme/frame
  "redeemed_prizes": [...]    # Purchase history
}
```

### Course Units
```python
{
  "name": "Unit 1: Foundations",
  "progress": 65,             # 0-100%
  "color": "orange"           # red/orange/green
}
```

---

## 🎨 Color Scheme

| Use | Color | Hex |
|-----|-------|-----|
| Mastered | Green | #22c55e |
| On Track | Orange | #f59e0b |
| Needs Work | Red | #ef4444 |
| Interactive | Purple | #8b5cf6 |
| Success | Green | #22c55e |
| Error | Red | #ef4444 |

---

## 📈 Gamification Framework

### Three Reward Types (from ideasGamification.md)

**1. Hooked Loop** (Social Recognition)
- Peer praise badges
- Streak sharing
- Class progress rings
- Teacher shoutouts
- Mini leaderboards

**2. Reward of the Hunt** (Discovery)
- Prize marketplace
- Power-ups surprises
- Gamble mechanics
- XP chests

**3. Reward of the Self** (Mastery)
- Progress bars per unit
- Mastery levels (red/orange/green)
- Streak shield protection
- Reflection moments

---

## 🐛 Troubleshooting

**Port already in use?**
```python
# In app.py, change:
app.run(debug=True, port=5001)  # Use 5001 instead
```

**Python not found?**
```bash
which python3
# Use the full path if needed
```

**Session resets on refresh?**
- This is normal (browser session based)
- Data persists during session
- Consider SQLite for persistent storage

---

## 🚀 Next Steps

### Phase 2 (Optional)
- [ ] Connect to persistent database (SQLite/PostgreSQL)
- [ ] Implement team competitions
- [ ] Add AI-powered smart challenges
- [ ] Create weekly leaderboards
- [ ] Build cosmetic marketplace
- [ ] Add streaming/analytics

### Phase 3 (Optional)
- [ ] Implement daily mystery questions
- [ ] Create explore map game mode
- [ ] Add real-time notifications
- [ ] Build mobile app
- [ ] Implement class social features

---

## 💡 Tips & Tricks

### Power-Up Combos
```
1. Activate 2x Boost (150 XP)
2. Claim Daily Bonus (+10 XP, doubled to +20 with boost!)
3. Effect: 170 XP net cost for 20 XP gain
```

### Prize Strategy
- Save for high-value prizes (Game Token 2000 XP)
- Use power-ups strategically
- Track redeemed prizes for achievement metrics

### Progress Tracking
- Click "Simulate Progress" to demo system
- Colors auto-update based on thresholds
- Chart modal shows detailed breakdown

---

## 🔐 Security Notes

- Secret key is hardcoded (⚠️ change for production)
- Session-based auth (upgrade for multi-user)
- No CSRF protection (add Flask-WTF for production)
- Input validation implemented for cosmetics

---

## 📞 Support

See documentation files for:
- **QUICK_START.md** - Getting started guide
- **API_ENDPOINTS.md** - Endpoint reference
- **IMPLEMENTATION_SUMMARY.md** - Feature details

---

## 📄 License

Built with Flask, Chart.js, and modern web standards.

---

**Ready to gamify learning? Start the app and explore! 🚀**
# ProfilePageRW
