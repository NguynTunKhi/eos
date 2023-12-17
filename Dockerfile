FROM python:2.7

WORKDIR /app

COPY . .
RUN unzip ./gluon.zip
RUN pip install -r applications/eos/requirements.txt
CMD python2 web2py.py --nogui -a admin -i 0.0.0.0 -p 8000


