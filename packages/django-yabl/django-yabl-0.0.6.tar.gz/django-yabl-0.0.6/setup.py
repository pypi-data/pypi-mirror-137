# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookmarks', 'bookmarks.migrations', 'examples', 'examples.migrations']

package_data = \
{'': ['*'],
 'bookmarks': ['docs/*',
               'static/css/*',
               'static/img/favicons/*',
               'templates/*',
               'templates/bookmarks/*',
               'templates/commons/*',
               'templates/tags/*'],
 'examples': ['fixtures/*', 'templates/*']}

install_requires = \
['Django>=4.0,<5.0',
 'django-debug-toolbar>=3.2.2,<4.0.0',
 'django-extensions>=3.1.5,<4.0.0']

setup_kwargs = {
    'name': 'django-yabl',
    'version': '0.0.6',
    'description': 'Yet another bookmarking library (yabl) for Django. Bookmark and tag arbitrary models.',
    'long_description': "# django-yabl\n\nYet another bookmarking library (yabl) for Django. Bookmark and tag arbitrary models.\n\n`AbstractBookmarkable` contains `bookmarks` field. This enables arbitrary child models, e.g. Movies, Books, Laws, Clothes, etc., to inherit uniform properties for bookmarking and tagging.\n\nThe `bookmarks` field is mapped to a generic `Bookmark` model containing:\n\n1. the authenticated user adding the bookmark, i.e. the `bookmarker`;\n2. the concrete model instance referenced, i.e. the _bookmarked_;[^1] and\n3. a ManyToMany `tags` field which maps to a `TagItem` model.\n\n[^1]: The model is referenced via a `content_type` and an `object_id`\n\n## AbstractBookmarkable\n\nThe abstraction makes each inheriting instance _bookmarkable_ and _taggable_ by authenticated users.\n\n| Attributes                        | Purpose                                                    |\n| --------------------------------- | ---------------------------------------------------------- |\n| `is_bookmarked`(user)             | Check whether object instance is bookmarked or not         |\n| `get_bookmarked`(user)            | Get instances of model that user has bookmarked            |\n| `get_user_tags`(user)             | If user bookmarked, get user-made tags on instance         |\n| `toggle_bookmark`(user)           | Toggle bookmark status as bookmarked or not                |\n| `add_tags`(user, tags: list[str]) | Add unique tags, accepts a list of names                   |\n| `remove_tag`(user, tag: str)      | Delete an existing tag name from tags previously added     |\n| `set_bookmarked_context`(user)    | Combines relevant urls and attributes for template output  |\n| @`modal`                          | Custom modal enables: _toggle_, _add tags_, _remove tag_   |\n| @`launch_modal_url`               | URL to launch custom modal                                 |\n| @`get_item_url`               | URL to load the panel containde within custom modal                                 |\n| @`add_tags_url`                   | URL to POST tags added                                     |\n| @`del_tag_url`                    | URL to DELETE tag added                                    |\n| @`toggle_status_url`              | URL to toggle bookmark status of an object instance added  |\n| @`object_content_for_panel`       | Content when custom modal is loaded; **must** be overriden |\n\n## Modal-based UX\n\n### What is the concept?\n\nThe modal is where the user interacts – i.e. toggle bookmark status, add tags, remove tag (see table above) – with the data.\n\n### How is the modal styled?\n\nSee the htmx/hyperscript example [modal.css](bookmarks/static/css/modal.css).\n\n### How is the modal constructed during run-time?\n\nSee _app-level_ [modal.html](bookmarks/templates/commons/modal.html) which shows a modal via htmx click on the `@launch_modal_url` property.\n\n### What are the pre-made contents of the modal?\n\nThe _app-level_ [panel.html](bookmarks/templates/tags/templates/tags/panel.html), contained within the modal, shows an actionable form for saving the bookmarable object and associating said object with tags:\n\n1. The submission of tags is POST'ed through the `add_tags_url`.\n2. The deletion of tags is DELETE'ed through the `del_tag_url`.\n3. The bookmark toggle is PUT'ed through the `toggle_status_url`.\n\n## Setup\n\n1. Download and [install](bookmarks/docs/setup.md).\n2. See [configuration](bookmarks/docs/configure.md) of models to be bookmarked and tagged.\n3. Examine [frontend](bookmarks/docs/frontend.md) setup using `htmx/hyperscript`.\n",
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/justmars/django-yabl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
