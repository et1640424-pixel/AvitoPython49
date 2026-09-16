from rest_framework import serializers
from .models import Profile, Category, SubCategory, Product, ProductImage, Review, Cart, CartItem, Favorite, FavoriteItem
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('email', 'username', 'password', 'phone_number', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = Profile(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})



        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']

class UserProfileListSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'username', 'date_joined', 'avatar', 'status']

class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'avatar']

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image']

class SubCategorySerializerForCategory(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['SubCategory_name', 'SubCategory_image']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategorySerializerForCategory(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'category_image', 'category_sub']

class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'category_image']

class SubCategoryListSerializer(serializers.ModelSerializer):
    category_name = CategorySimpleSerializer()
    class Meta:
        model = SubCategory
        fields = ['id', 'category_name', 'SubCategory_name', 'SubCategory_image']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ["id", "comment", "review_image", "stars", "crate_date", "user"]

class ProductListSerializer(serializers.ModelSerializer):
    SubCategory = SubCategoryListSerializer()
    product_img = ProductImageSerializer(many=True, read_only=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'get_avg_rating', 'get_count_people', 'price', 'product_img', 'SubCategory']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

class SubCategoryDefaultSerializer(serializers.ModelSerializer):
    category_name = CategorySimpleSerializer()
    sub_category = ProductListSerializer
    class Meta:
        model = SubCategory
        fields = ['category_name', 'SubCategory_name', 'SubCategory_image']

class ProductDefaultSerializer(serializers.ModelSerializer):
    product_img = ProductImageSerializer(many=True, read_only=True)
    product_reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'product_img', 'product_description',
                  'price', 'product_type', 'product_reviews', 'article_number', 'crate_date']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    class Meta:
        model = FavoriteItem
        fields = ['id', 'product', 'product_id']

class FavoriteSerializer(serializers.ModelSerializer):
    favorite_item = FavoriteItemSerializer(read_only=True, many=True)
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_item']
