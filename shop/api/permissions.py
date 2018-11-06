from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsUser(BasePermission):
    def has_permission(self, request, view):
    	print("hello")
    	if 'HTTP_USER_AGENT' in request.META:
    		# print (request.META[''])
    		if 'Mozilla' in request.META['HTTP_USER_AGENT']:
    			if(request.META.get('HTTP_REFERER')):
    				return True
    	return False