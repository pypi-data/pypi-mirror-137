from flask import Flask, g
from proxy_pool.db import Reidis_client

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis_client'):
        g.redis_client = Reidis_client()
    return g.redis_client


@app.route('/')
def index():
    return '<h1>欢迎进入代理池系统！</h1>'


@app.route('/get')
def get():
    return get_conn().pop()


@app.route('/count')
def count():
    return str(get_conn().queue_len)
