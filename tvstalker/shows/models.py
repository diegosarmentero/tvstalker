from django.db import models


class Serie(models.Model):
    """ Represents a TV show.
    """
    slug = models.SlugField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
"""
    image = models.StringProperty(default='')
    last_season = db.IntegerProperty()
    source_url = db.StringProperty()

    def store_image(self, link):
        file_name = files.blobstore.create(
            mime_type='application/octet-stream')
        with files.open(file_name, 'a') as f:
            f.write(urlfetch.Fetch(link, deadline=60).content)
        files.finalize(file_name)
        self.image_name = file_name


class Season(models.Model):
    nro = db.IntegerProperty()
    serie = db.ReferenceProperty(Serie)


class Episode(models.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    airdate = db.DateProperty()
    season = db.ReferenceProperty(Season)
    nro = db.IntegerProperty()
"""
