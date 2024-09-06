from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    duration = models.DurationField()
    # 新增字段
    description = models.TextField(blank=True, null=True)
    kind = models.CharField(max_length=100, blank=True, null=True)
    license = models.CharField(max_length=100, blank=True, null=True)
    # permalink = models.CharField(max_length=1024, unique=True)
    # permalink_url = models.URLField(max_length=2048, blank=True, null=True)

    permalink = models.TextField(blank=True, null=True)
    permalink_url = models.TextField(blank=True, null=True)
    permalink_image = models.TextField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    download_url = models.URLField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.title
