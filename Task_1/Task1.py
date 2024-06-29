from PIL import Image
import pytesseract
import sys

def extract_text(image_path):
    
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Task_1.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        extracted_text = extract_text(image_path)
        print("Extracted Text:")
        print(extracted_text)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
