from rest_framework import serializers

class TokenResponseSerializer(serializers.Serializer):
    class Meta:
        fields = ('token',)

    def to_representation(self, instance):
        return {
            'data': {
                'type': 'tokens',
                'attributes': {
                    'token': instance['token']
                }
            }
        }