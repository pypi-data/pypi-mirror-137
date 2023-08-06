# docs-git-revision-date-localized-plugin

Other Docums plugins that use information from git:

- [docums-git-authors-plugin](https://github.com/khanhduy1407/docums-git-authors-plugin) for displaying the authors from git

## Setup

Install the plugin using `pip3` with the following command:

```bash
pip3 install docums-git-revision-date-localized-plugin
```

Next, add the following lines to your `docums.yml`:

```yaml
plugins:
  - search
  - git-revision-date-localized
```

> If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. Docums enables it by default if there is no `plugins` entry set.

The [docurial](https://khanhduy1407.github.io/docurial/) theme has built in support for `git-revision-date-localized` and you should already see the last revision date on the bottom of your pages. See the [documentation](https://khanhduy1407.github.io/docums-git-revision-date-localized-plugin/index.html) on how to fine-tune the appearance and the date format.

### Note when using build environments

This plugin needs access to the last commit that touched a specific file to be able to retrieve the date. By default many build environments only retrieve the last commit, which means you might need to:

<details>
  <summary>Change your CI settings</summary>
    <ul>
      <li>github actions: set <code>fetch-depth</code> to <code>0</code> (<a href="https://github.com/actions/checkout">docs</a>)</li>
      <li>gitlab runners: set <code>GIT_DEPTH</code> to <code>0</code> (<a href="https://docs.gitlab.com/ee/ci/pipelines/settings.html#limit-the-number-of-changes-fetched-during-clone">docs</a>)</li>
      <li>bitbucket pipelines: set <code>clone: depth: full</code> (<a href="https://support.atlassian.com/bitbucket-cloud/docs/configure-bitbucket-pipelinesyml/">docs</a>)</li>
    </ul>
</details>


## Documentation

See [khanhduy1407.github.io/docums-git-revision-date-localized-plugin](https://khanhduy1407.github.io/docums-git-revision-date-localized-plugin/index.html).
