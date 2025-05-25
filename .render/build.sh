#!/usr/bin/env bash
apt-get update && apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-kaz
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
