import json
import sys

from bson import json_util
from flask import request

from app import app

@app.route('/api/rover', methods=['POST'])
def api_rover():
    data = request.data
    if not data or len(data) == 0:
        print('No data included in POST request.')
        return '', 500
    data = request.get_json()
    data['ip'] = request.remote_addr
    data['target'] = request.remote_addr
    if not data:
        print('No JSON data could be parsed from POST request.')
        return '', 500
    return app.core.api_controller.process_api_rover(data)

@app.route('/api/rover/<target>', methods=['POST'])
def api_rover_target(target):
    data = request.data
    if not data or len(data) == 0:
        print('No data included in POST request.')
        return '', 500
    data = request.get_json()
    data['ip'] = request.remote_addr
    data['target'] = target
    if not data:
        print('No JSON data could be parsed from POST request.')
        return '', 500
    return app.core.api_controller.process_api_rover(data)

@app.route('/api/pixy', methods=['POST'])
def api_pixy():
    data = request.data
    if not data or len(data) == 0:
        print('No data included in POST request.')
        return '', 500
    data = request.get_json()
    data['ip'] = request.remote_addr
    if not data:
        print('No JSON data could be parsed from POST request.')
        return '', 500
    return app.core.api_controller.process_api_pixy(data)

@app.route('/api/control', methods=['POST'])
def api_control():
    data = request.data
    if not data or len(data) == 0:
        print('No data included in POST request.')
        return '', 500
    data = request.get_json()
    data['ip'] = request.remote_addr
    data['target'] = request.remote_addr
    if not data:
        print('No JSON data could be parsed from POST request.')
        return '', 500
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>', methods=['POST'])
def api_control_target(target):
    data = request.data
    if not data or len(data) == 0:
        print('No data included in POST request.')
        return '', 500
    data = request.get_json()
    data['ip'] = request.remote_addr
    data['target'] = target
    if not data:
        print('No JSON data could be parsed from POST request.')
        return '', 500
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>/forward', methods=['POST'])
def api_control_forward(target):
    data = {}
    data['data'] = 'control'
    data['ip'] = request.remote_addr
    data['left'] = 10
    data['right'] = 10
    data['target'] = target
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>/left', methods=['POST'])
def api_control_left(target):
    data = {}
    data['data'] = 'control'
    data['ip'] = request.remote_addr
    data['left'] = -10
    data['right'] = 10
    data['target'] = target
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>/right', methods=['POST'])
def api_control_right(target):
    data = {}
    data['data'] = 'control'
    data['ip'] = request.remote_addr
    data['left'] = 10
    data['right'] = -10
    data['target'] = target
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>/reverse', methods=['POST'])
def api_control_reverse(target):
    data = {}
    data['data'] = 'control'
    data['ip'] = request.remote_addr
    data['left'] = -10
    data['right'] = -10
    data['target'] = target
    return app.core.api_controller.process_api_control(data)

@app.route('/api/control/<target>/stop', methods=['POST'])
def api_control_stop(target):
    data = {}
    data['data'] = 'control'
    data['ip'] = request.remote_addr
    data['left'] = 0
    data['right'] = 0
    data['target'] = target
    return app.core.api_controller.process_api_control(data)

@app.route('/api/notifications/<last_notification_datetime>', methods=['POST'])
def api_notifications(last_notification_datetime):
    return app.core.api_controller.notifications(last_notification_datetime)

@app.route('/api/last_location/<target>', methods=['POST'])
def api_last_location(target):
    return app.core.api_controller.last_location_api(target)

@app.route('/api/reset', methods=['POST'])
def api_reset():
    app.core.api_controller.reset()
    return '', 202

@app.route('/api/calibrate/<target>', methods=['POST'])
def api_calibrate(target):
    if target != None:
        app.core.api_controller.calibrate(target)
    return '', 202

@app.route('/api/get_tokens', methods=['POST'])
def api_get_tokens():
    return app.core.api_controller.get_tokens_api()

@app.route('/api/status', methods=['GET'])
def api_status():
    try:
        out = []
        out.append('Status check passed.')
        out.append(app.core.client.admin.command('ismaster'))
        return json.dumps(out, default=json_util.default), 200
    except AssertionError as e:
        return 'Status check failed.', 500