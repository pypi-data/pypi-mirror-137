# docums-localsearch

A Docums plugin to make the native "search" plugin work locally (file:// protocol).

**NOTE:** This plugin only works with the [Docurial](https://khanhduy1407.github.io/docurial/) theme. If you need support for other themes, feel free to create a pull request.

## Installation (Material v8)

To use the plugin with Material v8 projects:

1. Install the plugin using pip: `pip install docums-localsearch`
2. Activate the plugin in `docums.yml`, in addition to the `search` plugin:
    ```yaml
    plugins:
        - search
        - localsearch
    ```
3. Make sure that the `use_directory_urls` setting is set to `false` in `docums.yml` to have filenames in the URL (required when using the file:/// protocol).
4. Add a `custom_dir` entry to the `theme` section in `docums.yml`:
    ```yaml
    theme:
        name: material
        custom_dir: theme
    ```
5. Create a new file, save it in your project dir as `theme/main.html`, and add the following content: 
    ```html
    {% extends "base.html" %}
    {% block config %}
    {{ super() }}
    {% if "localsearch" in config["plugins"] %}
    <script src="https://unpkg.com/nkduy-iframe/polyfill"></script>
    <script src="{{ 'search/search_index.js' | url }}"></script>
    {% endif %}
    {% endblock %}
    ```
    **Note:** Don't use the `extra_javascript` option in `docums.yml` to add the two scripts above. Scripts referenced via `extra_javascript` are placed at the bottom of the HTML page, i.e., after the search implementation, which is too late.
6. If your documentation should work **offline**, i.e., without internet access:
    1. Open [this file](https://unpkg.com/nkduy-iframe/polyfill) and save it as `iframe-worker.js` in your `docs_dir`.<br>
       Example path: `docs/assets/javascripts/iframe-worker.js`
    2. Edit `theme/main.html` and change the following line:
       ```html
       <script src="https://unpkg.com/nkduy-iframe/polyfill"></script>
       ```
       to this:
       ```html
       <script src="{{ 'assets/javascripts/iframe-worker.js' | url }}"></script>
       ```
