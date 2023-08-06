# docums-git-authors-plugin

Lightweight [Docums](https://khanhduy1407.github.io/docums/) plugin to display git authors of a markdown page:

> Authors: Jane Doe, John Doe

See the [demo](https://khanhduy1407.github.io/docums-git-authors-plugin/). The plugin only considers authors of the current lines in the page ('surviving code' using `git blame`).

Other Docums plugins that use information from git:

- [docums-git-revision-date-localized-plugin](https://github.com/khanhduy1407/docums-git-revision-date-localized-plugin) for displaying the last revision date

## Setup

Install the plugin using pip3:

```bash
pip3 install docums-git-authors-plugin
```

Next, add the following lines to your `docums.yml`:

```yml
plugins:
  - search
  - git-authors
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set.

You can then use the `{{ git_page_authors }}` tag in your markdown document, or choose to customize your docums theme (see [usage](https://khanhduy1407.github.io/docums-git-authors-plugin/usage.html) page in the docs).

### Note when using build environments

This plugin needs access to the last commit that touched a specific file to be able to retrieve the date. By default many build environments only retrieve the last commit, which means you might need to:
<details>
  <summary>Change your CI settings</summary>
  
  - github actions: set `fetch_depth` to `0` ([docs](https://github.com/actions/checkout))
  - gitlab runners: set `GIT_DEPTH` to `1000` ([docs](https://docs.gitlab.com/ee/user/project/pipelines/settings.html#git-shallow-clone))
  - bitbucket pipelines: set `clone: depth: full` ([docs](https://support.atlassian.com/bitbucket-cloud/docs/configure-bitbucket-pipelinesyml/))
</details>


## Documentation

See [khanhduy1407.github.io/docums-git-authors-plugin](https://khanhduy1407.github.io/docums-git-authors-plugin/)
