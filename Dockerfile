FROM ubuntu:latest
LABEL authors="Vera Grosskop"

ENTRYPOINT ["top", "-b"]

#Use python 3.13 slim image as base
FROM python:3.13-slim

#set working directory in docker container
WORKDIR /app

#copy requirements.txt
COPY requirements.txt .

#install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy source code
COPY . .

# Expose port
EXPOSE 5000

#Run the application
CMD ["python", "app.py"]

