# web: gunicorn --bind 0.0.0.0:$PORT apis:app
web: gunicorn apis:application --preload -b 0.0.0.0:5001
worker1: python script.py
worker2: python emailTest.py
# web: gunicorn apis:app

