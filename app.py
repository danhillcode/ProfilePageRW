from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, request, session, url_for, flash


app = Flask(__name__)
# A secret key is needed to use sessions.
app.secret_key = "a-secret-key-that-you-should-change"


@dataclass
class UserProfile:
  username: str
  scores: int  # total XP
  streak: int  # days in a row
  minutes_active: int  # recent focused minutes
  sessions: int  # total serious revision sessions
  badges: list = None  # Peer praise badges
  course_units: list = None  # Three units with progress percentage
  power_ups: list = None  # Active power-ups: [{"type": "2x_boost", "expires": timestamp}]
  cosmetics: dict = None  # Owned cosmetics: {"themes": [...], "frames": [...]}
  redeemed_prizes: list = None  # Track redeemed prizes

  def __post_init__(self):
    if self.badges is None:
      self.badges = []
    if self.course_units is None:
      self.course_units = [
        {"name": "Unit 1: Foundations", "progress": 65, "color": "orange"},
        {"name": "Unit 2: Advanced", "progress": 45, "color": "red"},
        {"name": "Unit 3: Mastery", "progress": 85, "color": "green"}
      ]
    if self.power_ups is None:
      self.power_ups = []
    if self.cosmetics is None:
      self.cosmetics = {"theme": "dark", "frame": "default"}
    if self.redeemed_prizes is None:
      self.redeemed_prizes = []


def get_active_power_ups(power_ups: list) -> list:
  """Return only non-expired power-ups."""
  now = datetime.now().timestamp()
  return [p for p in power_ups if p.get("expires", 0) > now]


def calculate_level(scores: int, power_ups: list = None) -> dict:
  """Very simple level system based on XP."""
  safe_scores = max(0, int(scores))

  # Check for active 2x boost
  has_2x_boost = False
  if power_ups:
    active_ups = get_active_power_ups(power_ups)
    has_2x_boost = any(p.get("type") == "2x_boost" for p in active_ups)

  display_scores = safe_scores * 2 if has_2x_boost else safe_scores
  level = display_scores // 100 + 1
  xp_in_level = display_scores % 100
  xp_to_next = 100 - xp_in_level if xp_in_level < 100 else 0

  return {
    "level": level,
    "xp_in_level": xp_in_level,
    "xp_to_next": xp_to_next,
    "progress": xp_in_level,
    "has_2x_boost": has_2x_boost,
  }


def format_minutes(minutes: int) -> str:
  """Turn raw minutes into a friendly label."""
  minutes = max(0, int(minutes))
  if minutes >= 60:
    hours = minutes // 60
    rest = minutes % 60
    if rest == 0:
      return f"{hours} h"
    return f"{hours} h {rest} min"
  return f"{minutes} min"


def load_prizes() -> list:
  """Load prizes from JSON file."""
  prizes_path = Path(__file__).parent / "prizes.json"
  with open(prizes_path) as f:
    return json.load(f)


@app.route("/")
def index():
  """Redirect root to profile."""
  return redirect(url_for("profile"))


@app.route("/profile")
def profile() -> str:
  # If user data is not in the session, initialize it.
  if "user" not in session:
    user_profile = UserProfile(
      username="Student",
      scores=320,
      streak=5,
      minutes_active=45,
      sessions=7,
    )
    session["user"] = asdict(user_profile)

  user = UserProfile(**session["user"])
  level_info = calculate_level(user.scores, user.power_ups)

  streak_goal = 7
  time_goal_minutes = 300  # e.g. 5 hours per week
  sessions_goal = user.sessions + 5

  streak_progress = min(100, int(user.streak / streak_goal * 100))
  time_progress = min(100, int(user.minutes_active / time_goal_minutes * 100))
  sessions_progress = min(100, int(user.sessions / sessions_goal * 100))

  prizes = load_prizes()
  active_power_ups = get_active_power_ups(user.power_ups)

  return render_template(
    "profile.html",
    user=user,
    level_info=level_info,
    streak_goal=streak_goal,
    time_goal_minutes=time_goal_minutes,
    sessions_goal=sessions_goal,
    streak_progress=streak_progress,
    time_progress=time_progress,
    sessions_progress=sessions_progress,
    formatted_minutes=format_minutes(user.minutes_active),
    prizes=prizes,
    active_power_ups=active_power_ups,
  )


@app.route("/claim-reward", methods=["POST"])
def claim_reward():
  """Simple reward for daily activity."""
  if "user" in session:
    session["user"]["scores"] += 10
    session.modified = True
  return redirect(url_for("profile"))


@app.route("/gamble", methods=["POST"])
def gamble():
  """50/50 chance to win 50 XP or lose 25 XP."""
  if "user" in session:
    if random.random() > 0.5:
      session["user"]["scores"] += 50
    else:
      session["user"]["scores"] -= 25
    session.modified = True
  return redirect(url_for("profile"))


