import cv2
import pytesseract


def get_text(image):
    options = "--psm 4"
    # options = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB), config=options, lang="kor"
    )
    text = text.replace(" ", "").replace("\n", "").replace("|", "").strip()
    return text
