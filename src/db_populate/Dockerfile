FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY . .
RUN ln -s /app/db_config.json /app/populate_db/db_config.json
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["bash", "entry.sh"]
