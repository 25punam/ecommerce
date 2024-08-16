
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
            
            ProductModel.objects.create(
                name=name,
                desc=desc,
                price=price,
                image=image
            )
            
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
@api_view(["POST"])
def delete_product(request):
    if request.method == "POST":
        try :
            ProductModel.objects.filter(name=request.data["name"]).delete()

            return Response("Product delete successfully",status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)
        

