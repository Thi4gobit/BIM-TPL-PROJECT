from django.db import models


class GroupField(models.Model):

    name = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name


class Field(models.Model):
    
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):

    item = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.item}'


class FieldSelfRelationship(models.Model):

    field = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        # related_name='fieldselfrelationship_field'
    )
    subfield = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        related_name='subfields'
    )
    sequence = models.PositiveIntegerField(unique=False)
    text_before = models.CharField(max_length=32, blank=True, null=True)
    text_after = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return f'{self.field}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['field', 'subfield'], 
                name='unique_field_subfield_relationship'
            )
        ]
    

class CustomField(models.Model):

    field = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        related_name='customfield_field'
    )
    group = models.ForeignKey(
        GroupField, on_delete=models.CASCADE,
        related_name='customfield_group',
    )
    is_required = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=False)
    priority = models.IntegerField(unique=False, blank=True, null=True)
    is_identifier = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.field.name}'
    
    class Meta:
        unique_together = ('field', 'group')


class CustomService(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='customfieldvalue_item'
    )
    field = models.ForeignKey(
        CustomField, on_delete=models.CASCADE,
        related_name='customfieldvalue_field'
    )
    value = models.CharField(max_length=4000)

    def __str__(self):
        return f'{self.item.item}.{self.field.field.name}'





# class MainModel(models.Model):
#     name = models.CharField(max_length=100)  # Apenas um exemplo de atributo
#     update_date = models.DateTimeField(
#         auto_now=False, blank=True, null=True,
#     )
#     updated_by = models.ForeignKey(
#         User, on_delete=models.PROTECT, blank=True, null=True,
#         related_name='st_category_updated_by',
#     )
#     approved = models.BooleanField(
#         default=False,
#     )
#     approve_date = models.DateTimeField(
#         auto_now=False, blank=True, null=True,
#     )
#     approved_by = models.ForeignKey(
#         User, on_delete=models.PROTECT, blank=True, null=True,
#         related_name='st_category_approved_by',
#     )
#     pendency = models.ForeignKey(
#         'self', on_delete=models.CASCADE, blank=True, null=True,
#         related_name='st_category_pendency',
#     )
#     def __str__(self):
#         return self.name
