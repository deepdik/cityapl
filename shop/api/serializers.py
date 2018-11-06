import re
from datetime import datetime
from django.core.mail import send_mail,send_mass_mail
from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
	DateTimeField,
	SlugField,
	ValidationError,
	EmailField, 
	CharField,
	Serializer,
	)

from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .fields import DistanceField
from shop.models import (
	City,
	Category,
	SubCategory,
	Shop,
	FilterTag,
	Feedback,
	ShopRating,
	Vote,
	Pricing,
	)

from accounts.api.serializers import UserDetailSerializer



# url = HyperlinkedIdentityField(
# 		view_name = '',
# 		lookup_field = ''
# 	)

class CityListSerializer(ModelSerializer):
	class Meta:
		model = City
		fields = [
			'id',
			'city',
			'state',
			'country',
			'cityImg',
		]

class CityDetailSerializer(ModelSerializer):
	class Meta:
		model = City
		fields = [
			'city',
			'state',
			'country',
			'cityImg',
		]


class CategoryListSerializer(ModelSerializer):
#	subcategory_set = SubCategoryListSerializer(many=True)
	class Meta:
		model = Category
		fields = [
			'name',
			'catImg',
			'id',
		]

class CategoryDetailSerializer(ModelSerializer):
	class Meta:
		model = Category
		fields = [
			'name',
			'desc',
			'catImg'
		]

class CategorySerializerHelper(ModelSerializer):
	class Meta:
		model = Category
		fields = [
			'id',
			'name',
		]

class SubCategorySerializerHelper(ModelSerializer):
	class Meta:
		#this is correct please dont change this
		model = Category
		fields = [
			'id',
			'name',
		]

class SubCategoryListSerializer(ModelSerializer):
	category = CategorySerializerHelper()
	class Meta:
		model = SubCategory
		fields = [
			'category',
			'id',
			'name',
			'subCatImg'
		]

class SubCategoryDetailSerializer(ModelSerializer):
	class Meta:
		model = SubCategory
		fields = [
			'category',
			'name',
			'desc',
			'subCatImg'
		]

class FilterListSerializer(ModelSerializer):
	class Meta:
		model = FilterTag
		fields = ['tag',]

class ShopListSerializer(ModelSerializer):
	distance = SerializerMethodField()
	isOpen = SerializerMethodField('isOpenShop')
	isLiked = SerializerMethodField()
#	url = HyperlinkedIdentityField(view_name='shop-api:detailshop',lookup_field='slug')
#	category = CategorySerializerHelper()
#	subCategory = SubCategorySerializerHelper(many=True)
	city = CityListSerializer()
	filterTags = FilterListSerializer(many=True)
	thumbnail = SerializerMethodField()

	
	def get_distance(self, obj):
		distance = getattr(obj, "distance", None)
		return DistanceField(unit='m').to_representation(distance)
	

	def isOpenShop(self,instance):
		closingDay = instance.closingDay.lower()
		today = datetime.today().strftime("%A").lower()
		timeNow = datetime.now().time()
		if (closingDay != today) and instance.openingTime <= timeNow <= instance.closingTime:
			return True
		else:
			return False

	def get_isLiked(self,obj):
		user_ = self.context['request'].user
		if user_.is_authenticated():
			shop = obj.id
			vote = 0
			userVote = Vote.objects.filter(user=user_,shop=shop)
			
			if userVote.exists() and userVote.count() == 1:
				userVote = userVote.first()
				liked = userVote.liked
				if liked == True:
					vote = 1
				elif liked == False:
					vote = -1
				else:
					vote = 0
				return vote
		return 0

	def get_thumbnail(self,instance):		
		thumbnail = instance.banner_thumbnail.url
		return thumbnail


	class Meta:
		model = Shop
	#	geo_field = "location"
		fields = [
			'id',
			'shopName',
			'slug',
			'bannerImage',
			'thumbnail',
			'mobileNo',
			'alternateMobileNo',
			'rating',
			'likes',
			'dislikes',
			'tagline',
			'isOpen',
			'isLiked',
			'distance',
			'category',
			'subCategory',
			'filterTags',
			'location',
			'city',
			]

class FeedbackListSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	timestamp = DateTimeField(read_only=True)
	class Meta:
		model = Feedback
		fields = [
		'user',
		'content',
		'timestamp'
		]

class FeedbackSerializer(ModelSerializer):
	user = UserDetailSerializer(read_only=True)
	timestamp = DateTimeField(read_only=True)
	shopSlug = SlugField(write_only=True)
	
	def validate_shopSlug(self, slug):
		shop_qs = Shop.objects.filter(slug=slug)
		if shop_qs.exists() and shop_qs.count() == 1:
			return shop_qs.first()
		raise ValidationError('Sorry cannot find the shop you are commentig on')

	def create(self,validate_data):
		shopSlug = validate_data['shopSlug']
		shop = validate_data['shopSlug']
		content = validate_data["content"]
		user = self.context['request'].user
