FROM python:3.11

WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install-deps
RUN playwright install

CMD ["python", "main.py"]