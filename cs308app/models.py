from django.db import models

# Create your models here.

# Entities from here


class User(models.Model):

    USER_TY = (
        ('Customer', 'Customer'),
        ('Sales Manager', 'Sales Manager'),
        ('Product Manager', 'Product Manager'),
    )

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=50, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=14, null=True)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    user_exists = models.BooleanField(default=True)
    # logged-in or not, sales and product manager
    user_type = models.CharField(max_length=20, choices=USER_TY, default='Customer')

    def __str__(self):
        return "%s" % (self.user_id)


class Product(models.Model):

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()
    real_stock = models.IntegerField()
    img = models.CharField(max_length=400, null=True)
    rating = models.FloatField()
    brand_name = models.CharField(max_length=30)
    recommended = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    base_price = models.FloatField()
    discount=models.BooleanField()
    viewed = models.IntegerField(default=0)
    def __str__(self):
        return "%s" % (self.product_id)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=25)
    address_line = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)
    address = models.ForeignKey(
        Address, null=False, on_delete=models.DO_NOTHING)
    total_price = models.FloatField()
    allDelivered = models.BooleanField(default=False)
    cancelled=models.BooleanField(default=False)
    
class OrderAddressChange(models.Model):
    orderadresschange_id=models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,null=True,on_delete=models.DO_NOTHING)
    verified=models.BooleanField(default=False)

class OrderItem(models.Model):
    GETTING_PREPARED = 0
    ON_DELIVERY = 1
    DELIVERED = 2
    CANCELLED = 3

    ORDER_STATUS = (
        (GETTING_PREPARED, 'Getting Prepared'),
        (ON_DELIVERY, 'On Delivery'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    )
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, null=False, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(
        Product, null=False, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    status = models.IntegerField(default=GETTING_PREPARED, choices=ORDER_STATUS)


class BasketItem(models.Model):

    basket_item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    rating = models.FloatField()
    validation = models.BooleanField(default=False)
    nickname = models.TextField()
    user_id=models.ForeignKey(User,null=False,on_delete=models.CASCADE)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

class CampaignInfo(models.Model):
    campaing_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=60)
    description=models.CharField(max_length=250)
    discount_rate=models.FloatField()

class OrderCancel(models.Model):
    ordercancel_id=models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,null=False,on_delete=models.CASCADE)

class Campaignitems(models.Model):
    campaignitems_id=models.AutoField(primary_key=True)
    product=models.ForeignKey(Product,null=False,on_delete=models.CASCADE)
    campaigninfo=models.ForeignKey(CampaignInfo,null=False,on_delete=models.CASCADE)

# Relationships from here


class ProductCategory(models.Model):
    procat_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)


class Photos(models.Model):
    photos_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, null=False, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=600)


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, null=False, on_delete=models.CASCADE)
