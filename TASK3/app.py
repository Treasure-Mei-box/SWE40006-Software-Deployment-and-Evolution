import json, os, datetime
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DATA = "/data/pulse.json"

PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Daily Pulse</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 550px; margin: 2rem auto; padding: 0 1rem; background: #f8fafc; }
    .entry { background: white; border-left: 4px solid #6366f1; padding: 1rem; margin-bottom: 1rem; border-radius: 0 8px 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .tag { display: inline-block; background: #e0e7ff; color: #3730a3; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
    form { display: flex; flex-direction: column; gap: 0.5rem; background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    select, input, button { padding: 0.6rem; border-radius: 6px; border: 1px solid #cbd5e1; }
    button { background: #6366f1; color: white; border: none; font-weight: 600; cursor: pointer; }
  </style>
</head>
<body>
  <h1>🌱 Daily Pulse</h1>

  <form method="post" action="/add">
    <select name="status">
      <option value="🚀 Focused">🚀 Focused</option>
      <option value="✅ Productive">✅ Productive</option>
      <option value="☕ Relaxed">☕ Relaxed</option>
      <option value="⚠️ Blocked">⚠️ Blocked</option>
    </select>
    <input name="log" placeholder="What did you get done or how's it going?" required>
    <button type="submit">Log Entry</button>
  </form>

  <h3 style="margin-top:2rem;">Timeline</h3>
  {% for e in entries %}
    <div class="entry">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
        <span class="tag">{{ e.status }}</span>
        <small style="color:#94a3b8;">{{ e.time }}</small>
      </div>
      <div>{{ e.log }}</div>
    </div>
  {% else %}
    <p style="color:#94a3b8;">No status logged today.</p>
  {% endfor %}
</body>
</html>
"""


def load():
    if os.path.exists(DATA):
        with open(DATA) as f:
            return json.load(f)
    return []


@app.route("/")
def index():
    return render_template_string(PAGE, entries=load())


@app.route("/add", methods=["POST"])
def add():
    entries = load()
    entries.insert(
        0,
        {
            "status": request.form.get("status"),
            "log": request.form.get("log", "").strip(),
            "time": datetime.datetime.now().strftime("%b %d, %H:%M"),
        },
    )
    os.makedirs("/data", exist_ok=True)
    with open(DATA, "w") as f:
        json.dump(entries, f, indent=2)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
