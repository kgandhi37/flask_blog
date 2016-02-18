# file we will be running

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # points to this file, allows python to know starting point for this app
# above, find files current location then append python path to level above it

from flask.ext.script import Manager, Server # run python, manage and load, serve
from flask.ext.migrate import MigrateCommand # 
from flask_blog import app # from __init__.py


manager = Manager(app) # instantiating manager from the app, can import and add commands to manager, see below
manager.add_command('db', MigrateCommand) # adding Migrate to manager - now all set to use migrations - added to __init__.py too

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000))# note, using integer here for port
    )
)

# to run app

if __name__ == "__main__": # double ==
    manager.run() # execute manager
