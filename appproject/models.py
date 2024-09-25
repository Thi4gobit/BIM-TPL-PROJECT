from django.db import models


class Field(models.Model):
    
    name = models.CharField(max_length=32)
    template = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class FieldLink(models.Model):

    field = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        related_name='fieldlink_fields'
    )
    subfield = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        related_name='fieldlink_subfields'
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
                name='unique_together_field_subfield'
            )
        ]


class Group(models.Model):

    name = models.CharField(max_length=32)
    template = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class GroupSet(models.Model):

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        related_name='customfield_group',
    )
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE,
        related_name='customfield_field'
    )
    
    def __str__(self):
        return f'{self.field.name}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'field'],
                name='unique_together_group_field'
            )
        ]


class Item(models.Model):

    item = models.CharField(max_length=255)
    template = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.item}'


class Obj(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE,
        related_name='customfieldvalue_item'
    )
    field = models.ForeignKey(
        GroupSet, on_delete=models.CASCADE,
        related_name='customfieldvalue_field'
    )
    value = models.CharField(
        max_length=4000, blank=True, null=True
    )
    is_identifier = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item.item}.{self.field.field.name}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'field'],
                name='unique_together_item_field'
            )
        ]
