from app import create_app

wsgi = create_app('development')

if __name__ == '__main__':
    wsgi.run()