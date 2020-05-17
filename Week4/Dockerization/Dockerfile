FROM python:3.6
RUN mkdir -p /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "hw.py"]
