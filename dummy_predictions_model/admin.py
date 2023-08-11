from django.contrib import admin

from dummy_predictions_model.models import ModelUsed, Prediction

# Register your models here.
admin.site.register(ModelUsed)
admin.site.register(Prediction)
