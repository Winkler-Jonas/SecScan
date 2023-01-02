from django.db import models


class Error(models.Model):
    err_code = models.IntegerField()
    err_string = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Error report from: {self.created_at} \n ' \
               f'Error code: {self.err_code} \n' \
               f'Error string: {self.err_string}'
