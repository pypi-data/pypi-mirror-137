# File exclude plugin for docums

`docums-exclude` is a
[docums plugin](http://khanhduy1407.github.io/docums/user-guide/plugins/) that allows you
to exclude files from your input using unix-style wildcards (globs) or
regular expressions (regexes).


## Quick start

1. Install the module using pip: `pip3 install docums-exclude`

2. In your project, add a plugin configuration to `docums.yml`:

   ```yaml
   plugins:
     - exclude:
         glob:
           - exclude/this/path/*
           - "*.tmp"
           - "*.pdf"
           - "*.gz"
         regex:
           - '.*\.(tmp|bin|tar)$'
   ```

You can provide zero or more patterns of each type.  (If you don't provide
any patterns, then nothing will happen!)

Note!  Because of peculiarity of yaml syntax, the `glob:` and `regex:` lines
**must not** start with a dash, but the lines under them **must** start with
a dash.

Also because of yaml, patterns that start with a punctuation mark must be
quoted.

When writing regexes, it's best to use single quotes rather than double
quotes, so that your regex backslash escapes are preserved correctly without
having to be doubled up.
