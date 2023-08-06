# User Guide

## Installation

Install the latest pip package with:

```bash
  pip install sphinx-zama-theme
```

create a `docs` directory and run `sphinx-quickstart` to bootstrap the documentation content.

```
tree -L 1
.
├── Makefile
├── _build
├── _static
├── _templates
├── conf.py
├── index.rst
└── make.bat
```

## Configuration

Start by adding required extra vars at the top of your `conf.py` file. `author` and `description` will be
added as `META` information of the html rendered doc. `root_url` will be used for multi versions if your site is hosting several documentations, but you could safely copy/paste even if you won't use it.

```python
import os

author = "Zama"
description = "Project description in 1-3 line(s)"
root_url = os.environ.get("SPHINX_ROOT_URL", "")
```

Open `conf.py` and allow `myst_parser` for Markdown support, and `sphinx_copybutton` for
easy code blocks copy/pasting.

```
extensions = [
    "myst_parser",
    "sphinx_copybutton",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "dollarmath",
]
```

And select `sphinx_zama_theme` html theme:

```python
html_theme = 'sphinx_zama_theme'
html_theme_options = {
    "navigation_depth": 2,
    "collapse_navigation": False,
}
html_context = {
    "show_version": False,
    "author": author,
    "description": description,
    "language": "en",
    "versions_url": "#",
}
html_title = "%s Manual" % (project)

def setup(app):
    html_init = f"const CURRENT_VERSION = {release!r};"
    html_init += f"const ROOT_URL = {root_url!r};"
    app.add_js_file(None, body=html_init, priority=100)

```

At that point your documentation should compile for html output:

```shell
$ cd <docs rep>
$ make html
```

and you could start adding content.

## Content writing

Sphinx support **Restructured Text** by default and **Markdown** with `Myst parser`.
Both offers more or less the same features with less advanced elements supported by Markdown.

You could see in the respective `RST Syntax` and `MD Syntax` a list of all supported syntax.

```
Even if you go with Markdown, `index` files should be still in **RST** format
```

For more example on the supported syntax please see either `RST Syntax` or `MD Syntax`.

## Settings

### Custom logo

If you do not have any logo for your project, the name of your project will be displayed
instead in top left (like this sample documentation).

if you have a logo just add the following line:

```python
…
html_theme = 'sphinx_zama_theme'
html_logo = '_static/logo.png'
html_theme_options = {
…
```

### External link to Github / Twitter

If your project has a public repository or a dedicated twitter account you could link by adding these
extra lines in your `conf.py`:

```python
…
html_theme_options = {
    "github_url": "https://github.com/xxx",
    "twitter_url": "https://twitter.com/xxx",
    …
}
```

### Custom external link

If you want to add custom external links in the right top bar you need an icon ([Font awesome icon](https://fontawesome.com/v5.15/icons)
for example), a name and an address and add these lines in your `conf.py`. Here are 2 examples:

```python
…
html_theme_options = {
    …
    "icon_links": [{
        "url": "https://docs.zama.ai",
        "icon": "fas fa-home",
        "name": "Documentation main page",
    },
    {
        "url": "https://community.zama.ai/",
        "icon": "fab fa-discourse",
        "name": "Discourse",
    }],
    …
}
```

### Version

If you want to display the current version of the doc, make sure the `release` variable is correctly set (dynamically or statically).

```python
# The full version, including alpha/beta/rc tags
release = '0.1'
```

Then add in your `conf.py`:

```python
html_context = {
    "show_version": True,
    "versions_url": "#",
    …
}
```

The `versions_url` set to `#` is a workaround to just use one version of the doc. If you want to support
multiple versions of the doc just see below.

### Multi-versions

```{important}
Multi-version support has several requirements on target documentation architecture, it is not easy to switch from a single-version to multi-version so make sure you decide which way to go early.
```

Multi version implies that your tagged versions are in a dedicated directory (e.g.: `v0.1` documentation is in directory `v0.1`).
Ci-side you have to take that into account, you also need a symlink `latest` to the latest version of your docs (this one will be the one to link externally
and also the default one to redirect to when reaching the root url).

All the older versions are accessible thanks to a `versions.json` file that should looks like:

```json
{
    "all": [
      "main",
      "v0.0.3",
      "v1.0.0",
      "v1.0.1"
    ],
    "menu": [
      "main",
      "v1.0.0",
      "v1.0.1"
    ],
    "latest": "v1.0.1",
  }

```

If you host several documentation on the same server, your `versions.json` must be hosted in the project subdirectory root. To let sphinx
know this URL, please set `DOC_ROOT_URL` environment variable to the relative path to your project root e.g.:

```shell
DOC_ROOT_URL="/sphinx_zama_theme/" make html
```

Note that `DOC_ROOT_URL` should start with a `/` and end with a `/`

## Automatic Redirection to latest docs

If you want to have an automatic redirection from `<your-doc-site>/<DOC_ROOT_URL>` to `<your-doc-site>/<DOC_ROOT_URL>/<latest_version>` you should
first set a `versions.json` (see above) and then copy the following code to a `index.html` file in the same `<your-doc-site>/<DOC_ROOT_URL>` location. It will fetch the
`versions.json` and redirect to the latest version read from it.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <script>
      window.fetch('versions.json').then(function(response) { response.json().then(function(data) { window.location.href = data.latest; }); });
    </script>
  </head>
  <body>
    <h3>Something went wrong. No versions file found!</h3>
  </body>
</html>
```


## Live rebuild

If you want quick preview of your work you could install an extra package
called `sphinx-autobuild`

```shell
pip install sphinx-autobuild
```

and launch it directory (update `<docs>` with your project documentation path):

```shell
cd <docs>
python -m sphinx_autobuild . _build
```

This will launch a local web server on port 8000 by default with updated rendered version
on each source modifications.

## Continuous Integration

To see an example of building and deploying docs with github action see the current repository
actions file.
