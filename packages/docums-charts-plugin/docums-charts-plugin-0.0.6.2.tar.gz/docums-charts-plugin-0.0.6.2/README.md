# docums-charts-plugin

[Docums](https://khanhduy1407.github.io/docums/) plugin to create plots from data using the declarative [vegalite](https://vega.github.io/vega-lite/) syntax. This makes it easier to build reproducible reports.

👉 See it in action on the [demo page](https://khanhduy1407.github.io/docums-charts-plugin/demo/)

Includes supports for [docurial](https://github.com/khanhduy1407/docurial) theme features like [instant loading](https://khanhduy1407.github.io/docurial/setup/setting-up-navigation/?h=reload#instant-loading) and [dark color themes](https://khanhduy1407.github.io/docurial/setup/changing-the-colors/#color-palette-toggle).

## Installation

Install the plugin using `pip3`:

```shell
pip3 install docums-charts-plugin
```

Next, add the following lines to your `docums.yml`:

```yml
plugins:
  - search
  - charts

extra_javascript:
  - https://cdn.jsdelivr.net/npm/vega@5
  - https://cdn.jsdelivr.net/npm/vega-lite@5
  - https://cdn.jsdelivr.net/npm/vega-embed@6

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: vegalite
          class: vegalite
          format: !!python/name:docums_charts_plugin.fences.fence_vegalite
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set.

## Usage

You can insert any valid [vegalite](https://vega.github.io/vega-lite/) JSON into a markdown file using:

````
```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A simple bar chart with embedded data.",
  "data": {
    "values": [
      {"a": "A", "b": 28}, {"a": "B", "b": 55}, {"a": "C", "b": 43},
      {"a": "D", "b": 91}, {"a": "E", "b": 81}, {"a": "F", "b": 53},
      {"a": "G", "b": 19}, {"a": "H", "b": 87}, {"a": "I", "b": 52}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "b", "type": "quantitative"}
  }
}
```
````

See the [vegalite editor](https://vega.github.io/editor/#/) for a range of examples you could copy-paste into your docums site

## Documentation

See the documentation [khanhduy1407.github.io/docums-charts-plugin](https://khanhduy1407.github.io/docums-charts-plugin/) for examples, use cases and options.

