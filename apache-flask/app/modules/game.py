import datetime
import random

from app import app
from app.modules import token_manager

class Game:

    def __init__(self):
        pass

    def setup(self):
        self.parse_tokens()

    def parse_tokens(self):
        current_tokens = self.get_tokens()
        print(current_tokens)
        lines = ''
        with open('config/tokens.txt', 'r') as f:
            lines = f.read()
        lines = lines.split('\n')
        for s in lines:
            if len(s) == 0:
                continue
            token = self.parse_token(s)
            if token != None:
                new_token = True
                for ct in current_tokens:
                    if ct['name'] == token['name']:
                        new_token = False
                        break
                if new_token:
                    self.update_db_new_token(token)

    def get_tokens(self):
        results = app.core.db['token'].find({}).sort([('_id', -1)])
        return list(results)

    def get_active_tokens(self, target):
        condition = {'target': target, 'expiration': {'$gte': datetime.datetime.utcnow()}}
        results = list(app.core.db['token'].find(condition).sort([('_id', -1)]))
        return results

    def update_token(self, token):
        print('Updating token: {}'.format(token))
        c = app.core.db['token']
        search = {'_id': token['_id']}
        token.pop('_id', None)
        operation = {'$set': token}
        c.update_one(search, operation)

    def process_rgb(self, target, color):
        last_location = self.get_latest_location(target)
        if last_location == None:
            print('{} has no location data.'.format(target))
            return
        tokens = self.get_tokens()
        dt = datetime.datetime.utcnow()
        for token in tokens:
            if (token == None):
                continue
            if self.token_match(token, target, last_location['x'], last_location['y'], color, dt):
                token['target'] = target
                token['datetime'] = datetime.datetime.utcnow()
                token['expiration'] = token['datetime'] + datetime.timedelta(seconds=token['duration'])
                token['collected'] = True
                print('{} has collected {}. {}'.format(target, token['name'], token['description']))
                self.add_notification('{} has collected {}. {}'.format(target, token['name'], token['description']))
                self.update_token(token)

    def get_speed(self, target):
        control = self.get_control(target)
        if control == None:
            print('{} has no control messages.'.format(target))
            return (0, 0)
        active_tokens = self.get_active_tokens(target)
        print('{} has {} active tokens.'.format(target, len(active_tokens)))
        left, right = self.apply_slowdown(active_tokens, control['left'], control['right'])
        left = min(left, 10)
        left = max(left, -10)
        right = min(right, 10)
        right = max(right, -10)
        return (left, right)

    def update_db_new_token(self, token):
        c = app.core.db['token']
        c.insert_one(token)

    def get_control(self, target):
        results = app.core.db['control'].find({'target': target}).sort([('_id', -1)]).limit(1)
        for result in list(results):
            return result
        return None

    def get_latest_location(self, target):
        results = app.core.db['pixy'].find({'target': target}).sort([('_id', -1)]).limit(1)
        for result in list(results):
            return result
        return None

    def add_notification(self, s):
        data = {}
        data['datetime'] = datetime.datetime.utcnow()
        data['text'] = s
        c = app.core.db['notifications']
        c.insert_one(data)

    def apply_slowdown(self, tokens, left, right):
        for token in tokens:
            left = left * token['slowdown_left']
            right = right * token['slowdown_right']
        return (left, right)

    def parse_token(self, s):
        if (len(s) == 0 or s[0] == ';'):
            return
        fields = s.split(',')
        if len(fields) < 12:
            return None
        print('Parsing token: ' + s)
        token = {}
        token['name'] = fields[0].strip()
        token['color'] = fields[1].strip()
        token['slowdown_left'] = float(fields[2].strip())
        token['slowdown_right'] = float(fields[3].strip())
        token['duration'] = float(fields[4].strip())
        token['x'] = int(float(fields[5].strip()))
        token['y'] = int(float(fields[6].strip()))
        token['x1'] = int(fields[7].strip())
        token['y1'] = int(fields[8].strip())
        token['x2'] = int(fields[9].strip())
        token['y2'] = int(fields[10].strip())
        token['unique'] = (fields[11].strip().lower() == "true")
        token['target_limit'] = fields[12].strip()
        token['description'] = fields[13].strip()
        token['datetime'] = None
        token['target'] = None
        token['expiration'] = None
        token['collected'] = False
        return token

    def token_overlap(self, token, x, y):
        return x > token['x1'] and x < token['x2'] and y > token['y1'] and y < token['y2']

    def token_match(self, token, target, x, y, color, dt):
        if token['color'] != color:
            return False
        if token['unique'] == True:
            if token['target'] == target:
                return False
        else:
            print(token, target)
            if token['target_limit'] != target:
                print('fail')
                return False
            if token['collected']:
                if token['expiration'] > dt:
                    return False
        print('good')
        if self.token_overlap(token, x, y):
            print('Token match found: ({}, {})'.format(target, token))
            return True
        return False