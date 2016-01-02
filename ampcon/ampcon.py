from flask import Flask, render_template, jsonify, request
from amplifier import Amplifier, SOURCES
import yaml

app = Flask(__name__)

with open("config.yaml") as f:
	config = yaml.load(f)
amplifier_obj = Amplifier(serial_port=config["serial_port"], logger=app.logger)

@app.context_processor
def inject_user():
    if not amplifier_obj.configured:
        amplifier_obj.configure()

    return {
        'sources': SOURCES
    }

@app.route('/')
def hello_world():
    amplifier_obj.configured = False
    return render_template('index.html')

@app.route('/:volume')
def volume_change():
    step = int(request.args.get('step'))
    amplifier_obj.volume_change(step)
    return jsonify(amplifier_obj.json_ready())

@app.route('/:volume_percent/<int:percent>')
def volume_percent(percent):
    amplifier_obj.set_volume_percent(percent)
    return jsonify(amplifier_obj.json_ready())

@app.route('/:volume_calibrate')
def volume_calibrate():
    amplifier_obj.calibrate_volume()
    return jsonify(amplifier_obj.json_ready())

@app.route("/:status")
def status():
    return jsonify(amplifier_obj.json_ready())

@app.route("/:set_source")
def source():
    new_source = request.args.get('source')
    amplifier_obj.set_source(new_source)
    return jsonify(amplifier_obj.json_ready())

@app.route('/:mute')
def mute():
    amplifier_obj.mute_toggle()
    return jsonify(amplifier_obj.json_ready())

@app.route('/:power')
def power():
    amplifier_obj.power_toggle()
    return jsonify(amplifier_obj.json_ready())

@app.route('/:spk/<speaker>')
def toggle_speaker(speaker):
    amplifier_obj.speaker_toggle(speaker)
    return jsonify(amplifier_obj.json_ready())

@app.errorhandler(500)
def page_not_found(e):
    return "Error: %s" % e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
