from rest_framework import serializers

from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    spots_left = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Event
        fields = '__all__'

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError('capacity must be non-negative!')
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ['user', 'registered_at']
