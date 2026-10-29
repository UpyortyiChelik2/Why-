# Академія — навчальна LMS на Django

Навчальна система керування курсами: каталог курсів, реєстрація/вхід, ролі студентів і викладачів, запис на курс, уроки, завдання, здавання робіт та оцінювання.

## Запуск локально (Windows)

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Відкрийте http://127.0.0.1:8000/ . Панель адміністратора: http://127.0.0.1:8000/admin/

## Як користуватися
- Зареєструйтеся через кнопку «Створити акаунт»; за замовчуванням це студент.
- Щоб створити курс, увійдіть через Django admin і додайте курс, уроки та завдання. Для повноцінного викладацького доступу призначте користувачу роль «Викладач» у профілі.
- Студент може відкрити курс, записатися на нього, читати уроки, надсилати текст відповіді на завдання та бачити оцінку.
- Адміністратор керує всіма даними через `/admin/`.

## Деплой (Render)
1. Створіть GitHub-репозиторій і завантажте вміст цієї папки.
2. На Render створіть **New + → Web Service** та під'єднайте репозиторій.
3. Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --run-syncdb`
4. Start command: `gunicorn config.wsgi:application`.
5. Для публічного продакшну обов'язково налаштуйте `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS та PostgreSQL через змінні середовища. Ця навчальна версія використовує SQLite локально.

## GitFlow, мінімальний варіант
```bash
git checkout -b develop
git checkout -b feature/course-catalog
git add .
git commit -m "Build LMS course catalog and student workflow"
git push -u origin feature/course-catalog
```
Створіть Pull Request у GitHub з `feature/course-catalog` до `develop`, а потім з `develop` до `main`. Не додавайте `.venv/` або `db.sqlite3` до репозиторію.
