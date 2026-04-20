# 


import json
import requests
from django.core.files.base import ContentFile
from products.models import ProductModel

with open("products.json") as f:
    data = json.load(f)

for item in data:
    image_url = item["image"]
    image_name = image_url.split("/")[-1]

    try:
        response = requests.get(image_url)
    except:
        response = None

    product = ProductModel(
        name=item["name"],
        price=item["price"],
        desc=item["description"]
    )

    if response and response.status_code == 200:
        product.image.save(image_name, ContentFile(response.content), save=False)

    product.save()

print("Data inserted successfully")