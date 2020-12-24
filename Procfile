# web: gunicorn --bind 0.0.0.0:$PORT apis:app
web: gunicorn apis:application --preload -b 0.0.0.0:5001
worker: python script.py
worker: python emailTest.py
# web: gunicorn apis:app

