import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from urlparse import urlparse, parse_qs

from django.db import models
from django.forms.models import model_to_dict


class Media(models.Model):
    IMAGE = 'I'
    VIDEO = 'V'
    TYPE = (
        (IMAGE, _("Image")),
        (VIDEO, _("Video")),
    )
    # title        = models.CharField(max, blank=True, null=True_length=200)
    # description  = models.TextField()
    url = models.URLField(max_length=300)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    # video_thumbnail = models.ImageField(upload_to='reports/', blank=True, null=True)
    # external = models.BooleanField()

    def __unicode__(self):
        # return self.file.url
        return self.url

    # def clean(self):
    #   if not self.url:
    #       raise ValidationError('URL can not be empty.')

    def save(self, *args, **kwargs):
        super(Media, self).save(*args, **kwargs)
        if self.file and not self.url:
            self.url = self.file.url
            self.save()
        # else:
        #   self.external = True
        #super(Media, self).save(*args, **kwargs)

    def get_url(self):
        return self.url or self.file.url

    def is_file(self):
        return True if self.file else False

    def is_youtube(self):
        # return self.url.find('youtube.com') >= 0 or self.url.find('youtu.be') >= 0\
        url = urlparse(self.url)
        return url.netloc == 'www.youtube.com' or url.netloc == 'youtu.be'

    def get_youtube_thumbnail_url(self):
        url = urlparse(self.url)
        if url.netloc == 'www.youtube.com':  # self.url.find('youtube.com') >= 0:
            video_id = parse_qs(url.query)['v'][0]
        elif url.netloc == 'youtu.be':  # self.url.find('youtu.be') >= 0:
            video_id = url.path[1:]
        return "http://img.youtube.com/vi/%s/1.jpg" % video_id

    def is_facebook(self):
        # return self.url.find('youtube.com') >= 0 or self.url.find('youtu.be') >= 0\
        url = urlparse(self.url)
        return url.netloc == 'www.facebook.com'

    def get_facebook_embed_url(self):
        url = urlparse(self.url)
        video_id = parse_qs(url.query)['v'][0]
        return "https://www.facebook.com/video/embed?video_id=%s" % video_id

    def serialize(self):
        data = model_to_dict(self)
        # data['file'] = { 'url': self.url }
        data.pop('file')
        data['url'] = self.url
        return data

    class Meta:
        pass