#		print ("hello")
#		print (self.context['request'].COOKIES['token'])
#		print(self.context['request'].META['REMOTE_ADDR'])
		return Feedback.objects.create(
			user = user,
			shop = shop,
			content=content
			)
	class Meta:
		model = Feedback
		fields = [
		'shopSlug',
		'user',
		'content',
		'timestamp'
		]


class ShopDetailSerializer(ModelSerializer):
	isLiked = SerializerMethodField()
	feedback = SerializerMethodField()
	city = CityListSerializer()
	category = CategorySerializerHelper()
	subCategory = SubCategorySerializerHelper(many=True)
	filterTags = FilterListSerializer(many=True)
	isOpen = SerializerMethodField('isOpenShop')
	
	
	def isOpenShop(self,instance):
		 
		closingDay = instance.closingDay.lower()
		today = datetime.today().strftime("%A").lower()
		timeNow = datetime.now().time()
		if (closingDay != today) and instance.openingTime <= timeNow <= instance.closingTime:
			return True
		else:
			return False

	def get_feedback(self,instance):
		obj = Feedback.objects.filter(shop__slug=instance.slug).order_by('-timestamp')
		data = FeedbackListSerializer(obj,many=True).data
		return data
	def get_isLiked(self,obj):
		user_ = self.context['request'].user
		if user_.is_authenticated():
			shop = obj.id
			print (shop)
			vote = 0
			userVote = Vote.objects.filter(user=user_,shop=shop)
			if userVote.exists() and userVote.count() == 1:
				userVote = userVote.first()
				liked = userVote.liked
				if liked == True:
					vote = 1
				elif liked == False:
					vote = -1
				else:
					vote = 0
				return vote
		return 0


	
	



	class Meta:
		model = Shop
		fields = [
		'isLiked',
		'id',
		'shopName',
		'isOpen',
		'category',
		'subCategory',
		'filterTags',
		'city',
		'slug',
		'bannerImage',
	



		'rating',
		'likes',
		'dislikes',
		'tagline',
		'mobileNo',
		'alternateMobileNo',
		'email',
		'ownerName',
		'shopAddress',
		'shopPinCode',
		'mobileNo',
		'openingTime',
		'closingTime',
		'feedback',
		'location',
		'pricingTabName',
		]
		


class VoteSerializer(ModelSerializer):

	class Meta:
		model = Vote
		fields = ['liked','shop']

class RatingSerializer(ModelSerializer):
	class Meta:
		model = ShopRating
		fields = ['shop', 'user', 'rating']

class FreeListingSerializer(Serializer):
	email = EmailField()
	mobileNo = CharField()
	city = CharField()
	def validate_email(self, email):
		allowedDomains = [
		"aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
		"google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
		"live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
		"email.com", "games.com" , "gmx.net", "hush.com", "hushmail.com", "icloud.com", "inbox.com",
		"lavabit.com", "love.com" , "outlook.com", "pobox.com", "rocketmail.com",
		"safe-mail.net", "wow.com", "ygm.com" , "ymail.com", "zoho.com", "fastmail.fm",
		"yandex.com","iname.com"
		]
		domain = email.split("@")[1]
		if domain not in allowedDomains:
			raise ValidationError('Invalid email address')
		return email

	def validate_mobileNo(self,mobileNo):
		pattern = re.compile(r"^[987][0-9]{9}$")
		if pattern.match(mobileNo):
			return mobileNo
		else:
			raise ValidationError('Please correct the format of Mobile Number')

	def save(self):
		email = self.validated_data['email']
		mobileNo = self.validated_data['mobileNo']
		city = self.validated_data['city']
		messageToCityapl = "Email :"+str(email)+" Contact Number " + str(mobileNo)+" City " + str(city)
		messageToSender = "Thankyou for showing your interest in  CityAPL. We successfully received your details. We will get in touch with you very soon."
		mail1 = (
			'CTIYAPL, NEW USER IS INTRESTED IN LISTING HIS SHOP',
			messageToCityapl,
			'contact@cityapl.com',
			['arpt.svt@gmail.com',],
			)
		
		mail2 = (
			'CTIYAPL, Your request for shop listing is received',
			messageToSender,
			'contact@cityapl.com',
			[email,],
			)
		send_mass_mail((mail1, mail2), fail_silently=False)



class PricingSerializer(ModelSerializer):
	class Meta:
		model = Pricing
		fields = ['shop','name','price']