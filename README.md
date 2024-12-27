# netmovie
## Add initial data for test
Current fixture have 972 records. 
- Have a Superuser with: **Username:** adel , **Password:** adel

```bash
python manage.py loaddata initial_fixture.json
```
# Run with Docker
### required images:
- python:alpine, postgres:alpine, nginx:alpine
```bash
docker-compose up --build
```
- stop
```bash
docker-compose down
```
on address: `http://0.0.0.0/`
# Run with manage.py:
1. **settings.py:** comment **STATIC_ROOT**
2. **settings.py:** uncomment **STATICFILES_DIRS**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
project runed on `http://127.0.0.1:8000`

for create admin
```python
python manage.py createsuperuser USERNAME
```
*and then enter **email**(not required),**password**, **re-password***

## Run Tests
```bash
python manage.py test
```
## URLS
- Login: `http://127.0.0.1:800/login`
- Signup: `http://127.0.0.1:800/signup`
- Home: `http://127.0.0.1:800`
- Actors: `http://127.0.0.1:8000/actors`
- Serials: `http://127.0.0.1:8000/serial`
- Movies: `http://127.0.0.1:8000/movie/`
- User Panel `http://127.0.0.1:8000/dashboard/dashboard/`
- Movie Ganer Detail: `http://127.0.0.1:8000/movie/ganer/GANER_SLUG/`
- Serial Ganer Detal: `http://127.0.0.1:8000/serial/ganer/GANER_SLUG/` 
