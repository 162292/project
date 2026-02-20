from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Customer,Order


# # ---------------- PRODUCT LIST ----------------
def product_list(request):

    # Fetch all products
    products = Product.objects.all()

    return render(request, "myapp/product_list.html", {"products": products})


# # ---------------- ADD PRODUCT ----------------
def add_product(request):

    if request.method == "POST":

        # Get form data
        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        # Create product in database
        Product.objects.create(
            name=name,
            category=category,
            price=price,
            stock=stock
        )

        # Redirect avoids duplicate submission
        return redirect("product_list")

    return render(request, "myapp/product_form.html")


# # ---------------- EDIT PRODUCT ----------------
def edit_product(request, id):

    # Get product by ID
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":

        # Update values
        product.name = request.POST.get("name")
        product.category = request.POST.get("category")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")

        # Save updated data
        product.save()

        return redirect("product_list")

    return render(request, "myapp/product_form.html", {"product": product})


# # ---------------- DELETE PRODUCT ----------------
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)
    product.delete()

    return redirect("product_list")


# # ---------------- ADD CUSTOMER ----------------
def add_customer(request):

    if request.method == "POST":

        Customer.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            city=request.POST.get("city"),
        )

        return redirect("product_list")

    return render(request, "myapp/customer_form.html")


# # ---------------- ADD ORDER ----------------
def add_order(request):

    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == "POST":

        customer_id = request.POST.get("customer")
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")

        # -------- VALIDATION --------
        if not quantity:
            return redirect("add_order")

        try:
            quantity = int(quantity)
        except ValueError:
            return redirect("add_order")

        product = Product.objects.get(id=product_id)

        # -------- STOCK CHECK --------
        if product.stock >= quantity:

            # Create order
            Order.objects.create(
                customer_id=customer_id,
                product_id=product_id,
                quantity=quantity
            )

            # Reduce stock
            product.stock -= quantity
            product.save()

        return redirect("order_list")

    return render(request, "myapp/order_form.html", {
        "customers": customers,
        "products": products
    })



# ---------------- VIEW ORDERS ----------------
def order_list(request):

    # select_related improves query performance
    orders = Order.objects.select_related("customer", "product")

    return render(request, "myapp/order_list.html", {"orders": orders})
