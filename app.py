from flask import Flask, render_template, request
import requests
import logging
import time
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SummarizerConfig:
    """Configuration for Hugging Face summarizer."""
    API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    API_TOKEN = os.getenv("HF_API_TOKEN")  # Loaded from Render environment variable
    MIN_LENGTH = 20
    MAX_LENGTH = 200
    MAX_RETRIES = 2
    RETRY_DELAY = 3
    REQUEST_TIMEOUT = 15

class TextSummarizer:
    def __init__(self, config: SummarizerConfig):
        self.config = config
        self.headers = {"Authorization": f"Bearer {config.API_TOKEN}"}
        self.last_request_time = 0
        self.rate_limit_delay = 1

    def _check_rate_limit(self):
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def _handle_model_loading(self, response: requests.Response) -> bool:
        try:
            response_json = response.json()
            if isinstance(response_json, dict) and "loading" in response_json.get("error", "").lower():
                logger.warning("Model loading... retrying")
                time.sleep(self.config.RETRY_DELAY)
                return True
            return False
        except Exception:
            return False

    @retry(stop=stop_after_attempt(SummarizerConfig.MAX_RETRIES),
           wait=wait_exponential(multiplier=1, min=3, max=10))
    def _make_api_request(self, payload: dict) -> dict:
        self._check_rate_limit()

        response = requests.post(
            self.config.API_URL,
            headers=self.headers,
            json=payload,
            timeout=self.config.REQUEST_TIMEOUT
        )

        logger.info(f"HF API {response.status_code}: {response.text}")
        if response.status_code == 503 or self._handle_model_loading(response):
            raise requests.exceptions.RequestException("Model loading")
        response.raise_for_status()
        return response.json()

    def summarize(self, text: str, max_length: int) -> dict:
        try:
            payload = {
                "inputs": text,
                "parameters": {
                    "min_length": self.config.MIN_LENGTH,
                    "max_length": max_length
                }
            }
            output = self._make_api_request(payload)

            if isinstance(output, list) and output and "summary_text" in output[0]:
                return {"success": True, "summary": output[0]["summary_text"]}
            else:
                return {"success": False, "error": f"Unexpected API response: {output}"}
        except Exception as e:
            logger.error("Summarization error", exc_info=True)
            return {"success": False, "error": str(e)}

# ---------------------- Flask App ----------------------
app = Flask(__name__)
summarizer = TextSummarizer(SummarizerConfig())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result="")

@app.route("/summer", methods=["POST"])
def summer():
    try:
        text = request.form.get("data", "").strip()
        if not text:
            return render_template("index.html", result="⚠️ Please provide text to summarize.")

        max_length = int(request.form.get("maxl", SummarizerConfig.MAX_LENGTH))
        max_length = min(max(max_length, SummarizerConfig.MIN_LENGTH), SummarizerConfig.MAX_LENGTH)

        result = summarizer.summarize(text, max_length)
        return render_template("index.html", result=result["summary"] if result["success"] else result["error"])
    except Exception as e:
        logger.error("Flask route error", exc_info=True)
        return render_template("index.html", result=f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
