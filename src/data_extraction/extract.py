import fitz
import os
import pandas as pd
import json
import easyocr
from utils import clean_text

reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.
    Returns:
        str: Extracted text from the PDF.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        doc = fitz.open(file_path)
        text = ""
    except Exception as e:
        raise ValueError(f"Could not open the PDF file: {e}")
    for page_num in range(len(doc)):
        page = doc[page_num]
        text += page.get_text()

    return text


def extract_text_from_structured_file(file_path):
    """
    Extract text from a structured file.

    Args:
        file_path (str): The path to the structured file.

    Returns:
        str: Extracted text from the structured file.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    elif ext == ".json":
        try:
            df = pd.read_json(file_path)
        except ValueError:
            with open(file_path, "r") as file:
                data = json.load(file)
            df = pd.json_normalize(data)
    df = df.describe()
    df = df.to_string(index=False)
    return df


def extract_text_from_image(file_path):
    """
    Extract text from an image file using OCR.

    Args:
        file_path (str): The path to the image file.

    Returns:
        str: Extracted text from the image.
    """
    result = reader.readtext(file_path, detail=0)
    data = "\n".join(result)
    return data


def extract_text_from_text_files(file_path):
    """
    Extraxt text from .txt , .md , .docx format files

    Args:
        file_path (str): The path to the image file.

    Returns:
        str: Extracted text from the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data
    except Exception as e:
        raise ValueError(f"Could not read the text file: {e}")


def extract_text(file_path):
    """
    Extract text from a file based on its type.

    Args:
        file_path (str): The path to the file.

    Returns:
        str or pd.DataFrame: Extracted text or data from the file.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".csv", ".xls", ".xlsx", ".json"]:
        return extract_text_from_structured_file(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    elif ext in [".txt", ".md", ".docx"]:
        return extract_text_from_text_files(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def extract_multiple_forms(file_paths):
    """
    Extract text from multiple files.

    Args:
        file_paths (list): List of file paths to extract text from.

    Returns:
        dict: A dictionary with file names as keys and extracted text/data as values.
    """
    results = {}
    for path in file_paths:
        try:
            extracted_data = extract_text(path)
            extracted_data = clean_text(extracted_data)
            results[os.path.basename(path)] = extracted_data
        except Exception as e:
            print(f"[ERROR] Failed to process {path}:{e}")
            results[os.path.basename(path)] = None
    return results
