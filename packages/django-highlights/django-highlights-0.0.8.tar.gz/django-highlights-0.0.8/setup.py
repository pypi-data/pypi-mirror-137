# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['highlights', 'highlights.migrations', 'highlights.templatetags']

package_data = \
{'': ['*'],
 'highlights': ['static/img/favicons/*',
                'static/js/*',
                'templates/*',
                'templates/highlights/*']}

install_requires = \
['Django>=4.0,<5.0',
 'django-debug-toolbar>=3.2.2,<4.0.0',
 'django-extensions>=3.1.5,<4.0.0']

setup_kwargs = {
    'name': 'django-highlights',
    'version': '0.0.8',
    'description': 'Text selection and save as highlight via htmx',
    'long_description': '# django-highlights\n\nAdd a generic relation `Highlight` to arbitrary models.\n\n1. Selecting the highlight is done with custom javascript.\n2. Saving the highlightted snippet (without page refresh) is done with `htmx` with a dash of `hyperscript` for dealing with the return trigger.\n\n## Setup\n\n### Install\n\n```zsh\n.venv> poetry add django-highlights # pip3 install django-highlights\n```\n\n### Add app to project settings\n\n```python\n# in project_folder/settings.py\nINSTALLED_APPS = [\n    ...,\n    \'highlights\'\n]\n```\n\n### Add highlight model to database\n\n```zsh\n.venv> python manage.py migrate\n```\n\n## Configuration\n\n### Initialize model\n\nEnsure model, e.g. `Sentinel`, with:\n\n1. a _unique_ SlugField named `slug` - this will be used for creating the `highlight url`\n2. a TextField, e.g. `content`/`description` - this is the field that will be _highlightable_\n\n### Add mixin\n\nMake the initialized model inherit from the `AbstractHighlightable` abstract base model :\n\n```python\nfrom django_extensions.db.models import TitleSlugDescriptionModel\nfrom highlights.models import AbstractHighlightable # import\nclass Sentinel(TitleSlugDescriptionModel, AbstractHighlightable): # add\n      pass\n```\n\nEach `Sentinel` instance, i.e. pk=1, pk=2, etc., will now have generic relations to a `Highlight` model and have access to a pre-named, `slug`-based `highlight_url`. The `Sentinel` class will now have a `@highlight_path` property to be used in `urlpatterns` so that each instances `highlight_url` is recognized by the project.\n\n### Setup url\n\n```python\n# sentinels/urls.py\nfrom .apps import SentinelsConfig # already built when you previously created `sentinels` via python manage.py startapp sentinels\nfrom .models import Sentinel\n\napp_name = SentinelsConfig.name # new\nurlpatterns = [\n    Sentinel.highlight_path, # new\n    ...\n]\n```\n\n### Use article id with highighter and notice\n\n```jinja\n<!-- sentinels/templates/sentinel_detail.html -->\n\n<!-- Note the `object` as the context_object_name -->\n\n<main class="container">\n    <h1>Title: {{ object.title }}</h1>\n\n    <!-- 1. article id will be the scope monitored for user highlights -->\n    <article id="highlightable">\n        {{object.description}}\n    </article>\n</main>\n\n{% if user.is_authenticated %}\n    <!-- 2. a toast box will be triggered on a successful highlight -->\n    <div class="position-fixed top-0 end-0 p-3" style="z-index: 11">\n        <div id="highlight-notice" class="toast hide" role="alert" aria-live="assertive" aria-atomic="true">\n            <div class="toast-body">\n                <span class="me-auto">Highlight added!</span>\n                <button type="button" class="btn-close float-end" data-bs-dismiss="toast" aria-label="Close"></button>\n            </div>\n        </div>\n    </div>\n\n    <!-- 3. the footer is unhidden when text within the scope is selected, and will contain a button to highlight -->\n    {% load highlighter %}\n    {% highlight_btn_show url=object.highlight_url %}\n{% endif %}\n```\n\n## Flow\n\n1. The `<article>` tag will contain the `scope` or the highlightable text field.\n2. The `<footer>` will contain the `url` or the submission of highlights to the server.\n3. The specific DOM nodes have event listeners found in `textSelector.js`.\n4. Any text selection inside the scoped `<article>` will reflect in the `<footer>`\'s hidden `<input>`.\n5. When highlight `maker` is ready with text selection, click on footer `<button>` submits highlight stored in `<input>`.\n6. The submission is done through `htmx`\'s `hx-post` without refreshing or swapping content, i.e. a POST request is sent to the `save_highlight` view c/o the passed `highlight_url`.\n7. The request adds a new `Highlight` (from an authenticated highlight `maker`) to the highlightable model instance, e.g. Sentinel pk=2.\n8. The successful POST request sends a header trigger to the client to alert the `maker`.\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/justmars/django-highlights',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
