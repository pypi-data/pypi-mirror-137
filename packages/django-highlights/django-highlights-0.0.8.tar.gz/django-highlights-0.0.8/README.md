# django-highlights

Add a generic relation `Highlight` to arbitrary models.

1. Selecting the highlight is done with custom javascript.
2. Saving the highlightted snippet (without page refresh) is done with `htmx` with a dash of `hyperscript` for dealing with the return trigger.

## Setup

### Install

```zsh
.venv> poetry add django-highlights # pip3 install django-highlights
```

### Add app to project settings

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'highlights'
]
```

### Add highlight model to database

```zsh
.venv> python manage.py migrate
```

## Configuration

### Initialize model

Ensure model, e.g. `Sentinel`, with:

1. a _unique_ SlugField named `slug` - this will be used for creating the `highlight url`
2. a TextField, e.g. `content`/`description` - this is the field that will be _highlightable_

### Add mixin

Make the initialized model inherit from the `AbstractHighlightable` abstract base model :

```python
from django_extensions.db.models import TitleSlugDescriptionModel
from highlights.models import AbstractHighlightable # import
class Sentinel(TitleSlugDescriptionModel, AbstractHighlightable): # add
      pass
```

Each `Sentinel` instance, i.e. pk=1, pk=2, etc., will now have generic relations to a `Highlight` model and have access to a pre-named, `slug`-based `highlight_url`. The `Sentinel` class will now have a `@highlight_path` property to be used in `urlpatterns` so that each instances `highlight_url` is recognized by the project.

### Setup url

```python
# sentinels/urls.py
from .apps import SentinelsConfig # already built when you previously created `sentinels` via python manage.py startapp sentinels
from .models import Sentinel

app_name = SentinelsConfig.name # new
urlpatterns = [
    Sentinel.highlight_path, # new
    ...
]
```

### Use article id with highighter and notice

```jinja
<!-- sentinels/templates/sentinel_detail.html -->

<!-- Note the `object` as the context_object_name -->

<main class="container">
    <h1>Title: {{ object.title }}</h1>

    <!-- 1. article id will be the scope monitored for user highlights -->
    <article id="highlightable">
        {{object.description}}
    </article>
</main>

{% if user.is_authenticated %}
    <!-- 2. a toast box will be triggered on a successful highlight -->
    <div class="position-fixed top-0 end-0 p-3" style="z-index: 11">
        <div id="highlight-notice" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-body">
                <span class="me-auto">Highlight added!</span>
                <button type="button" class="btn-close float-end" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    </div>

    <!-- 3. the footer is unhidden when text within the scope is selected, and will contain a button to highlight -->
    {% load highlighter %}
    {% highlight_btn_show url=object.highlight_url %}
{% endif %}
```

## Flow

1. The `<article>` tag will contain the `scope` or the highlightable text field.
2. The `<footer>` will contain the `url` or the submission of highlights to the server.
3. The specific DOM nodes have event listeners found in `textSelector.js`.
4. Any text selection inside the scoped `<article>` will reflect in the `<footer>`'s hidden `<input>`.
5. When highlight `maker` is ready with text selection, click on footer `<button>` submits highlight stored in `<input>`.
6. The submission is done through `htmx`'s `hx-post` without refreshing or swapping content, i.e. a POST request is sent to the `save_highlight` view c/o the passed `highlight_url`.
7. The request adds a new `Highlight` (from an authenticated highlight `maker`) to the highlightable model instance, e.g. Sentinel pk=2.
8. The successful POST request sends a header trigger to the client to alert the `maker`.
