from rest_framework import serializers


class ErrorDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    detail = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    errors = ErrorDetailSerializer(many=True)

    def to_representation(self, instance):
        return {
            'errors': instance['errors']
        }
    