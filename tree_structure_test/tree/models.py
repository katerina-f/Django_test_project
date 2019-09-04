from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete='CASCADE',
                               related_name='children')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
