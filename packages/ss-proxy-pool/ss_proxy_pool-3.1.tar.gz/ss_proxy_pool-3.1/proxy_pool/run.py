from proxy_pool.scheduler import Sheduler
from proxy_pool.api import app


def main():
    s = Sheduler()
    s.run()
    app.run()


if __name__ == '__main__':
    main()
