from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from dummy_predictions_model.models import ModelUsed, Prediction
from dummy_predictions_model.serializers import ModelUsedSerializer, PredictedSerializer


class ModelUsedView(APIView):
    serializer_class = ModelUsedSerializer

    def get(self, request):

        model_name = request.query_params.get('model_name', None)

        if model_name:
            # models_used = ModelUsed.objects.filter(model_id=model_id)
            models_used = ModelUsed.objects.filter(model_name=model_name)
        else:
            models_used = ModelUsed.objects.all()

        if models_used:
            model_serializer = self.serializer_class(models_used, many=True)
            return Response(model_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No models found'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_name'],
            properties={
                'model_name': openapi.Schema(type=openapi.TYPE_STRING),
                'model_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Update a model'
    )
    def post(self, request):
        model_id = request.data.get('model_id', None)
        model_name = request.data.get('model_name', None)

        #todo update model instead of just save


        post_data = {
            'model_name': model_name
        }

        serializer = self.serializer_class(data=post_data)
        if serializer.is_valid(raise_exception=True):
            model_used = serializer.save()

            if model_used:
                return Response({'message': 'Successful new model'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_id'],
            properties={
                'model_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Delete prediction'
    )
    def delete(self, request):
        model_id = request.data.get('model_id', None)
        if model_id:
            # todo add for model_name
            model = ModelUsed.objects.filter(id=model_id)
            if model:
                model.delete()
                response = {'message': f'Successfully deleted {model_id}'}
                return Response(response, status=status.HTTP_200_OK)
        response = {'message': f'unable to delete {model_id}'}
        return Response(response, status=status.HTTP_200_OK)



class PredictionView(APIView):
    serializer_class = PredictedSerializer

    def get(self, request):
        predictions = Prediction.objects.all()
        prediction_serializer = self.serializer_class(predictions, many=True)
        return Response(prediction_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PredictedSerializer)
    def put(self, request):
        model_name = request.data.get('model_name', None)
        model = ModelUsed.objects.get(model_name=model_name)
        prediction = request.data.get('prediction', None)

        if model:
            prediction = Prediction.objects.create(model=model, prediction=prediction)

            serializer = self.serializer_class(prediction)
            #todo do a check to see if should save
            serializer.is_valid()
            serializer.save()
            response = {'message': 'prediction created', 'result': serializer.data}

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'model not found'}, status=status.HTTP_200_OK)
#todo consider using a method for the delte instead of using the built in status
    @swagger_auto_schema(
        # methods=['delete'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['model_used', 'pred_id'],
            properties={
                'model_used': openapi.Schema(type=openapi.TYPE_STRING),
                'pred_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        operation_description='Delete prediction'
    )
    def delete(self, request):

        pred_id = request.data.get('pred_id', None)
        model_used = request.data.get('model_used', None)
        if pred_id:
            prediction = Prediction.objects.filter(id=pred_id)
            if prediction:
                prediction.delete()
                response = {'message': f'Successfully deleted {pred_id}'}
                return Response(response, status=status.HTTP_204_NO_CONTENT)
        if model_used:
            model_name = request.data.get('model_used', None)
            remove_predictions = Prediction.objects.filter(model__model_name=model_name)
            prediction_ids = []
            for prediction in remove_predictions:
                prediction_ids.append(prediction.id)
                prediction.delete()

            if len(prediction_ids) > 0:
                response = {'message': f'Successfully deleted {prediction_ids}'}
                return Response(response, status=status.HTTP_204_NO_CONTENT)

        response = {'message': 'No prediction found to delete'}
        return Response(response)
    #todo consider putting a update function
