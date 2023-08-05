import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse
from django.utils.functional import classproperty
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel


class Highlight(TimeStampedModel):
    """The `AbstractHighlightable` model has a highlights field which map to this model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # main fields
    content = models.TextField(editable=False)
    is_public = models.BooleanField(default=False, editable=False)
    maker = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name="highlights",
        editable=False,
    )

    # generic fk base, uses CharField to accomodate sentinel models with UUID as primary key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return (
            f"{self.content[:15]}... by {self.maker}"
            or "No content in {self.id} by {self.maker}"
        )


class AbstractHighlightable(models.Model):
    highlights = GenericRelation(
        Highlight, related_query_name="%(app_label)s_%(class)ss"
    )

    class Meta:
        abstract = True

    @classproperty
    def _highlight_label(cls) -> str:
        return f"highlight_{cls._meta.model_name}"

    @property
    def highlight_url(self) -> str:
        """Each inheriting model instance will have its own `@highlight_url`."""
        return reverse(
            f"{self._meta.app_label}:{self._highlight_label}",
            args=(self.slug,),
        )

    @classproperty
    def highlight_path(cls) -> URLPattern:
        """Note `name` of path and relation to each instance's `highlight_url`. Each inheriting model will have access to the `highlight_url`, provided it's added to the namespaced `urlpatterns`."""
        return path(
            f"{cls._highlight_label}/<slug:slug>",
            cls._save_highlight,
            name=cls._highlight_label,
        )

    @classmethod
    def _save_highlight(cls, request: HttpRequest, slug: str) -> HttpResponse:
        if not request.user.is_authenticated:  # required to highlight
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        highlight = Highlight(
            content=request.POST.get("highlight"),
            maker=request.user,
            content_object=cls.objects.get(slug=slug),
        )
        highlight.save()

        return HttpResponse(request, headers={"HX-Trigger": "highlightSaved"})
