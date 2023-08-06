# docums-print-site-plugin

[Docums](https://khanhduy1407.github.io/docums/) plugin that adds a print page to your site that combines the entire site, allowing for easy export to PDF and standalone HTML. See [demo](https://khanhduy1407.github.io/docums-print-site-plugin/print_page.html).

## Features :star2:

- Support for [docurial](https://github.com/khanhduy1407/docurial) theme, including features like instant loading and dark color themes.
- Support for pagination in PDFs.
- Many options to customize appearance
- Option to add a cover page
- Lightweight, no dependencies.

## Setup

Install the plugin using `pip3`:

```bash
pip3 install docums-print-site-plugin
```

Next, add the following lines to your `docums.yml`:

```yml
plugins:
  - search
  - print-site
```

> ⚠️ Make sure to put `print-site` to the **bottom** of the plugin list. This is because other plugins might alter your site (like the navigation), and you want these changes included in the print page.

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set.

## Usage

- Navigate to `/print_page/` or `print_page.html`
- Export to standalone HTML (see [export to HTML](https://khanhduy1407.github.io/docums-print-site-plugin/how-to/export-HTML.html))
- Export to PDF using your browser using *File > Print > Save as PDF*  (see [export to PDF](https://khanhduy1407.github.io/docums-print-site-plugin/how-to/export-PDF.html))

## Documentation

Available at [khanhduy1407.github.io/docums-print-site-plugin](https://khanhduy1407.github.io/docums-print-site-plugin/).
