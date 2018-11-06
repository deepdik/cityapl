# -*- coding: utf-8 -*-

from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _


class Dialog(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"))
    dialog_status_owner = models.BooleanField(verbose_name=_("dialog_status_owner"),default=True)
    dialog_status_opponent = models.BooleanField(verbose_name=_("dialog_status_opponent"),default=True)
    

    def __str__(self):
        return _("Chat with ") + self.opponent.username


class Message(TimeStampedModel, SoftDeletableModel):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages")    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("Receiver"), related_name="messages_receiver",default=11)
    text = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    seen = models.BooleanField(verbose_name=_("Seen"), default=False)
    sender_del_msg = models.BooleanField(verbose_name=_("Auther_delete_msg"), default=False)
    receiver_del_msg = models.BooleanField(verbose_name=_("Receiver_delete_msg"), default=False)
    all_objects = models.Manager()
    

    def get_formatted_create_datetime(self):
        return dj_date(self.created, settings.DATETIME_FORMAT)

    def __str__(self):
        return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"

    def receiver_user(self):
        if self.sender.username==self.dialog.owner.username:
            return self.dialog.opponent.username
        else:
            return self.dialog.owner.username