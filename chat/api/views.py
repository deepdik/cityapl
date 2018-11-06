from rest_framework.generics import ListAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework import filters

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Count 

from rest_framework.permissions import (
	IsAuthenticated,
	IsAdminUser,
	AllowAny,
	)

from django_filters.rest_framework import DjangoFilterBackend

from chat.models import (
	Dialog,
	Message,	
	)

from .serializers import (
	DialogListSerializer,
	MessageListSerializer,
	DialogNotificationSerializer,
	DialogBlockSerializer 
	)
try:
	from django.urls import reverse
except ImportError:
	from django.core.urlresolvers import reverse
from chat import models
from chat import utils
from django.shortcuts import get_object_or_404

from django.conf import settings

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class DialogListAPIView(ListAPIView):
	queryset = Dialog.objects.all()
	serializer_class = DialogListSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)

	def get_queryset(self):
		user=self.request.user      
		return Dialog.objects.filter(Q(owner=user) | Q(opponent=user))
	
	# def get_serializer_context(self):
	#     context = super(TaskListViewSet, self).get_serializer_context()
	#     return {'request' : 'test'}
	
class MessageListAPIView(ListAPIView):
	queryset = Message.objects.all()
	serializer_class = MessageListSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	ordering_fields = ('-modified')
	# pagination_class = ShortPAginator   
	def get_queryset(self):
		if self.kwargs.get('username'):
			user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
			dialog = utils.get_dialogs_with_user(self.request.user, user)
			# dialog_status=Dialog.objects.get(
			# Q(owner=self.request.user, opponent=user) | Q(opponent=self.request.user, owner=user))
			# print(dialog_status)
			# dialogStatus=dialog_status.dialog_status
			# print(dialogStatus)
		 
			if len(dialog) == 0:
				dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)               
				return Message.objects.filter(dialog=dialog)
			else:
				dialog = dialog[0]
				opponent_unseen_msg = Message.objects.filter(dialog=dialog, sender__username = user ,seen=False).update(seen=True) 
				return Message.objects.filter(dialog=dialog)
		else:
			pass
	
class DialogNotifictionListAPIView(ListAPIView):
   
	serializer_class = DialogNotificationSerializer

	def get_queryset(self):
		user=self.request.user
		return Dialog.objects.filter(Q(owner=user) | Q(opponent=user))

class DialogBlockListAPIView(RetrieveAPIView):
	queryset = Dialog.objects.all()
	serializer_class =DialogBlockSerializer
	lookup_field="username"


	def get_queryset(self):
		if self.kwargs.get('username') and self.kwargs.get('status'):

			user = get_object_or_404(get_user_model(), username = self.kwargs.get('username'))
		
			user_dialog = Dialog.objects.filter(
			Q(owner = self.request.user, opponent = user) | Q(opponent = self.request.user, owner = user))                			
			if len(user_dialog) > 0:
				
				dialog = user_dialog.first()
				dialog_owner = dialog.owner
				if self.kwargs.get('status') == "block":				
					if self.request.user == dialog_owner:
						block_user = user_dialog.update(dialog_status_owner = False)
					else:
						block_user = user_dialog.update(dialog_status_opponent = False)
						
					return Response( status = HTTP_200_OK)

				elif self.kwargs.get('status') == "unblock":
					if self.request.user == dialog_owner:
						block_user = user_dialog.update(dialog_status_owner = True)
					else:
						block_user = user_dialog.update(dialog_status_opponent = True)
						
					return Response(status = HTTP_200_OK)				
				else:					
					return  HttpResponseServerError()
			else:
				# no user
				pass

		else:
			pass       
				 
					
# class DeleteMsg(APIView):
# 	serializer_class = DeleteMsgSerializer
# 	lookup_field = "id"
	












	