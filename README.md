#


## Set Up

1. Download ElasticSearch for Linux [Link](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.2-linux-x86_64.tar.gz) and extract the `tar.gz` file.
2. Create an Environment Variable for the [NLP Cloud API](https://nlpcloud.io/) `NLPCLOUD_TOKEN`
3. Install the dependencies `$ pip3 install -r requirements.txt`
4. Run ElasticSearch `cd elasticsearch-7.15.2` and then `$ bin/elasticsearch`. It will run on the default `http://localhost:9200`.

## Testing

Run the Flask app `$ python3 main.py`
Run tests with `$ pytest -vs`

## Running the Demo

Run the Flask app `$ python3 main.py`
The server will run on the default `http://127.0.0.1:5000/`

You can manually add a document with the following command:

```
curl -X POST "localhost:9200/contents/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
  "content_data": "London is the capital and largest city of England and the United Kingdom. Standing on the River Thames in south-east England at the head of a 50-mile (80 km) estuary down to the North Sea, it has been a major settlement for two millennia. The City of London, its ancient core and financial centre, was founded by the Romans as Londinium and retains boundaries close to its medieval ones."
}
'
```

This will return the `_id` of the created document that can be used in the routes below.

You can check the routes:

- [Home](http://127.0.0.1:5000/)
- GET all created docs [`/get_docs`](http://127.0.0.1:5000/get_docs)
- GET all info about a document [`/get_doc/doc_id=`](http://127.0.0.1:5000/get_doc?doc_id=27vAFX0Bxzluzn2kHfx7)
- GET summary about a document[`/get_doc_summary?doc_id=`](http://127.0.0.1:5000/get_doc?doc_id=27vAFX0Bxzluzn2kHfx7)
- POST a document `/add_text`
- POST a search request for documents by keyword `/search_text`

