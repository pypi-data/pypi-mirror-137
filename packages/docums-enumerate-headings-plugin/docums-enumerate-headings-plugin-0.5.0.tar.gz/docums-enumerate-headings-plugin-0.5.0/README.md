# docums-enumerate-headings-plugin

[Docums](https://khanhduy1407.github.io/docums/) Plugin to enumerate the headings (h1-h6) across Docums pages.

> :point_right: If you're looking to add heading numbers to your site to support exporting to single-page standalone HTML or a PDF file, have a look at [docums-print-site-plugin](https://khanhduy1407.github.io/docums-print-site-plugin/) instead!

## Features :star2:

- Automatically number all headings and (optionally) give each page an sequential chapter number
- Great for writing (technical) reports
- Compatible with `plugins` like [awesome-pages](https://github.com/khanhduy1407/docums-awesome-pages-plugin) and [monorepo](https://github.com/khanhduy1407/docums-monorepo-plugin)
- Compatible with `markdown_extensions` like [pymdownx.snippets](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/)
- Compatible with themes like [docurial](https://github.com/khanhduy1407/docurial)
- Easy to customize styling through CSS

## Setup

Install the plugin using `pip`:

```bash
pip3 install docums-enumerate-headings-plugin
```

Next, add the following lines to your `docums.yml`:

```yml
plugins:
  - search
  - enumerate-headings
```

> Docums executes plugins in the order they are defined. If you use any other plugins that alter the navigation, make sure to define them *before* the `enumerate-headings` plugin.

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set.

## Usage

`enumerate-headings` will increment the chapter number for each new page (in the order they appear in the navigation) and enumerate all subheadings (unless you disable in this in the options).

There is only one requirement: make sure each markdown page starts with a level 1 header (see [how to write markdown headers](https://daringfireball.net/projects/markdown/syntax#header)). Some Docums themes will handle this for your automatically, inserting the page title as a heading 1 if you do not specify one. If a heading 1 is still missing, you'll get a helpful error.

Pages with multiple level 1 headings are allowed and the chapter numbers will increment accordingly.

> Note this plugin does not affect your markdown files, only the rendered HTML.

### Styling

All heading numbers are wrapped in `<span class='enumerate-headings-plugins'></span>` and can be styled using CSS. See [customizing a Docums theme](https://khanhduy1407.github.io/docums/user-guide/styling-your-docs/#customizing-a-theme) on how to add an CSS to your theme.

As an example you can make the numbering lighter than the heading title by saving the CSS snippet below to a file and adding it to your Docums site using the [extra_css](https://khanhduy1407.github.io/docums/user-guide/configuration/#extra_css) setting in your `docums.yml` file.

```css
/* Extra CSS for docums-enumerate-headings-plugin */ 
.enumerate-headings-plugin {
  filter: opacity(35%);
}
```

## Options

You can customize the plugin by setting options in `docums.yml`:

```yml
plugins:
    - enumerate-headings:
        toc_depth: 0
        strict: true
        increment_across_pages: true
        exclude:
          - index.md
          - another_page.md
```

- **`toc_depth`** (default `0`): Up to which level the table of contents should be enumerated as well. Default is 0, which means the TOC is not enumerated at all. Max is 6 (showing all enumeration)
- **`strict`** (default `true`): Raise errors instead of warnings when first heading on a page is not a level one heading (single `#`) and your Docums theme has not inserted the page title as a heading 1 for you. Note that in `strict: false` mode the heading numbers might be incorrect between pages and before and after a level 1 heading.
- **`increment_across_pages`** (default `true`): Increment the chapter number for each new page (in the order they appear in the navigation). If disabled, each page will start from 1.
- **`exclude`** (default *not specified*): Specify a list of page source paths (one per line) that should not have enumeration (excluded from processing by this plugin). This can be useful for example to remove enumeration from the front page. The source path of a page is relative to your `docs/` folder. You can also use [globs](https://docs.python.org/3/library/glob.html) instead of source paths. For example, to exclude `docs/subfolder/page.md` specify in your `docums.yml` a line under `exclude:` with `- subfolder/page.md`
