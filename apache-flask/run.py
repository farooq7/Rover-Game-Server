import configparser
import sys

from app import app
from app.core import Core

def main():
    if len(sys.argv) != 2:
        print('Usage: python run.py [config]')
        sys.exit(1)
    try:
        app.core = Core(sys.argv[1])
        app.core.setup()
        config = app.core.config
        app.run(host='0.0.0.0', port=config.getint('app', 'port'),
                threaded=config.getboolean('app', 'threaded'),
                debug=config.getboolean('app', 'debug'))
    except configparser.NoOptionError as e:
        print('Invalid configuration file.')
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
