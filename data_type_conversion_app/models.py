from django.db import models

class ProcessedData(models.Model):
    column_name = models.CharField(max_length=255)
    inferred_data_type = models.CharField(max_length=50)

    def __str__(self):
        return self.column_name
