FROM python:3.12

WORKDIR /magician

COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod 755 .


ENTRYPOINT [ "python3", "main.py" ]
