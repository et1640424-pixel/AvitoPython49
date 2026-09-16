from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

ROLE_CHOICES = (
('gold', 'Gold'),
('silver', 'Silver'),
('bronze', 'Bronze'),
('simple', 'Simple'),
)


class Profile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(18)],
                                      null=True, blank=True)
    phone_number = PhoneNumberField(default="+996")
    avatar = models.ImageField(upload_to="Profile_images/", null=True, blank=True)
    status = models.CharField(choices=ROLE_CHOICES, default='simple', max_length=10)

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="Category_images/")
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub')
    SubCategory_name = models.CharField(max_length=65, unique=True)
    SubCategory_image = models.ImageField(upload_to="SubCategory_images/")
    def __str__(self):
        return self.SubCategory_name

class Product(models.Model):
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category')
    product_name = models.CharField(max_length=40)
    product_description = models.TextField(max_length=500)
    product_image = models.ImageField(upload_to="Product_images/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.BooleanField(default=True)
    article_number = models.PositiveIntegerField(unique=True)
    crate_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        ratings = self.product_reviews.all()
        if ratings.exists():
            return round(sum([i.stars for i in ratings]) / len(ratings), 1)
        return 0

    def get_count_people(self):
        return self.product_reviews.count()

class ProductImage(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    product_image = models.ImageField(upload_to="product_images/")

class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    comment = models.TextField(null=True, blank=True)
    review_image = models.ImageField(upload_to="review_images/", null=True, blank=True)
    stars = models.PositiveIntegerField(choices=[(i, str(i))for i in range(1, 6)])
    crate_date = models.DateField(auto_now_add=True)

class Cart(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.item.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


