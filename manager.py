__author__ = 'Xu Zhao'

from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(ssl_context="adhoc")
