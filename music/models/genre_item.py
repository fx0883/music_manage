from django.db import models

class GenreItem(models.Model):
    image_large_light = models.URLField()
    image_large_dark = models.URLField()
    border_color = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    action_link_navigation_type = models.CharField(max_length=50)
    action_link_id = models.CharField(max_length=100)
    action_link_caption = models.CharField(max_length=255)
    image_small_dark = models.URLField()
    image_medium_dark = models.URLField()
    portrait_size = models.IntegerField()
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image_medium_light = models.URLField()
    landscape_size = models.IntegerField()
    image_small_light = models.URLField()

    def __str__(self):
        return self.title
