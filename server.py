from flask import Flask, escape, request, render_template, g, jsonify
from driver import apa102

app = Flask(__name__)

def update_strip(strip, color, brightness):
  color = int(color[1:], 16)
  for led in range(strip.num_led):
    strip.set_pixel_rgb(led, color, bright_percent=brightness)
  strip.show()

def init_strip(g):
  g.strip = apa102.APA102(num_led=4*60)
  g.color = "#ffffff"
  g.brightness = 100

@app.route('/')
def index():
  if 'strip' not in g:
    init_strip(g)

  return render_template('index.html', color=g.color, brightness=g.brightness)

@app.route('/color', methods=['POST'])
def set_color():
  if 'strip' not in g:
    init_strip(g)

  g.color = request.form['color']
  update_strip(g.strip, g.color, g.brightness)
  return jsonify(success=True)

@app.route('/brightness', methods=['POST'])
def set_brightness():
  if 'strip' not in g:
    init_strip(g)

  g.brightness = int(request.form['brightness'])
  update_strip(g.strip, g.color, g.brightness)
  return jsonify(success=True)

@app.route('/shutdown', methods=['POST'])
def shutdown():
  if 'strip' not in g:
    init_strip(g)

  g.strip.clear_strip()
  return jsonify(success=True)

