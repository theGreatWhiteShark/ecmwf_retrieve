# v0.1.0
- Mention Python version and `setuptools` dependency in README.md
- Sorting the downloaded NetCDF files before joining them all
  together. For some reason the `os.listdir()` function returns the
  files in an unordered list, which causes the joined file to not have
  a proper ordering in time. By an additional ordering of the found
  files before joining them this problem could be resolved.
