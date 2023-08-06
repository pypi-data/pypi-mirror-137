# docums-git-revision-date-plugin

Docums plugin that displays the last revision date of the current page of the documentation based on Git. The revision date will be displayed in ISO format *(YYYY-mm-dd)*.

## Setup
Install the plugin using pip:

`pip install docums-git-revision-date-plugin`

Activate the plugin in `docums.yml`:
```yaml
plugins:
  - search
  - git-revision-date
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [Docums documentation][docums-plugins].

## Usage

### Templates - `page.meta.revision_date`:
#### Example
```django hljs
{% block footer %}
<hr>
<p>{% if config.copyright %}
<small>{{ config.copyright }}<br></small>
{% endif %}
<small>Documentation built with <a href="https://khanhduy1407.github.io/docums/">Docums</a>.</small>
{% if page.meta.revision_date %}
<small><br><i>Updated {{ page.meta.revision_date }}</i></small>
{% endif %}
</p>
{% endblock %}
```

### Markdown - `{{ git_revision_date }}`:
#### Example
```md
Page last revised on: {{ git_revision_date }}
```


[docums-plugins]: https://khanhduy1407.github.io/docums/dev-guide/plugins/

## Options

### `enabled_if_env`

Setting this option will enable the build only if there is an environment variable set to 1. Default is not set.

### `modify_md`

Setting this option to false will disable the use of `{{ git_revision_date }}` in markdown files. Default is true.

### `as_datetime`

Setting this option to True will output git_revision_date as a python `datetime`. This means you can use jinja2 date formatting, for example as `{{ git_revision_date.strftime('%d %B %Y') }}`. Default is false.
