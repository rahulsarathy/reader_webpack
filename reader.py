from app import create_app, db
from app.models import User, Blog, Poll
from app.main import routes
import os
import threading
import time
import requests
from config import Config


def start_runner():
    def start_loop():
        not_started = True
        if os.environ.get('HOME_URL') is None:
            url = 'http://127.0.0.1:5000'
        else:
            url = os.environ.get('HTTP') + os.environ.get('HOME_URL') + os.environ.get('PORT')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        print(url)
        while not_started:
            print('In start loop')
            try:
                r = requests.get(url + '/poll', headers=headers)
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except Exception as e:
                print(e)
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

app = create_app()
start_runner()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Blog': Blog, 'Poll': Poll}
