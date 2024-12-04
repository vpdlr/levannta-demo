from rest_framework import serializers

class PortfolioFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError('Only CSV files are allowed.')
        return value