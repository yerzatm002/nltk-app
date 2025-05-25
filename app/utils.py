import os
from pdf2image import convert_from_path
import pytesseract
from nltk.tokenize import word_tokenize, sent_tokenize
from PIL import Image, ImageEnhance, ImageFilter
import re

# Пути к Poppler и Tesseract
POPPLER_PATH = r'C:\Program Files\poppler\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Предобработка изображения
def preprocess_image(image):
    image = image.convert('L')  # Конвертация в оттенки серого
    image = image.filter(ImageFilter.SHARPEN)  # Увеличение резкости
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Увеличение контраста
    return image

# Очистка текста
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # Удаление знаков препинания
    text = re.sub(r'\s+', ' ', text).strip()  # Удаление лишних пробелов
    return text

# Токенизация текста
def tokenize_text(text):
    sentences = sent_tokenize(text, language="russian")
    words = [word_tokenize(sentence, language="russian") for sentence in sentences]
    return sentences, words

# Удаление суффиксов
def remove_suffix(word, suffixes):
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

# Лемматизация слов
def lemmatize_words(words):
    suffixes = ['лар', 'лер', 'дар', 'дер', 'тар', 'тер', 'дың', 'дің', 'тың', 'тің']
    lemmatized = []
    for word_list in words:
        lemmatized.append([remove_suffix(word, suffixes) for word in word_list])
    return lemmatized

# Сохранение текста в файл
def save_to_txt(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

# Основная функция обработки PDF
def process_pdf(pdf_path, output_folder):
    """
    Обрабатывает PDF файл:
    1. Конвертирует страницы PDF в изображения.
    2. Извлекает текст с помощью OCR.
    3. Обрабатывает текст (очистка, токенизация, лемматизация).
    4. Сохраняет результат в формате TXT.
    """
    try:
        # Конвертация PDF в изображения
        images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
        text = ""

        # Извлечение текста с каждой страницы
        for page_number, image in enumerate(images, start=1):
            print(f"Обработка страницы {page_number} PDF")
            image = preprocess_image(image)
            text += pytesseract.image_to_string(image, lang="kaz+eng")

        # Очистка, токенизация и лемматизация текста
        cleaned_text = clean_text(text)
        _, words = tokenize_text(cleaned_text)
        lemmatized_words = lemmatize_words(words)
        processed_text = "\n".join([" ".join(word_list) for word_list in lemmatized_words])

        # Сохранение обработанного текста в TXT файл
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(pdf_path))[0] + '_processed.txt')
        save_to_txt(processed_text, output_file)

        print(f"Обработанный файл сохранен: {output_file}")
        return output_file
    except Exception as e:
        print(f"Ошибка при обработке PDF: {e}")
        return None
