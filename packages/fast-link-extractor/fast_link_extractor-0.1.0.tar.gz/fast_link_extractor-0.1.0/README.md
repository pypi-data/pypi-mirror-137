# Fast Link Extractor
**Project under active deveopment**

A Python 3.7+ package to extract links from a webpage. Asyncronous functions allows the code to run fast when extracting from many sub-directories.

A use case for this tool is to extract download links for use with `wget` or `fsspec`.

### Main base-level functions
- `.link_extractor()`: extract links from a given URL
- `.filter_with_regex()`: allows you to filter output with a regular expression
- `.prepend_with_baseurl()`: allows the original URL to be pre-pended to each output

# Installation
## PyPi
```sh
pip install fast-link-extractor
```

# Example
Simply import the package and call `link_extractor()`. This will output of list of extracted links
```python
import fast-link-extractor as fle

# url to extract links from
base_url = "https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/"

# extract all links from sub directories ending with .nc
# this may take ~10 seconds, there are a lot of sub-directories
links = fle.link_extractor(base_url, 
                           search_subs=True,
                           regex='.nc$')
```

# ToDo
- **more tests**: need more tests
- **documentation**: need to setup documentation
