from flask import Flask
import os

env = {
    'PORT'      : 3000,
    'HOST'      : '127.0.0.1',
    'APP_ENV'   : 'DEV',
    'APP_SECRET': 'c3ds1bN@de',
    'APP'       : Flask(__name__, template_folder="public"),  
    'SQL_CONF'  : {
        'DB_NAME'  : 'valkiria_chatbot_lite_2',
        # 'DB_URI'   : 'mysql://root:arr0wf1r3@localhost/valkiria_chatbot_mysql'
        'DB_URI'   : str.format('sqlite:////{0}', os.path.abspath('database/valkiria_chatbot_lite_2.db'))
    },
    'NO_SQL_CONF':{
        'DB_NAME': 'valkiria_chatbot_mongo',
        'DB_URI' : 'mongodb://localhost:27017',
    },
    'CHILD_TIME_WRITING_FACTOR': 0.6
}