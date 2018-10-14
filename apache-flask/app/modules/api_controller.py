import datetime
import json
import jsonschema
import sys

from bson import json_util

from app import app
from game import Game

class API_Controller:

    def __init__(self):
        self.init_schema()
        self.game = Game()
        self.seq = {}

    def setup(self):
        self.game.setup()

    def init_schema(self):
        self.pic32_data_schema = {
            'type' : 'object',
            'properties' : {
                'seq' : {'type' : 'number'},
                'data' : {'type' : 'string'},
                'ip' : {'type' : 'string'},
                'target' : {'type' : 'string'},
                'rgb_r' : {'type' : 'number'},
                'rgb_g' : {'type' : 'number'},
                'rgb_b' : {'type' : 'number'},
                'color' : {'type' : 'string'}
            },
            'required': ['seq', 'data', 'ip', 'target', 'rgb_r', 'rgb_g', 'rgb_b', 'color']
        }
        self.pixy_data_schema = {
            'type' : 'object',
            'properties' : {
                'target' : {'type' : 'string'},
                'x' : {'type' : 'number'},
                'y' : {'type' : 'number'},
                'width' : {'type' : 'number'},
                'height' : {'type': 'number'}
            },
            'required': ['target', 'x', 'y', 'height', 'width']
        }
        self.control_data_schema = {
            'type' : 'object',
            'properties' : {
                'data' : {'type' : 'string'},
                'ip' : {'type' : 'string'},
                'target' : {'type' : 'string'},
                'left' : {'type' : 'number'},
                'right' : {'type' : 'number'}
            },
            'required': ['data', 'ip', 'target', 'left', 'right']
        }

    def reset(self):
        print('Performing reset.')
        app.core.db.command('dropDatabase')
        self.game.parse_tokens()

    def calibrate(self, target):
        c = app.core.db['calibrate']
        data = {}
        data['target'] = target
        data['datetime'] = datetime.datetime.utcnow()
        data['responded'] = False
        c.insert_one(data)

    def check_calibrate_status(self, target):
        c = app.core.db['calibrate']
        results = c.find({'target': target, 'responded': False}).sort([('_id', -1)]).limit(1)
        count = results.count()
        for result in results:
            c.update_one({'_id': result['_id']}, {'$set': {'responded': True}})
        if count > 0:
            return True
        else:
            return False

    def process_api_rover(self, data):
        try:
            jsonschema.validate(data, self.pic32_data_schema)
        except Exception as e:
            print(e)
            return 'Data does not match JSON schema.', 500
        data['datetime'] = datetime.datetime.utcnow().isoformat()
        self.rover_integrity_check(data['target'], data['seq'], data['datetime'])
        self.record_rgb_data(data)
        self.game.process_rgb(data['target'], data['color'])
        return_package = self.generate_return_rover_package(data['target'], data['seq'])
        return json.dumps(return_package), 200

    def process_api_pixy(self, data):
        try:
            jsonschema.validate(data, self.pixy_data_schema)
        except Exception as e:
            print(e)
            return 'Data does not match JSON schema.', 500
        data['datetime'] = datetime.datetime.utcnow().isoformat()
        self.record_pixy_data(data)
        return '', 204

    def process_api_control(self, data):
        try:
            jsonschema.validate(data, self.control_data_schema)
        except Exception as e:
            print(e)
            return 'Data does not match JSON schema.', 500
        data['datetime'] = datetime.datetime.utcnow().isoformat()
        self.record_control_data(data)
        return '', 204

    def record_missed_message(self, target, i, datetime):
        c = app.core.db['integrity']
        c.insert_one({'target': target, 'seq': i, 'datetime': datetime})

    def record_rgb_data(self, rgb_data):
        c = app.core.db['rgb']
        c.insert_one(rgb_data)

    def record_pixy_data(self, pixy_data):
        if 'rotaton' not in pixy_data:
            pixy_data['rotation'] = 0
        c = app.core.db['pixy']
        c.insert_one(pixy_data)

    def record_control_data(self, control_data):
        c = app.core.db['control']
        c.insert_one(control_data)

    def generate_return_rover_package(self, target, seq):
        data = {}
        data['seq'] = seq
        if self.check_calibrate_status(target):
            data['cmd'] = 'motor_calibrate'
            data['motor_left'] = 0
            data['motor_right'] = 0
        else:
            data['cmd'] = 'motor_control'
            motor_left, motor_right = self.game.get_speed(target)
            data['motor_left'] = int(motor_left)
            data['motor_right'] = int(motor_right)
        return data

    def rover_integrity_check(self, target, seq, datetime):
        if target not in self.seq:
            self.seq[target] = 0
        if self.seq[target] == 0 or seq == 0:
            self.seq[target] = seq
            return True
        self.seq[target] = self.seq[target] + 1
        if seq != self.seq[target]:
            for i in range(self.seq[target], seq):
                self.record_missed_message(target, i, datetime)
            self.seq[target] = seq
            return False
        return True

    def notifications(self, last_notification_datetime):
        data = {}
        data['notifications'] = []
        parsed_datetime = datetime.datetime.strptime(last_notification_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        condition = {'datetime': {'$gt': parsed_datetime}}
        results = app.core.db['notifications'].find(condition).sort([('_id', -1)])
        for result in list(results):
            result['datetime'] = result['datetime'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            data['notifications'].append(result)
        return json.dumps(data, default=json_util.default), 200

    def last_location_api(self, target): 
        return json.dumps(self.game.get_latest_location(target), default=json_util.default), 200

    def get_tokens_api(self):
        return json.dumps(self.game.get_tokens(), default=json_util.default), 200