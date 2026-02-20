from django.db import models


#  ---------------- PRODUCT MODEL ----------------
class Product(models.Model):

    # Product name must be unique
    name = models.CharField(max_length=100, unique=True)

    category = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

    def __str__(self):
        return self.name


# # ---------------- CUSTOMER MODEL ----------------
class Customer(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# # ---------------- ORDER MODEL ----------------
class Order(models.Model):

    # ForeignKey creates relationship
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    # Automatically store order date
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"
