FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY ./ /app

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]