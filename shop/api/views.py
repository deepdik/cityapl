from django.db.models import F
from rest_framework.generics import (
	ListAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
	RetrieveAPIView
	)

from rest_framework.permissions import (
	IsAuthenticated,
	IsAdminUser,
	AllowAny,
	)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST

from .filters import OrderedDistanceToPointFilter

from shop.models import (
	City,
	Category,
	SubCategory,
	Shop,
	Feedback,
	ShopRating,
	Vote,
	Pricing,
	)

from .serializers import (
	CityListSerializer,
	CityDetailSerializer,
	CategoryListSerializer,
	CategoryDetailSerializer,
	SubCategoryListSerializer,
	SubCategoryDetailSerializer,
	ShopDetailSerializer,
	ShopListSerializer,
	FeedbackListSerializer,
	FeedbackSerializer,
	RatingSerializer,
	VoteSerializer,
	FreeListingSerializer,
	PricingSerializer,
	)

from .pagination import ShortPAginator

from .permissions import IsOwnerOrReadOnly,IsUser


class CityCreateAPIView(CreateAPIView):
	queryset = City.objects.all()
	serializer_class = CityDetailSerializer
	permission_classes = (IsAuthenticated,IsAdminUser)

class CityListAPIView(ListAPIView):
	queryset = City.objects.all()
	serializer_class = CityListSerializer
#	pagination_class = ShortPAginator

class CityUpdateAPIView(UpdateAPIView):
	queryset = City.objects.all()
	serializer_class = CityDetailSerializer
	lookup_field = "id"
	permission_classes = (IsAuthenticated,IsAdminUser)
 
class CityDeleteAPIView(DestroyAPIView):
	queryset = City.objects.all()
	serializer_class = CityDetailSerializer
	lookup_field = "id"
	permission_classes = (IsAuthenticated,IsAdminUser)

