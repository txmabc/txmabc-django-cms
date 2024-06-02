FROM python:3.10.5
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install --upgrade pip
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
RUN rm -rf /code
COPY . /code
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]