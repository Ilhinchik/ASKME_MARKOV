import multiprocessing

# Привязка к порту
bind = '127.0.0.1:8081'

# Количество рабочих процессов
workers = multiprocessing.cpu_count() * 2 + 1

wsgi_app = "wsgi_app.wsgi:application"