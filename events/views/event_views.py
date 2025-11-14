from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.services.event_service import EventService
from events.serializers.event_serializer import EventSerializer


event_service = EventService()


@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = event_service.get_all_events()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            try:
                event = event_service.create_event(serializer.validated_data)
                return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    try:
        if request.method == 'GET':
            event = event_service.get_event_by_id(pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = EventSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                event = event_service.update_event(pk, serializer.validated_data)
                return Response(EventSerializer(event).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            event_service.delete_event(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def event_statistics(request, pk):
    try:
        stats = event_service.get_event_statistics(pk)
        return Response(stats)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)