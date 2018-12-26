FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN ls -l

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -l

RUN pip install ./en_core_web_sm-2.0.0.tar.gz

CMD [ "python", "app.py" ]
