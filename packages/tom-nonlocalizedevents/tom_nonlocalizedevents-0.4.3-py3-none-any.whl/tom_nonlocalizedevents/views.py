from django.views.generic import DetailView, ListView

from rest_framework import permissions, viewsets

from tom_nonlocalizedevents.superevent_clients.gravitational_wave import GravitationalWaveClient

from .models import EventCandidate, EventLocalization, Superevent
from .serializers import EventCandidateSerializer, EventLocalizationSerializer, SupereventSerializer


class NonlocalizedEventListView(ListView):
    """
    Unadorned Django ListView subclass for Superevent model.
    (To be updated when Superevent model is renamed to NonlocalizedEvent).
    """
    model = Superevent
    template_name = 'tom_nonlocalizedevents/index.html'


class NonlocalizedEventDetailView(DetailView):
    """
    Django DetailView subclass for SuperEvent model.
    (To be updated when Superevent model is renamed to NonlocalizedEvent).

    Has mechanism to supply templates specific to the type of NonlocalizedEvent
    (GW, GRB, Nutrino).
    """
    model = Superevent
    template_name = 'tom_nonlocalizedevents/detail.html'

    # TODO: consider combining these dictionaries
    template_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE:
            'tom_nonlocalizedevents/superevent_detail/gravitational_wave.html',
        Superevent.SupereventType.GAMMA_RAY_BURST:
            'tom_nonlocalizedevents/superevent_detail/gamma_ray_burst.html',
        Superevent.SupereventType.NEUTRINO:
            'tom_nonlocalizedevents/superevent_detail/neutrino.html',
    }

    # A client in this context is the interface to the service providing event info.
    # (i.e GraceDB for gravitational wave events)
    client_mapping = {
        Superevent.SupereventType.GRAVITATIONAL_WAVE: GravitationalWaveClient(),
        Superevent.SupereventType.GAMMA_RAY_BURST: None,
        Superevent.SupereventType.NEUTRINO: None,
        Superevent.SupereventType.UNKNOWN: None,
    }

    def get_template_names(self):
        obj = self.get_object()
        return [self.template_mapping[obj.superevent_type]]

    # TODO: error handling
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        superevent_client = self.client_mapping[obj.superevent_type]
        # TODO: should define superevent_client API (via ABC) for clients to implement
        if superevent_client is not None:
            context['superevent_data'] = superevent_client.get_superevent_data(obj.superevent_id)
            context.update(superevent_client.get_additional_context_data(obj.superevent_id))
        return context


# Django Rest Framework Views


class NonlocalizedEventViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint that allows Superevents to be viewed or edited.
    """
    queryset = Superevent.objects.all()
    serializer_class = SupereventSerializer
    permission_classes = []


class EventCandidateViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint for EventCandidate model.

    Implementation has changes for bulk_create and update/PATCH EventCandidate instances.
    """
    queryset = EventCandidate.objects.all()
    serializer_class = EventCandidateSerializer
    permission_classes = []  # TODO: re-implement auth permissions

    def get_serializer(self, *args, **kwargs):
        # In order to ensure the list_serializer_class is used for bulk_create, we check that the POST data is a list
        # and add `many = True` to the kwargs
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Provide support for the PATCH HTTP verb to update individual model fields.

        An example request might look like:

            PATCH http://localhost:8000/api/eventcandidates/18/

        with a Request Body of:

            {
                "viability": false
            }

        """
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class EventLocalizationViewSet(viewsets.ModelViewSet):
    """
    DRF API endpoint that allows EventLocalizations to be viewed or edited.
    """
    queryset = EventLocalization.objects.all()
    serializer_class = EventLocalizationSerializer
    permission_classes = [permissions.IsAuthenticated]
