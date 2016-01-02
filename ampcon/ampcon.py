from flask import Flask, render_template, jsonify, request
from amplifier import Amplifier, SOURCES

app = Flask(__name__)

amplifier_obj = Amplifier(serial_port=2, logger=app.logger)

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

@app.route('/:volume_up')
def volume_up():
    amplifier_obj.volume_up()
    return jsonify(amplifier_obj.json_ready())

@app.route('/:volume_down')
def volume_down():
    amplifier_obj.volume_down()
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

@app.route('/:spk_a')
def spk_a():
    amplifier_obj.speaker_a_toggle()
    return jsonify(amplifier_obj.json_ready())

@app.errorhandler(500)
def page_not_found(e):
    return "Error: %s" % e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
