# eBookstore

## Clone project
```
git clone https://github.com/binh234/eBookstore.git

cd  eBookstore/eBookstore
```

## Cài đặt các thư viện cần thiết
```
python -m pip install -r requirements.txt
```

## Chuẩn bị MySQL
> Đảm bảo có một schema tên **bookstore** với user là **root** và password là **Admin.12345**
<img src="./screenshots/database.png">

## Migrate data vào MySQL
```
python manage.py migrate
```

## Nạp dữ liệu vào database
```
python manage.py loaddata db.json
```

### Development
```
python manage.py runserver
```
Mở [localhost:8000](http://localhost:8000).

### Thêm 1 template mới vào project
* Thêm file **.html** vào thư mục <app_name>/template/<app_name>
* Thêm một view function mới vào file <app_name>/view_funnc.py
<img src="./screenshots/view_func.png">
* Thêm url mới vào file <app_name>/urls.py theo cấu trúc path('<url_path>', view_func, name='<url_name>')
<img src="./screenshots/url.png">

### Thêm file static (css, js, image, ...) vào project
* Thêm file *.(css/js/...)* vào thư mục *static/(css/js/...)*

### Liên kết css, js, ... vào file html
* Thêm dòng **{% load static %}** vào file html tương ứng
* Liên kết css, js, ... vào file html
*Ex:* 
```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```
