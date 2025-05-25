#!/usr/bin/env bash
apt-get update && apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-kaz
pip install -r requirements.txt
python -m nltk.downloader punkt
