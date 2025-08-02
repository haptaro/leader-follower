from django.db import models

class Note(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'auth.User',
        related_name='notes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message[:30]
