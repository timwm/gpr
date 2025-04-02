from django.db import models
# from collections import namedtuple

from .user import User, Staff, Student


class Category(models.Model):
    name = models.CharField(unique=True, max_length=32)
    description = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return "%s" % self.name


class Issue(models.Model):

    class Meta:
        ordering = ('-created_at', )

    STATUS_OPEN = 1
    STATUS_REVIEW = 2
    STATUS_ESCALATED = 4
    STATUS_RESOLVED = 8
    STATUS_CLOSED = 16
    STATUS_CHOICES = {
        STATUS_OPEN: 'open',
        STATUS_REVIEW: 'in_review',
        STATUS_ESCALATED: 'escalated',
        STATUS_RESOLVED: 'resolved',
        STATUS_CLOSED: 'closed',
    }

    PRIOTITY_LOW = 1
    PRIOTITY_MODERATE = 2
    PRIOTITY_HIGH = 4
    PRIOTITY_CRITICAL = 8
    PRIORITY_CHOICES = {
        PRIOTITY_LOW: 'low',
        PRIOTITY_MODERATE: 'moderate',
        PRIOTITY_HIGH: 'high',
        PRIOTITY_CRITICAL: 'critical',
    }

    ESCALATION_L0 = 1
    ESCALATION_L1 = 2
    ESCALATION_L2 = 4
    ESCALATION_CHOICES = {
        ESCALATION_L0: 'level_0',
        ESCALATION_L1: 'level_1',
        ESCALATION_L2: 'level_2',
    }

    owner = models.ForeignKey(Student, related_name='issues', on_delete=models.CASCADE)
    assignee = models.ForeignKey(Staff,
        related_name='assingned_issues', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=256, null=True, blank=False, default='')
    categories = models.ManyToManyField(Category, blank=False)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=STATUS_OPEN
    )
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES, default=PRIOTITY_LOW
    )
    escalation_level = models.PositiveSmallIntegerField(
        choices=ESCALATION_CHOICES, default=ESCALATION_L0
    )
    notes = models.TextField(max_length=4096, null=True, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return "%s" % self.title


def get_attachment_path(instance, filename):
    import uuid
    # return "attachments/{0}".format(uuid.uuid4()
    return str(uuid.uuid4())

def get_attachment_storage():
    from django.core.files.storage import FileSystemStorage
    from django.conf import settings
    from os import path

    location = path.join(settings.MEDIA_ROOT, 'attachments')
    base_url = path.join(settings.MEDIA_URL, 'attachments')

    return FileSystemStorage(location=location, base_url=base_url)
        

# class Att(models.Model):
#     fh = models.FileField(upload_to=get_attachment_path, storage=get_attachment_storage)
#     name = models.CharField(max_length=256, blank=True)
# 
#     def save(self, *args, **kwargs):
#         if self.fh:
#             self.name = self.fh.name
#             self.size = self.fh.size
#             super().save(*args, **kwargs)
#         else:
#             print('called save: else block')
# 
#     def delete(self, *args, **kwargs):
#         super().delete(*args, **kwargs)
#         self.fh.delete()
# 
#     def __str__(self):
#         name = "%s" % self.fh
#         return name.rpartition('/')[-1] or name

class Attachment(models.Model):
    # file = models.UUIDField(primary_key=True)
    file = models.FileField(unique=True, upload_to=get_attachment_path, storage=get_attachment_storage, max_length=256)
    issue = models.ForeignKey(Issue, related_name='attachments', on_delete=models.CASCADE) 
    name = models.CharField(max_length=1024, blank=False, editable=False)
    size = models.PositiveBigIntegerField()
    type = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # TODO: Check for filetype (python-magic)
        if self.file:
            self.name = self.file.name
            self.size = self.file.size
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.file.delete()

    def __str__(self):
        return "%s" % self.file


class IssueLog(models.Model):
    issue = models.ForeignKey(Issue, related_name='logs', null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(Staff,
        related_name='+', null=True, on_delete=models.CASCADE
    )
    actor = models.ForeignKey(User,
        related_name='+', on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(Category, related_name='+', blank=False)
    status = models.PositiveSmallIntegerField(
        choices=Issue.STATUS_CHOICES, default=Issue.STATUS_OPEN
    )
    priority = models.PositiveSmallIntegerField(
        choices=Issue.PRIORITY_CHOICES, default=Issue.PRIOTITY_LOW
    )
    escalation_level = models.PositiveSmallIntegerField(
        choices=Issue.ESCALATION_CHOICES, default=Issue.ESCALATION_L0
    )
    attachments = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
