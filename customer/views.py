
from products.models import ProductModel 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def create_product(request):
    if request.method == "POST":
        try:
            name = request.data.get("name")
            desc = request.data.get("desc")
            price = request.data.get("price")
            image = request.FILES.get("image")

            ProductModel.objects.create(name=name, desc=desc, price=price, image=image)

            return Response(
                {"message": "Product created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def delete_product(request):
#     if request.method == "POST":
#         try:
#             ProductModel.objects.filter(name=request.data["name"]).delete()

#             return Response("Product delete successfully", status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE", "POST"])
def delete_product(request, id=None):
    # 1. id either from URL or body
    product_id = id or request.data.get("id")

    if not product_id:
        return Response(
            {"error": "Product ID is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. delete safely (no crash even if not found)
    deleted_count, _ = ProductModel.objects.filter(id=product_id).delete()

    # 3. idempotent response (important)
    if deleted_count == 0:
        return Response(
            {"message": "Product already deleted or not found"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": "Product deleted successfully"},
        status=status.HTTP_200_OK
    )