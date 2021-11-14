import json
from datetime import datetime
from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch
from loguru import logger
from nlp_work import TextSummary


es = Elasticsearch("http://localhost:9200")

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Hello Squirro's Challenge"


@app.route('/get_docs', methods=['GET'])
def get_docs():
    """Retrieve the `id` and content for all documents."""
    result = es.search(index="contents",
                       doc_type="_doc",
                       body={
                           'size': 100,
                           'query': {
                               'match_all': {}
                           }
                       })
    if result:
        specific_info = []
        for doc in result['hits']['hits']:
            specific_info.append([doc['_id'], doc['_source']])
        result = Response(json.dumps(specific_info),
                        mimetype='application/json')
    else:
        result = jsonify('All documents not found')
        result.status_code = 500

    return result


@app.route('/get_doc', methods=['GET'])
def get_doc():
    """Retrieve all fields for all documents."""
    doc_id = request.args.get('doc_id')

    if doc_id:
        result = es.get(index="contents", id=str(doc_id))
        logger.info(result)
        result = jsonify(result)
    else:
        result = jsonify('Parameter "doc_id" not found in query string')
        result.status_code = 500

    return result


@app.route('/get_doc_summary', methods=['GET'])
def get_doc_summary():
    """Retrieve the `id` and `summary` for a document."""
    doc_id = request.args.get('doc_id')
    if doc_id:
        result = es.get(index="contents", id=str(doc_id))
        logger.info(result)
        result = jsonify(
            {"_id": result["_id"], "summary": result["_source"]["summary"]})
    else:
        result = jsonify('Parameter "doc_id" not found in query string')
        result.status_code = 500

    return result


@app.route('/add_text', methods=['POST'])
def add_text():
    """Add the document from user request."""
    text = request.form['text']

    if text:
        summary_maker = TextSummary()
        summary = summary_maker.summarize_text_entry(text)

        if not summary:
            logger.exception("No summary generated for document entry")

        body = {
            "text": text,
            "summary": summary,
            "timestamp": datetime.now()
        }
        result = es.index(index='contents', doc_type='_doc', body=body)
        logger.info(result)
        result = jsonify(result)

    else:
        result = jsonify("Parameter 'text' not found in request")
        result.status_code = 500

    return result


@app.route('/search_text', methods=['POST'])
def search_text():
    """Retrieve the documents from user specific `keyword`."""
    keyword = request.form['keyword']
    if keyword:
        body = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["text"]
                }
            }
        }

        result = es.search(index="contents", doc_type="_doc", body=body)
        logger.info(result)
        result = jsonify(result['hits']['hits'])
    else:
        result = jsonify("Parameter 'keyword' not found in request")
        result.status_code = 500

    return result


if __name__ == "__main__":
    app.run(port=5000, debug=True)
