FROM tiangolo/meinheld-gunicorn-flask:python3.7

RUN pip install --upgrade pip
RUN pip install mysqlclient
# RUN  apt-get install -y python3-dev libpython3-dev python3-mysqldb
RUN pip install -U setuptools
RUN pip install pipenv
# RUN pipenv install --system --deploy

ADD resources /resources/
WORKDIR /resources/
RUN pip install -r requirements.txt


ONBUILD ADD app /app/

WORKDIR /app

CMD ["python", "run.py"]
