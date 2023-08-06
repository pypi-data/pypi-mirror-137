# docums-toc-sidebar-plugin

An Docums plugin that allows users to add additional content to the ToC sidebar using the Material theme. 

![demo image](img/docums-toc-sidebar.png)

## Pre-requisites

Currently this plugin will only work with the Table of Contents sidebars in the [Docurial](https://github.com/khanhduy1407/docurial).

## Setup

Install the plugin using pip:

`pip install docums-toc-sidebar-plugin`

Activate the plugin in `docums.yml`:
```yaml
plugins:
  - search
  - toc-sidebar
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

More information about plugins in the [Docums documentation][docums-plugins].

## Usage

To add a toc sidebar to one of your markdown pages, simply add a div anywhere in the markdown source like so:

```markdown
<div markdown=1 class="sidebar">
# Toc Sidebar

It's filled with information specific to this page.

It's locked to the screen just like the ToC!
</div>
```

## See Also

More information about templates [here][docums-template].

More information about blocks [here][docums-block].

[docums-plugins]: https://khanhduy1407.github.io/docums/user-guide/plugins/
[docums-template]: https://khanhduy1407.github.io/docums/user-guide/custom-themes/#template-variables
[docums-block]: https://khanhduy1407.github.io/docums/user-guide/styling-your-docs/#overriding-template-blocks
