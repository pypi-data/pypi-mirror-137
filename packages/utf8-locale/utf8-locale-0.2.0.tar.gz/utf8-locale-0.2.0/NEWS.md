# Change log for utf8-locale, the UTF-8-compatible locale detector

0.2.0
-----

- IMPORTANT: the "C" language is now appended to the end of the list
  returned by the `get_preferred_languages()` function if it is not
  already there!

- Add the `get_utf8_vars()` function returning an environment-like
  dictionary that only contains the variables that need to be set,
  i.e. `LC_ALL` and `LANGUAGE`.
- Add the `u8loc` command-line tool to the Python implementation.
- Add the `u8loc.1` manual page.
- Bring the Python build infrastructure somewhat more up to date.
- Add the `tests/functional.py` functional testing tool.
- Require Python 3.7 for dataclasses support.
- Add an EditorConfig definitions file.
- Push the Python implementation into a `python/` source subdirectory.
- Add a Rust implementation.

0.1.1
-----

- Ignore locales with weird names instead of erroring out.
- Ignore the type of a `subprocess.check_output()` mock in the test suite.
- Add a manifest file for the source distribution.

0.1.0
-----

- First public release.
