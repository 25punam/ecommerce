import requests
from django.core.files.base import ContentFile
from products.models import ProductModel

API_URL = "https://dummyjson.com/products?limit=100"

response = requests.get(API_URL)
data = response.json()["products"]

for item in data:
    name = item["title"]
    price = item["price"]
    desc = item["description"]
    image_url = item["thumbnail"]

    product = ProductModel(
        name=name,
        price=price,
        desc=desc,
    )

    # image download
    img = requests.get(image_url)
    if img.status_code == 200:
        file_name = image_url.split("/")[-1]
        product.image.save(file_name, ContentFile(img.content), save=False)

    product.save()

print("✅ Real Products Imported")