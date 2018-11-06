from django.contrib import admin

from .models import Dialog, Message


class DialogAdmin(admin.ModelAdmin):
    list_display = ('id', 
        'created',
        'modified',
        'owner',
        'owner_id',
        'opponent',
        'dialog_status_owner',
        'dialog_status_opponent'

    )


    list_filter = ('created', 'modified', 'owner', 'opponent')
admin.site.register(Dialog, DialogAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        # 'modified',
        # 'is_removed',
        'dialog',
        'sender',
        'receiver',
        # 'receiver_user',
        'text',
        'seen',
    )
    list_filter = ('created', 'modified', 'is_removed', 'dialog', 'sender')
admin.site.register(Message, MessageAdmin)