@app.route("/redeem-prize/<int:prize_id>", methods=["POST"])
def redeem_prize(prize_id):
  """Redeem XP for a specific prize from the marketplace."""
  prizes = load_prizes()
  prize = next((p for p in prizes if p["id"] == prize_id), None)

  if prize and "user" in session:
    user_xp = session["user"]["scores"]
    if user_xp >= prize["cost"]:
      session["user"]["scores"] -= prize["cost"]

      # Track redeemed prize
      if "redeemed_prizes" not in session["user"]:
        session["user"]["redeemed_prizes"] = []
      session["user"]["redeemed_prizes"].append({
        "id": prize_id,
        "name": prize["name"],
        "timestamp": datetime.now().isoformat()
      })

      flash(f"✨ Redeemed {prize['name']}! (-{prize['cost']} XP)", "success")
      session.modified = True
    else:
      flash(f"❌ Not enough XP! Need {prize['cost'] - user_xp} more XP.", "error")
  else:
    flash("❌ Prize not found or session error.", "error")

  return redirect(url_for("profile"))


@app.route("/add-badge", methods=["POST"])
def add_badge():
  """Peer praise: add a badge to the user's collection."""
  badges_list = {
    "well_done": {"emoji": "👍", "text": "Well Done", "color": "#22c55e"},
    "nice_work": {"emoji": "🎉", "text": "Nice Work", "color": "#06b6d4"},
    "improvement": {"emoji": "📈", "text": "Great Improvement", "color": "#f59e0b"},
  }
  badge_type = request.form.get("badge_type", "well_done")

  if "user" in session:
    if "badges" not in session["user"]:
      session["user"]["badges"] = []

    badge = badges_list.get(badge_type, badges_list["well_done"])
    session["user"]["badges"].append(badge)
    session.modified = True

  return redirect(url_for("profile"))


@app.route("/update-units", methods=["POST"])
def update_units():
  """Update course unit progress values for demo purposes."""
  if "user" in session:
    # Simulate progress update by adding random XP-based changes
    import random
    for unit in session["user"]["course_units"]:
      current = unit["progress"]
      change = random.randint(-5, 10)
      unit["progress"] = max(0, min(100, current + change))

      # Update color based on threshold
      if unit["progress"] >= 80:
        unit["color"] = "green"
      elif unit["progress"] >= 50:
        unit["color"] = "orange"
      else:
        unit["color"] = "red"

    session.modified = True

  return redirect(url_for("profile"))


@app.route("/activate-power-up/<power_up_type>", methods=["POST"])
def activate_power_up(power_up_type):
  """Activate a power-up (2x_boost or streak_shield)."""
  valid_power_ups = {
    "2x_boost": {"cost": 150, "duration_hours": 1, "name": "2x XP Boost"},
    "streak_shield": {"cost": 100, "duration_hours": 24, "name": "Streak Shield"}
  }

  if power_up_type not in valid_power_ups and "user" in session:
    flash("❌ Invalid power-up type.", "error")
    return redirect(url_for("profile"))

  if "user" in session:
    power_up_info = valid_power_ups[power_up_type]
    user_xp = session["user"]["scores"]

    if user_xp >= power_up_info["cost"]:
      session["user"]["scores"] -= power_up_info["cost"]

      # Add power-up with expiration
      expires_at = (datetime.now() + timedelta(hours=power_up_info["duration_hours"])).timestamp()
      if "power_ups" not in session["user"]:
        session["user"]["power_ups"] = []

      session["user"]["power_ups"].append({
        "type": power_up_type,
        "expires": expires_at,
        "name": power_up_info["name"]
      })

      flash(f"⚡ Activated {power_up_info['name']}! ({power_up_info['duration_hours']}h duration)", "success")
      session.modified = True
    else:
      flash(f"❌ Not enough XP! Need {power_up_info['cost'] - user_xp} more XP.", "error")

  return redirect(url_for("profile"))


@app.route("/change-cosmetic/<cosmetic_type>/<value>", methods=["POST"])
def change_cosmetic(cosmetic_type, value):
  """Change user cosmetic (theme or frame)."""
  valid_themes = ["dark", "light", "neon", "sunset"]
  valid_frames = ["default", "gold", "crystal", "rainbow"]

  if cosmetic_type == "theme" and value in valid_themes:
    if "user" in session:
      if "cosmetics" not in session["user"]:
        session["user"]["cosmetics"] = {"theme": "dark", "frame": "default"}
      session["user"]["cosmetics"]["theme"] = value
      flash(f"🎨 Theme changed to {value.capitalize()}!", "success")
      session.modified = True
  elif cosmetic_type == "frame" and value in valid_frames:
    if "user" in session:
      if "cosmetics" not in session["user"]:
        session["user"]["cosmetics"] = {"theme": "dark", "frame": "default"}
      session["user"]["cosmetics"]["frame"] = value
      flash(f"🖼️ Frame changed to {value.capitalize()}!", "success")
      session.modified = True
  else:
    flash("❌ Invalid cosmetic option.", "error")

  return redirect(url_for("profile"))


if __name__ == "__main__":
  app.run(debug=True)
