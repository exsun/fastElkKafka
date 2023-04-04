from fastapi import FastAPI
from loguru import logger
from elasticsearch import Elasticsearch, helpers

app = FastAPI()

#es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])

es_client = Elasticsearch(["http://elasticsearch:9200"])


es_client = Elasticsearch(
                hosts=['http://elasticsearch:9200'],
                http_auth=('elastic', 'ctx1iJ2MF6*ptA*OQKEa')
            )
if es_client.ping():
    print("Elasticsearch cluster is up and running!")
else:
    print("Connection failed.")
#Define a helper function to bulk insert logs into Elasticsearch
def insert_logs_into_logstash(logs):
    print(es_client.__dict__)
    index_name = 'app_logs'
    actions = [
        {
            "_index": index_name,
            "_source": { **log }

        } for log in logs
    ]
    response = helpers.bulk(es_client, actions, index=index_name)
    logger.info(f"Inserted {len(logs)} logs into Elasticsearch. Response: {response}")

# Define a route for logging messages
@app.get("/log/{message}")
async def log_message(message: str):
    # Log using both FastAPI's logger and Loguru's logger
    logger.info(message)
    return {"message": message}

# Define a route for generating logs
@app.get("/generate-logs")
async def generate_logs():
    logs = [
        {"message": "This is log number 1"},
        {"message": "This is log number 2"},
        {"message": "This is log number 3"}
        ]
    insert_logs_into_logstash(logs)
    return {"message": "Logs generated and sent to Elasticsearch"}

@app.get('/search/{query}')
async def search(query: str):
    res = es_client.search(index='app_logs', body={'query': {'match': {'my_field': query}}})
    hits = [hit['_source'] for hit in res['hits']['hits']]
    return {'hits': hits}

# Configure the loggers to write to both the console and Elasticsearch
logger.add(insert_logs_into_logstash, format="{time} {level} {message}", level="INFO")

