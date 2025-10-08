from django.conf import settings
from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    def __str__(self) -> str:
        return self.title

    @property
    def spots_left(self) -> int:
        """
        Number of free spots remaining. Never returns negative.

        Uses related_name 'registrations' on Registration to count current
        registrations.
        """
        taken = self.registrations.count()
        remaining = self.capacity - taken
        return max(0, remaining)


class Registration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # prevent duplicate registration rows
        unique_together = ('user', 'event')
        ordering = ['-registered_at']

    def __str__(self) -> str:
        return f'{self.user} -> {self.event.title}'
