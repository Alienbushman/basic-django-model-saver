from rest_framework import serializers

from dummy_predictions_model.models import ModelUsed, Prediction


class ModelUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelUsed
        fields = '__all__'

class PredictedSerializer(serializers.ModelSerializer):
    # model_name = serializers.CharField(source='model.model_name')
    class Meta:
        model = Prediction
        # fields = ('id','prediction', 'model', 'model__model_name')
        fields = '__all__'

    # def