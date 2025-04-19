# Развертывание 
Дальнейшее руководство предназначено для развертывания приложения CashFlow на устройствах с операционной системой Ubuntu. Предполагается, что устройство (учетная запись пользователя) предназначено только для развертывания и не использовалось ранее.

## 1. Подготовка сервера
### 1.1. Обновите систему
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2. Установите зависимости 
```bash
sudo apt install -y git python3-pip python3-venv nginx supervisor python3-virtualenv
```
## 2. Настройка проекта
### 2.1. Склонируйте репозиторий
#### 2.1.1. Настройка SSH ключей
```bash
ssh-keygen -t ed25519 && eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519 && cat ~/.ssh/id_ed25519.pub 
```
После введения этой команды будет необходимо совершить 4 последовательных ввода:
1. Расположение ключей: нажмите Enter;
2. Пароль для ключа: придумайте, введите и запомните пароль. Во время ввода пароля он не будет отображаться - это нормально, на самом деле он вводится.
3. Подтверждение пароля: введите пароль, созданный ранее.
4. Запрос пароля для подключения SSH ключа: введите пароль, созданный ранее.

По завершению команды появится строка которая будет выглядеть примерно так:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ56mgDNksTjh6p4rDl9/EdBenmmy7AgA5iQqJiuveFh user@server
```
Полностью скопируйте строку и отправьте владельцу репозитория, для добавления публичного SSH ключа.

#### 2.1.2. Клонирование репозитория
```bash
git clone git@github.com:MonkEHlam/it-solution-test-task.git
```
На вопрос системы отвечаем yes

### 2.2. Создание виртуального окружения
```bash
virtualenv it-solution-test-task/venv && source it-solution-test-task/venv/bin/activate
```
### 2.3. Установка проектных зависимостей
```bash
pip install -r it-solution-test-task/CashFlow/requirements.txt
```

### 2.4. Настройка окружения.
В следующих подразделах необходимо пользоваться текстовым редактором nano. Чтобы сохранить файл, нажмите control+O, затем Enter. Чтобы выйти, нажмите control+X.
#### 2.4.1. Настройки django
```bash
nano it-solution-test-task/CashFlow/CashFlow/production_settings.py
```

Введите следующее:
```python
from pathlib import Path  
import os  
from django.core.management.utils import get_random_secret_key  
  
BASE_DIR = Path(__file__).resolve().parent.parent  
  
STATIC_URL = "/static/"  
  
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  
  
STATICFILES_DIRS = [  
    os.path.join(BASE_DIR, 'CashFlowRecords/static'),  
]  
  
SECRET_KEY = get_random_secret_key()  
  
DEBUG = True  
  
SECURE_SSL_REDIRECT = False  
  
CSRF_COOKIE_SECURE = True  
  
SESSION_COOKIE_SECURE = True  
  
ALLOWED_HOSTS = ["127.0.0.1", "domen.com", "www.domen.com"]  
  
DATABASES = {  
    "default": {  
        "ENGINE": "django.db.backends.sqlite3",  
        "NAME": BASE_DIR / "db.sqlite3",  
    }  
}
```
#### 2.4.2. Настройки gunicorn
```bash
mkdir it-solution-test-task/CashFlow/config && nano it-solution-test-task/CashFlow/config/gunicorn.conf.py
```

Введите следующее, заменяя USER на имя учетной записи пользователя:
```python
bind = "127.0.0.1:8000"  
workers = 2  
user = "USER"  
timeout = 120
```
#### 2.4.3. Настройки Supervisor
```bash
sudo nano /etc/supervisor/conf.d/cashflow.conf
```

Введите следующее, заменяя USER на имя учетной записи пользователя:
```conf
[program:CashFlow]  
command=/home/USER/it-solution-test-task/venv/bin/gunicorn CashFlow.wsgi:application -c /home/USER/it-solution-test-task/CashFlow/config/gunicorn.conf.py  
directory=/home/USER/it-solution-test-task/CashFlow  
user=USER  
autorestart=true  
redirect_stderr=true  
stdout_logfile=/home/USER/it-solution-test-task/CashFlow/logs/debug.log
```

```bash
sudo supervisorctl reread && sudo supervisorctl update
```

#### 2.4.4. Настройки nginx

```bash
sudo nano /etc/nginx/sites-available/cashflow
```

Введите следующее, заменяя USER на имя учетной записи пользователя:
```
server {
    listen 80;
    server_name domen.com www.domen.com;
    access_lof /var/log/nginx/debug.log

    location /static/ {
        alias \home\USER\it-solution-test-task\CashFlow\static;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $server_name;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### 2.5.5. Миграции

```bash
cd it-solution-test-task/CashFlow && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic --noinput
```

## 3. Запуск
```bash 
sudo systemctl restart nginx && sudo supervisorctl start CashFlow
```

## 4. Отключение
```bash
sudo systemctl stop nginx && sudo supervisorctl stop CashFlow
```