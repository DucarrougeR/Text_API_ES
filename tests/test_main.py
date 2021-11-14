import os
import requests
from elasticsearch import Elasticsearch

from nlp_work import TextSummary


class TestEsDemo:

    def test_es_server(self):
        """Test that ElasticSearch is running."""
        es = Elasticsearch("http://localhost:9200")

        assert es.info()[
            "cluster_name"] == "elasticsearch", "ElasticSeach is not running."


class TestSummarization:

    def test_nlpcloud_creds(self):
        assert os.environ["NLPCLOUD_TOKEN"] is not None

    def test_summarize_text_entry(self):
        """Test the summarization logic to ensure it yields a value."""
        test_string = ("Paris is the capital and most populous city of France,"
                       " with an estimated population of 2,175,601 residents "
                       "as of 2018, in an area of more than 105 square "
                       "kilometres (41 square miles).[4] Since the 17th "
                       "century, Paris has been one of Europe's major centres "
                       "of finance, diplomacy, commerce, fashion, gastronomy, "
                       "science, and arts. The City of Paris is the centre "
                       "and seat of government of the region and province of "
                       "Île-de-France, or Paris Region, which has an estimated"
                       " population of 12,174,880, or about 18 percent of "
                       "the population of France as of 2017")
        summary_maker = TextSummary()
        result = summary_maker.summarize_text_entry(test_string)

        assert result is not None


class TestSquirroDemo:

    doc_to_test = requests.get("http://127.0.0.1:5000/get_docs")

    def test_server(self):
        """Test the Flask application is running."""
        resp = requests.get("http://127.0.0.1:5000/")

        assert resp.status_code == 200, "The Flask App is not running"

    def test_add_text(self) -> str:
        """Test route to add document to ElasticSearch."""
        content_data = (
            "The input should be a string, and must be longer "
            "than ParisParis sentences for the summary to make sense. "
            "The text will be split into sentences using the "
            "split_sentences method in the gensim.summarization.texcleaner"
            " module. Note that newlines divide sentences.")
        test_data = {"text": content_data}

        resp = requests.post("http://127.0.0.1:5000/add_text",
                             data=test_data
                             )
        assert resp.status_code == 200
        assert resp.json()["_id"] is not None
        with open("demofile2.txt", "w") as docs:
            docs.write(resp.json()["_id"])
        assert resp.json()["result"] == "created"

    def test_search_text(self):
        """Test the search route for documents based on keyword."""
        test_data = {"keyword": "ParisParis"}
        resp = requests.post("http://127.0.0.1:5000/search_text",
                             data=test_data)

        assert resp.status_code == 200
        for search_result in resp.json():
            assert search_result["_id"] is not None
        assert "ParisParis" in resp.text

    def test_get_doc(self):
        """Test route retrieving all Document fields by doc_id."""
        doc_to_get = TestSquirroDemo.doc_to_test.json()[-1][0]

        if doc_to_get:
            print(f"Testing test_get_doc for '{doc_to_get}'")
            resp = requests.get(
                f"http://127.0.0.1:5000/get_doc?doc_id={doc_to_get}")

            assert resp.status_code in [200, 404]
            assert resp.json()["_id"] is not None
            assert resp.json()["_index"] == "contents"
            assert resp.json()["found"] is True
        else:
            print("No document to retrieve for test_get_doc()")

    def test_get_doc_summary(self):
        """Test route retrieving Document 'summary' by doc_id."""
        doc_to_get = TestSquirroDemo.doc_to_test.json()[-1][0]

        if doc_to_get:
            print(f"Testing test_get_doc for '{doc_to_get}'")
            resp = requests.get(
                f"http://127.0.0.1:5000/get_doc_summary?doc_id={doc_to_get}"
            )

            assert resp.json()["_id"] is not None
            assert resp.json()["summary"] is not None
        else:
            print("No document to retrieve for test_get_doc_summary()")
