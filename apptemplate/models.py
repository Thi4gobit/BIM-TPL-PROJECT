from django.db import models
from django.contrib.auth.models import User

"""
Template
- nome
- criador
- data
- visualizadores concept
- editores concept
- aprovadores concept
- visualizadores concept
- editores concept
- aprovadores concept
"""

class Template(models.Model):

    name = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='temp_created_by',
    )
    field_editor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='temp_field_editor',
    )
    value_editor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='temp_value_editor',
    )

    def __str__(self):
        return str(self.name)