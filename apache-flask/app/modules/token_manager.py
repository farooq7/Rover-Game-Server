import datetime

def parse(s):
    if (len(s) == 0 or s[0] == ';'):
        return
    fields = s.split(',')
    if len(fields) < 10:
        return None
    print('Parsing token: ' + s)
    token = {}
    token['name'] = fields[0].strip()
    token['color'] = fields[1].strip()
    token['slowdown'] = float(fields[2].strip())
    token['duration'] = int(fields[3].strip())
    token['x1'] = int(fields[4].strip())
    token['y1'] = int(fields[5].strip())
    token['x2'] = int(fields[6].strip())
    token['y2'] = int(fields[7].strip())
    token['unique'] = (fields[8].strip().lower() == "true")
    token['description'] = (fields[9].strip())
    return token

def get_token_instance(token):
    new_token = {}
    for k, v in token.items():
        new_token[k] = v
    new_token['collected'] = datetime.datetime.utcnow()
    new_token['expiration'] = new_token['collected'] + datetime.timedelta(seconds=token['duration'])
    return new_token

def token_overlap(token, loc):
    return loc['x'] >= token['x1'] and loc['x'] <= token['x2'] and loc['y'] >= token['y1'] and loc['y'] <= token['y2']

def check_token(token, rgb, last_location):
    return token['color'] == rgb['color'] and token_overlap(token, last_location)