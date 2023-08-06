from rest_framework import serializers
from tom_targets.models import Target
from tom_targets.serializers import TargetSerializer

from tom_nonlocalizedevents.models import EventCandidate, EventLocalization, Superevent


class BulkCreateEventCandidateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        event_candidates = [EventCandidate(**item) for item in validated_data]
        return EventCandidate.objects.bulk_create(event_candidates)


class EventCandidateSerializer(serializers.ModelSerializer):
    """
    Serializer class for the ``EventCandidate``. ``PrimaryKeyRelatedField``s are used in order to allow creating an
    ``EventCandidate`` with just a primary key, and ``to_representation`` is then overridden for proper display values.
    See: https://www.django-rest-framework.org/api-guide/relations/#custom-relational-fields
    """
    superevent = serializers.PrimaryKeyRelatedField(queryset=Superevent.objects.all())
    target = serializers.PrimaryKeyRelatedField(queryset=Target.objects.all())

    viable = serializers.BooleanField(default=True)
    priority = serializers.IntegerField(default=1)

    class Meta:
        model = EventCandidate
        fields = '__all__'
        list_serializer_class = BulkCreateEventCandidateListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # TODO: this is a little unorthodox. it's convenient for now to handle the data from
        # the ForiengKey objects, but that should be handled separately by their own serializers.
        # (and to_representation could be left undisturbed).
        representation['target'] = TargetSerializer(Target.objects.get(pk=representation['target'])).data
        representation['superevent'] = Superevent.objects.get(pk=representation['superevent']).superevent_id
        return representation


class SupereventSerializer(serializers.HyperlinkedModelSerializer):
    event_candidates = serializers.SerializerMethodField()

    class Meta:
        model = Superevent
        fields = ['superevent_id', 'superevent_url',
                  'id', 'event_candidates', 'created', 'modified']

    def get_event_candidates(self, instance):
        alerts = instance.eventcandidate_set.all()
        # This returns the superevent identifier, which means it's duplicated in the response. The SupereventSerializer
        # should therefore use its own custom EventCandidateSerializer rather than the one defined above
        return EventCandidateSerializer(alerts, many=True).data


class EventLocalizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventLocalization
        fields = ['id', 'created', 'modified']
