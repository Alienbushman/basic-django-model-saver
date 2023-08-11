from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from dummy_predictions_model.models import ModelUsed, Prediction
from dummy_predictions_model.serializers import ModelUsedSerializer, PredictedSerializer


class ModelUsedView(APIView):
    serializer_class = ModelUsedSerializer

    @swagger_auto_schema(
        operation_description='Returns all models'
    )
    def get(self, request):
        # todo can add some filtering my model name
        models_used = ModelUsed.objects.all()

        if models_used:
            model_serializer = self.serializer_class(models_used, many=True)
            return Response(model_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No models found'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_name', 'model_id'],
            properties={
                'model_name': openapi.Schema(type=openapi.TYPE_STRING),
                'model_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Update a model'
    )
    def put(self, request):
        model_id = request.data.get('model_id', None)
        model_name = request.data.get('model_name', None)
        model = ModelUsed.objects.get(id=model_id)
        if model:
            #todo handle changing to existing model name
            model.model_name = model_name
            model.save()
            if model:
                return Response({'message': 'Successfully updated model name'}, status=status.HTTP_200_OK)
            return Response({'message': 'Something went wrong during name update'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Model not found'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_id'],
            properties={
                'model_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Delete model'
    )
    def delete(self, request):
        model_id = request.data.get('model_id', None)
        if model_id:
            # todo add removal for model name
            model = ModelUsed.objects.filter(id=model_id)
            if model:
                model.delete()
                response = {'message': f'Successfully deleted {model_id}'}
                return Response(response, status=status.HTTP_200_OK)
        response = {'message': f'unable to delete {model_id}'}
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ModelUsedSerializer,
        operation_description='Adds a model'
    )
    def post(self, request):
        model_name = request.data.get('model_name', None)

        post_data = {
            'model_name': model_name
        }

        serializer = self.serializer_class(data=post_data)
        if serializer.is_valid(raise_exception=True):
            model_used = serializer.save()

            if model_used:
                return Response({'message': 'Successful new model'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'unable to save new model'}, status=status.HTTP_400_BAD_REQUEST)


class PredictionView(APIView):
    serializer_class = PredictedSerializer

    @swagger_auto_schema(
        title="Get all predictions",
        operation_description='Get all the predictions'
    )
    def get(self, request):
        predictions = Prediction.objects.all()
        prediction_serializer = self.serializer_class(predictions, many=True)
        display_data = []
        model_dict = {}
        for prediction in prediction_serializer.data:
            model_id = prediction['model']
            display_prediction = {}
            model_name = ''
            if model_id in model_dict:
                model_name = model_dict[model_id]
            else:
                model_name = ModelUsed.objects.get(id=model_id).model_name
                model_dict[model_id] = model_name
            display_prediction["id"] = prediction["id"]
            display_prediction["prediction"] = prediction["prediction"]
            display_prediction["model_name"] = model_name
            display_data.append(display_prediction)
        return Response(display_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        title="Create a prediction",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_name', 'prediction'],
            properties={
                'model_name': openapi.Schema(type=openapi.TYPE_STRING),
                'prediction': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
        operation_description='add a prediction'
    )
    def post(self, request):
        model_name = request.data.get('model_name', None)
        prediction = request.data.get('prediction', None)
        model_query = ModelUsed.objects.filter(model_name=model_name)
        if model_query.exists():
            model = model_query[0]
            post_data = {
                'model': model.id,
                'prediction': prediction
            }
            serializer = self.serializer_class(data=post_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {'message': 'prediction created', 'result': serializer.data}

                return Response(response, status=status.HTTP_201_CREATED)
            return Response({'message': 'Unable to save prediction'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'model not found'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            # required=['model_used', 'pred_id'],
            required=[],
            properties={
                'model_used': openapi.Schema(type=openapi.TYPE_STRING),
                'pred_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Delete prediction'
    )
    def delete(self, request):
        prediction_ids = []
        pred_id = request.data.get('pred_id', None)
        model_used = request.data.get('model_used', None)
        if pred_id:
            prediction = Prediction.objects.filter(id=pred_id)
            if prediction:
                prediction.delete()
                prediction_ids.append(pred_id)

        if model_used:
            model_name = request.data.get('model_used', None)
            remove_predictions = Prediction.objects.filter(model__model_name=model_name)

            for prediction in remove_predictions:
                prediction_ids.append(prediction.id)
                prediction.delete()
        if len(prediction_ids) > 0:
            response = {'message': f'Successfully deleted {prediction_ids}'}
            return Response(response, status=status.HTTP_200_OK)

        response = {'message': 'No prediction found to delete'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
