from account.models import User
from base import NotificationVerbs
from base.models import TimeStampedModel
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import JSONField, QuerySet


class ConcatNotificationQueryset(QuerySet):

    """
    Chain-able QuerySets using ```.as_manager()``.
    """

    def active(self):
        """
        QuerySet filter() for retrieving both read and unread notifications
        which are not soft-deleted.
        :return: Non soft-deleted notifications.
        """
        return self.filter(deleted=False)

    def read(self):
        """
        QuerySet filter() for retrieving read notifications.
        :return: Read and active Notifications filter().
        """
        return self.filter(deleted=False, unread=False)

    def unread(self):
        """
        QuerySet filter() for retrieving unread notifications.
        :return: Unread and active Notifications filter().
        """
        return self.filter(deleted=False, unread=True)

    def unread_all(self, user=None):
        """
        Marks all notifications as unread for a user (if supplied)
        :param user: Notification recipient.
        :return: Updates QuerySet as unread.
        """
        qs = self.read()
        if user:
            qs.filter(recipient=user)
        qs.update(unread=True)

    def read_all(self, user=None):
        """
        Marks all notifications as read for a user (if supplied)
        :param user: Notification recipient.
        :return: Updates QuerySet as read.
        """
        qs = self.unread()
        if user:
            qs.filter(recipient=user)
        qs.update(unread=False)

    def delete_all(self, user=None):
        """
        Method to soft-delete all notifications of a User (if supplied)
        :param user: Notification recipient.
        :return: Updates QuerySet as soft-deleted.
        """
        qs = self.active()
        if user:
            qs.filter(recipient=user)

        soft_delete = getattr(settings, "NOTIFY_SOFT_DELETE", True)

        if soft_delete:
            qs.update(deleted=True)
        else:
            qs.delete()

    def active_all(self, user=None):
        """
        Method to soft-delete all notifications of a User (if supplied)
        :param user: Notification recipient.
        :return: Updates QuerySet as soft-deleted.
        """
        qs = self.deleted()
        if user:
            qs.filter(recipient=user)
        qs.update(deleted=False)

    def deleted(self):
        """
        QuerySet ``filter()`` for retrieving soft-deleted notifications.
        :return: Soft deleted notification filter()
        """
        return self.filter(deleted=True)


class ConcatNotification(TimeStampedModel):
    recipient = models.ForeignKey(
        User, blank=False, related_name="concat_notifications", on_delete=models.CASCADE
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True)
    verb = models.CharField(choices=NotificationVerbs.choices, max_length=255)
    deleted = models.BooleanField(default=False, db_index=True)
    data = JSONField(blank=True, null=True)
    objects = ConcatNotificationQueryset.as_manager()

    class Meta(object):
        ordering = ("-created_at",)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()
