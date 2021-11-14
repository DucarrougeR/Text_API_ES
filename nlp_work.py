import os
from collections import Counter
from loguru import logger
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import nlpcloud
import nltk
nltk.download('punkt')
nltk.download('stopwords')


class TextSummary():
    """Run Pegasus model for document Abstractive Summarization."""

    def __init__(self) -> None:
        self.client = nlpcloud.Client(
            "pegasus-xsum", os.environ["NLPCLOUD_TOKEN"])

    def summarize_text_entry(self, string_data: str) -> str:
        """Text Summarization for Document content.

        Args:
            string_data: the string content of the document posted to ElasticSearch.

        Returns:
            The summary of the input string or the most frequent token in the text.
        """
        if string_data:
            logger.info("Processing summary for input.")
            result = self.client.summarization(string_data)["summary_text"]
            if result:
                return result
            else:
                logger.log(f"NLPcloud API encountered error.")
                stop_words = set(stopwords.words('english'))
                word_tokens = word_tokenize(string_data)
                words_only = [w for w in word_tokens if w.isalnum()]
                cleaned_sentence = [
                    w for w in words_only if not w.lower() in stop_words]
                return Counter(cleaned_sentence).most_common(1)

        else:
            logger.error("Error Processing summary for input.")
            return "Summary not processed for the document yet."
