import multiprocessing

#change port as your wish
bind = "127.0.0.1:8000" 
workers = multiprocessing.cpu_count() * 2 + 1
# create a folder called log and use pwd to see actual path and then add path/log/gunicorn-access.log and path/log/gunicorn-error.log
accesslog = "/home/p/production/InvenTrack/log/gunicorn-access.log"
errorlog = "/home/p/production/InvenTrack/log/gunicorn-error.log"