class CategoryCreateAPIView(CreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailSerializer
	permissions_classes = (IsAuthenticated,IsAdminUser)

class CategoryListAPIView(ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryListSerializer
	permissions_classes = (IsUser,)

class CategoryUpdateAPIView(UpdateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailSerializer
	lookup_field = "id"
	permissions_classes = (IsAuthenticated,IsAdminUser)

class CategoryDeleteAPIView(DestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailSerializer
	lookup_field = "id"
	permissions_classes = (IsAuthenticated,IsAdminUser)

class SubCategoryCreateAPIView(CreateAPIView):
	queryset = SubCategory.objects.all()
	serializer_class = SubCategoryDetailSerializer
	permissions_classes = (IsAuthenticated,IsAdminUser)

class SubCategoryListAPIView(ListAPIView):
	queryset = SubCategory.objects.all()
	serializer_class = SubCategoryListSerializer
	permissions_classes = (IsUser,)
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('category',)

class SubCategoryUpdateAPIView(UpdateAPIView):
	queryset = SubCategory.objects.all()
	serializer_class = SubCategoryDetailSerializer
	lookup_field = "id"
	permissions_classes = (IsAuthenticated,IsAdminUser,)
	
class SubCategoryDeleteAPIView(DestroyAPIView):
	queryset = SubCategory.objects.all()
	serializer_class = SubCategoryDetailSerializer
	lookup_field = "id"
	permissions_classes = (IsAuthenticated,IsAdminUser,)


class ShopDetailAPIView(RetrieveAPIView):
	queryset = Shop.objects.all()
	serializer_class = ShopDetailSerializer
	permissions_classes = (IsUser,)
	lookup_field = "slug"

class ShopListAPIView(ListAPIView):
	# permission_classes = (IsUser,)
	serializer_class = ShopListSerializer
	#pagination_class = ShortPAginator
	filter_backends = (OrderedDistanceToPointFilter,DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter,)
	distance_filter_field = 'location'
	filter_fields = ('category','subCategory')
	ordering_fields = ('likes','shopName')
	search_fields = ('category__name','subCategory__name','filterTags__tag','shopName')

	def get_queryset(self):
		cityId = self.kwargs['cityId']
		subCatId = self.kwargs['subCatId']
		search = self.request.query_params.get('search',None)
		if search and len(search)>3:
			return Shop.objects.filter(city__id=cityId)
		else:
			return Shop.objects.filter(city__id=cityId,subCategory=subCatId)
	
	# def get_serializer_context(self):
	# 	cityId = self.kwargs['cityId']
	# 	subCatId = self.kwargs['subCatId']
	# 	context = super(ShopListAPIView, self).get_serializer_context()
	# 	context.update({
	# 		"cityId": cityId,
	# 		"subCatId" :subCatId
		   
	# 	})
	# 	return context
		
		# return {'cityId ': cityId , 'request': self.request}

class FeedbackListAPIView(ListAPIView):
	queryset = Feedback.objects.all()
	serializer_class = FeedbackListSerializer

	# pagination_class = ShortPAginator

class FeedbackCreateAPIView(CreateAPIView):
	queryset = Feedback.objects.all()
	serializer_class = FeedbackSerializer
	permission_classes = (IsAuthenticated,IsUser)

class FeedbackUpdateAPIView(UpdateAPIView):
	queryset = Feedback.objects.all()
	serializer_class = FeedbackSerializer
	lookup_field = "id"
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

class RateShop(APIView):
	serializer_class = RatingSerializer
	

	def get(self, request, format=None):
		rate =ShopRating.objects.all()
		serializer = RatingSerializer(rate, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = RatingSerializer(data=request.data)
			
	
		if serializer.is_valid():
			serialized_data = serializer.validated_data
			shop = serialized_data.get('shop')
			rating = serialized_data.get('rating')
			user = request.user
	
			rating_qs = ShopRating.objects.filter(shop = shop,user=user)
			shop_obj = Shop.objects.get(id=shop.id)			
			all_previous_rating = shop_obj.rating
			rated_users = ShopRating.objects.filter(shop = shop).count()            
			if rating_qs.exists() and rating_qs.count() == 1:
				rate_obj = rating_qs.first()
				previous_rating = rate_obj.rating				
				rating_data= serializer.data								
				final_serialized_data = RatingSerializer(rate_obj,data=rating_data)				
				if final_serialized_data.is_valid():
					final_serialized_data.save()
					new_rating = ((all_previous_rating * rated_users) + rating - previous_rating)/rated_users					
					shop_obj.rating = new_rating
					shop_obj.save()
			else:
				serializer.save()								
				new_rating = ((all_previous_rating * rated_users) + rating)/(rated_users +1)
				shop_obj.rating = new_rating
				shop_obj.save()			
			return Response(serializer.data, status=HTTP_200_OK)		
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
			
			


class VoteShop(APIView):
	
	serializer_class = VoteSerializer
	def get(self, request, format=None):
		vote = Vote.objects.all()
		serializer = VoteSerializer(vote, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = VoteSerializer(data=request.data)
		if serializer.is_valid():
			resp = {}
			already_voted = {}
			like_count = 0
			dislike_count = 0
			serialized_data = serializer.validated_data
#			print(serializer)
			shop = serialized_data.get('shop')
			likes = serialized_data.get('liked')
			user = request.user
			vote_qs = Vote.objects.filter(shop = shop,user=user)
			# if the user already VOTED for  the current shop
			if vote_qs.exists() and vote_qs.count() == 1:
				vote_obj = vote_qs.first()
				already_voted = VoteSerializer(vote_obj).data
		#	print (liked)
		#	print(serializer_new)

			if already_voted:
				like_count = 0
				dislike_count = 0
				#if the entry for vote is already exist
				previously_liked = already_voted.get('liked')
				if likes:
					#if current response is like
					if previously_liked == None:
						#not voted previously
						like_count = 1
						already_voted['liked'] = True
					elif previously_liked == True:
						#previously liked
						like_count = -1
						already_voted['liked'] = None
					else:
						#if disliked previously
						like_count = 1
						dislike_count = -1
						already_voted['liked'] = True
				else:
					#if current response is dislike
					if previously_liked == None:
						 #not voted previously
						 dislike_count = 1
						 already_voted['liked'] = False
					elif previously_liked == True:
						#liked previously
						like_count = -1
						dislike_count = 1
						already_voted['liked'] = False
					else:
						#disliked previously
						dislike_count = -1
						already_voted['liked'] = None
				final_serialized_data = VoteSerializer(vote_obj,data=already_voted)
				if final_serialized_data.is_valid():
					final_serialized_data.save()
			else:
				like_count = 0
				dislike_count = 0
				print("1st time")
				serializer.save(user=user)
				#if voted first time
				if likes:
					#if current response is like
					like_count = 1
					#if current response is dislike
				else:
					dislike_count = 1
			resp = {
			'likeCnt' : like_count,
			'dislikeCnt' : dislike_count
			}
			if like_count != 0 or  dislike_count != 0:				
				shop_obj = Shop.objects.get(id=shop.id)
				shop_obj.likes = F('likes') + like_count
				shop_obj.dislikes = F('dislikes') + dislike_count
				shop_obj.save()
			return Response(resp, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class FreeListingAPIView(APIView):
	permission_classes = (AllowAny,IsUser)
	def post(self, request, format=None):
		serializer = FreeListingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PricingListAPIView(ListAPIView):
	queryset = Pricing.objects.all()
	serializer_class = PricingSerializer
	def get_queryset(self):
		shopSlug = self.kwargs['slug']
		return Pricing.objects.filter(shop__slug=shopSlug)