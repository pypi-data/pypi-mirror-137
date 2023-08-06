# docums-monorepo-plugin

> **Note: This plugin is in beta.** Whilst it is not expected to significantly change in functionality, it may not yet be fully compatible with other Docums configuration and thus may break with some advanced configurations. Once these have been resolved and all bugs have been ironed out, we will move this to a stable release.

✚ This plugin enables you to build multiple sets of documentation in a single Docums. It is designed to address writing documentation in Spotify's largest and most business-critical codebases (typically monoliths or monorepos).

## Features

- **Support for multiple `docs/` folders in Docums.** Having a single `docs/` folder in a large codebase is hard to maintain. Who owns which documentation? What code is it associated with? Bringing docs closer to the associated code enables you to update them better, as well as leverage folder-based features such as [GitHub Codeowners].

- **Support for multiple navigations.** In Spotify, large repositories typically are split up by multiple owners. These are split by folders. By introducing multiple `docums.yml` files along with multiple `docs/` folder, each team can take ownership of their own navigation. This plugin then intelligently merges of the documentation together into a single repository.

- **Support across multiple repositories.** Using [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) it is possible to merge documentation across multiple repositories into a single codebase dynamically.

- **The same great Docums developer experience.** It is possible to run `docums serve` in the root to merge all of your documentation together, or in a subfolder to build specific documentation. Autoreload still works as usual. No more using [symlinks](https://devdojo.com/tutorials/what-is-a-symlink)!

## Install

It's easy to get started using [PyPI] and `pip` using Python:

```terminal
$ pip install docums-monorepo-plugin
```

## Usage

Take a look in [our sample project](./sample-docs) for an example implementation, or see [what it looks like after running `docums build`](https://khanhduy1407.github.io/docums-monorepo-plugin/monorepo-example/).

In general, this plugin introduces the `!include` syntax in your Docums navigation structure and then merges them together.

```yaml
# /docums.yml
site_name: Cats API

nav:
  - Intro: 'index.md'
  - Authentication: 'authentication.md'
  - API:
    - v1: '!include ./v1/docums.yml'
    - v2: '!include ./v2/docums.yml'

plugins:
  - monorepo

# /src/v1/docums.yml
site_name: versions/v1

nav:
  - Reference: "reference.md"
  - Changelog: "changelog.md"

# /src/v2/docums.yml
site_name: versions/v2

nav:
  - Migrating to v2: "migrating.md"
  - Reference: "reference.md"
  - Changelog: "changelog.md"

```

#### Example Source Filetree

```terminal
$ tree .

├── docs
│   ├── authentication.md
│   └── index.md
├── docums.yml
├── v1
│   ├── docs
│   │   ├── changelog.md
│   │   └── reference.md
│   └── docums.yml
└── v2
    ├── docs
    │   ├── changelog.md
    │   ├── migrating.md
    │   └── reference.md
    └── docums.yml

5 directories, 10 files
```

#### Example Rendered Filetree

```
$ docums build
$ tree ./site

├── 404.html
├── authentication
│   └── index.html
├── css
│   ├── base.css
│   ├── bootstrap-custom.min.css
│   └── font-awesome.min.css
├── fonts
│   ├── fontawesome-webfont.eot
│   ├── fontawesome-webfont.svg
│   ├── fontawesome-webfont.ttf
│   ├── fontawesome-webfont.woff
│   ├── fontawesome-webfont.woff2
│   ├── glyphicons-halflings-regular.eot
│   ├── glyphicons-halflings-regular.svg
│   ├── glyphicons-halflings-regular.ttf
│   ├── glyphicons-halflings-regular.woff
│   └── glyphicons-halflings-regular.woff2
├── img
│   ├── favicon.ico
│   └── grid.png
├── index.html
├── js
│   ├── base.js
│   ├── bootstrap-3.0.3.min.js
│   └── jquery-1.10.2.min.js
├── sitemap.xml
├── sitemap.xml.gz
└── versions
    ├── v1
    │   ├── changelog
    │   │   └── index.html
    │   └── reference
    │       └── index.html
    └── v2
        ├── changelog
        │   └── index.html
        ├── migrating
        │   └── index.html
        └── reference
            └── index.html

13 directories, 28 files
```

Note that, as of `v0.5.2`, the `*include` syntax can be used in place of `!include` in order to compile any number of `docums.yml` files that match a glob-like pattern, without having to specify every one individually. For example:


```yaml
# /docums.yml
site_name: Cats System

nav:
  - Intro: 'index.md'
  - Components: '*include ./components/*/docums.yml'
```

#### Example Source Filetree

```terminal
$ tree .

├── components
│   ├── belly-rubs
│   │   ├── docs
│   │   |   └── index.md
│   │   └── docums.yml
|   ├── purring
│   │   ├── docs
│   │   |   └── index.md
│   │   └── docums.yml
|   └── skritches
│   │   ├── docs
│   │   |   └── index.md
│   │   └── docums.yml
├── docs
│   └── index.md
└── docums.yml

8 directories, 8 files
```

## Supported Versions

- Python 3 &mdash; 3.6, 3.7
- [Docums] 1.0.0.0 and above.

[khanhduy1407/docums]: https://github.com/khanhduy1407/docums
[docums-plugin-template]: https://github.com/khanhduy1407/docums-plugin-template
[pypi]: https://pypi.org
[docums]: https://khanhduy1407.github.io/docums
[github codeowners]: https://help.github.com/en/articles/about-code-owners
