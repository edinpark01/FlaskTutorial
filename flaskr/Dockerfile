FROM centos:latest

WORKDIR /usr/src/app

ENV FLASK_APP=__init__.py
ENV FLASK_ENV=developement

COPY requirements.txt ./

RUN yum -y update
RUN yum -y install centos-release-scl
RUN yum -y install epel-release && yum clean all
RUN yum -y install rh-python36
RUN scl enable rh-python36 bash
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -l

CMD [ "flask", "run" ]
