from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.services.participant_service import ParticipantService
from events.serializers.participant_serializer import ParticipantSerializer


participant_service = ParticipantService()


@api_view(['GET', 'POST'])
def participant_list(request):
    if request.method == 'GET':
        participants = participant_service.get_all_participants()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            try:
                participant = participant_service.create_participant(serializer.validated_data)
                return Response(ParticipantSerializer(participant).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def participant_detail(request, pk):
    try:
        if request.method == 'GET':
            participant = participant_service.get_participant_by_id(pk)
            serializer = ParticipantSerializer(participant)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ParticipantSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                participant = participant_service.update_participant(pk, serializer.validated_data)
                return Response(ParticipantSerializer(participant).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            participant_service.delete_participant(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)