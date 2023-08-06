# docums-tooltipster-links-plugin

An Docums plugin that adds tooltips to preview the content of page links using tooltipster

## Setup

### Install the Plugin

Install the plugin using pip:

`pip install docums-tooltipster-links-plugin`

Activate the plugin in `docums.yml`:
```yaml
plugins:
  - search
  - tooltipster-links
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [Docums documentation][docums-plugins].

### Install Tooltipster

Download Tooltipster and add the css and javascript to `docums.yml`:

```yml
extra_css:
  - css/tooltipster.bundle.min.css

extra_javascript:
  - js/tooltipster.bundle.js  
```

Create custom directory and `main.html` file for overriding the `extra_head` template block

```sh
mkdir theme
touch theme/main.html
```

Add the following to `main.html`:
```html
{% extends "base.html" %}

{% block extrahead %}
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script>
                $(document).ready(function() {
                    $('.link-tooltip').tooltipster();
                });
        </script>
{% endblock %}
```
Add the custom directory to `docums.yml`:
```yml
theme:
  name: docums
  custom_dir: theme
```

Add additonal css to the site (either in a new css file or existing one):
```css
.tooltip_templates { display: none; }
```

## Usage
Once configured property, tooltips-links should create tooltips automagically!

## See Also

More information about templates [here][docums-template].

More information about blocks [here][docums-block].

[docums-plugins]: https://khanhduy1407.github.io/docums/user-guide/plugins/
[docums-template]: https://khanhduy1407.github.io/docums/user-guide/custom-themes/#template-variables
[docums-block]: https://khanhduy1407.github.io/docums/user-guide/styling-your-docs/#overriding-template-blocks
