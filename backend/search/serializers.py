# from ..models import Department, Faculty
from rest_framework import serializers
from core.models import Issue
from core.fields import MultiTypeField


class IssueQuerySerializer(serializers.Serializer):
    """
    All fields are optional
    """
    owner = serializers.ListField(
        child=MultiTypeField([
            int,
            serializers.CharField(min_length=1),
        ]),
        required=False
    )
    assignee = serializers.ListField(
        child=serializers.CharField(min_length=1),
        required=False
    )
    categories = serializers.ListField(
        child=serializers.CharField(min_length=1),
        required=False
    )
    status = serializers.MultipleChoiceField(
        choices=list(Issue.STATUS_CHOICES.items()),
        required=False
    )
    priority = serializers.MultipleChoiceField(
        choices=list(Issue.PRIORITY_CHOICES.items()),
        required=False
    )
    escalation_level = serializers.MultipleChoiceField(
        choices=list(Issue.ESCALATION_CHOICES.items()),
        required=False
    )

    before = serializers.DateTimeField(required=False)
    after = serializers.DateTimeField(required=False)

    def validate(self, data):
        before = data.get('before', None)
        after = data.get('after', None)
        if before and after and before > after:
            raise serializers.ValidationError("Invalid datetime range")
        return data

