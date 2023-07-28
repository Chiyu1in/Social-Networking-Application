FROM python:3.9

WORKDIR /code
RUN pip install --no-cache-dir --upgrade locust
COPY . .

EXPOSE 8089
CMD [ "locust", "-f", "locustfile.py", "-H", "https://ptt-server-stage.azurewebsites.net", "--autostart", "-u", "10", "-t", "1800"]