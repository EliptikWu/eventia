from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from events.services.attendance_service import AttendanceService
from events.serializers.attendance_serializer import AttendanceSerializer, AttendanceCreateSerializer


attendance_service = AttendanceService()


@api_view(['POST'])
def register_attendance(request):
    serializer = AttendanceCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            event_id = serializer.validated_data['event_id']
            participant_id = serializer.validated_data['participant_id']
            attendance = attendance_service.register_attendance(event_id, participant_id)
            return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def cancel_attendance(request):
    serializer = AttendanceCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            event_id = serializer.validated_data['event_id']
            participant_id = serializer.validated_data['participant_id']
            attendance_service.cancel_attendance(event_id, participant_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def event_attendees(request, event_id):
    try:
        attendances = attendance_service.get_attendees_by_event(event_id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def participant_events(request, participant_id):
    try:
        attendances = attendance_service.get_events_by_participant(participant_id)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)