echo "BUILD START..."

# create a virtual environment named 'venv' if it doesn't already exist
python3 -m venv .venv

# activate the virtual environment
source .venv/bin/activate

# install the required packages
# pip install -r requirements.txt
pip install \
    django \
    django-cors-headers \
    djangorestframework \
    djangorestframework-simplejwt \
    django-allauth[socialaccount,mfa] \
    django-rest-auth \
    django-environ \
    pyJWT \
    psycopg2-binary \
    twilio \
    sendgrid \
    gunicorn

python3 manage.py collectstatic --noinput


echo "...BUILD END"

echo "SPINNING UP THE SERVER..."

python3 manage.py makemigrations
python3 manage.py migrate

# python3 ./manage.py runserver

# [optional] Start the application here 
# python manage.py runserver
