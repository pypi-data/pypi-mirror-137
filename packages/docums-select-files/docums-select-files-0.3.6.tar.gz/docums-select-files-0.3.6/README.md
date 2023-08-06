# File filter plugin for docums

`select-files` is a
[docums plugin](http://khanhduy1407.github.io/docums/user-guide/plugins/) that filters out
files (pages) using a parametrized regular expression.

The main use case for this plugin is to prepare lectures or assignments
and only publishing them at a given date.

## Quick start

1. Install the module using pip: `pip3 install docums-select-files`

2. In your project, add a plugin configuration to `docums.yml`:

   ```yaml
   plugins:
     - select-files:
      select: '^s(\d+)'
      where: 'lambda x : int(x) <= 5'
   ```

  This would search for files named `sNN...` and select only those where `NN` is
  less than or equal to `5`.

  In the `where` expression, you can use the following declared variables
  - `now` : represent the current time in [ISO format](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat)
  - `sfc` : The value of the `SELECT_FILE_CONDITION` environment variable.

  The modules `os` and `datetime` are imported, so you can use methods from them.

## Disabling the plugin

You can disable the plugin using an environment variable. For example, you could configure
your site this way:

```yaml
plugins:
  - select-files:
  select: '^s(\d+)'
  where: 'lambda x : int(x) <= 5'
  disabled_if_env: SELECT_FILES_DISABLED
```

and then, running docums with `SELECT_FILES_DISABLED` set to 1 would disable this plugin
and let all pages be processed:

``` bash
SELECT_FILES_DISABLED=1 docums ...
```

## Similar plugins

- [docums-exclude](https://github.com/khanhduy1407/docums-exclude) : exclude arbitrary file paths and
patterns from the input