FROM python:3.11.5

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./wait-for-it.sh", "db:5432", "--"]
