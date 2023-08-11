from django.db import models


class ModelUsed(models.Model):
    model_name = models.CharField(max_length=32, unique=True)

    class Meta:
        db_table = "testing_model_table"

class Prediction(models.Model):

    model = models.ForeignKey(ModelUsed, on_delete=models.CASCADE)

    prediction = models.FloatField()
    class Meta:
        # if you want ot index unique say time and model
        # unique_together = (('model', 'prediction'))
        # index_together = (('model', 'prediction'))
        db_table = "testing_model_prediction"

