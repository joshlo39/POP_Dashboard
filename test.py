from utils import *
# Usage
# Usage example
file_path = "test_hyperlink.pdf"
url = "https://www.example.com"
text = "Click here for Example"
#x, y= 100, 750  # Coordinates on the PDF pagea
#create_pdf_with_hyperlink_test(file_path, url, text, x, y)
x = ["image_2.png", "image_3.png", "image_4.png","image_100.png","image_1.png","image_99.png"]

x = sorted(x, key=lambda x: int(x.split("_")[1].split(".")[0]))
print(x)