# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aisexplorer', 'aisexplorer.Utils']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.4,<5.0.0',
 'pandas>=1.3.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tenacity>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'aisexplorer',
    'version': '0.0.13',
    'description': 'Wrapper to fetch data from marinetraffic',
    'long_description': '# AISExplorer\nAISExplorer can be used to locate vessels or to scrape all vessel in an specific AREA. \nAlso free proxies can be used for scraping. Proxies will be scraped from https://www.sslproxies.org/, tested and used.\nAlso Fallback are implemented\n\n## Installation\n\n```\npip install aisexplorer\n```\n\n## Usage\n\n### Find vessel by MMIS\n\n```python\nfrom aisexplorer.AIS import AIS\n\nAIS().get_location(211281610)\n```\n\n### Find vessels in Area\n\n**maximum 500 vessels**\n\n```python\nfrom aisexplorer.AIS import AIS\n\nAIS(return_df= True).get_area_data("EMED")\n```\nOutput is limited to 500 rows.\n[Areas](https://help.marinetraffic.com/hc/en-us/articles/214556408-Areas-of-the-World-How-does-MarineTraffic-segment-them-) can be found here\n\n### Get Table via URL\n\n```python\nfrom aisexplorer.AIS import AIS\n\nAIS(return_df = True).get_data_by_url("https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=time_of_latest_position:desc,flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,area,lat_of_latest_position,lon_of_latest_position,speed,length,width&area_in|in|West%20Mediterranean,East%20Mediterranean|area_in=WMED,EMED&time_of_latest_position_between|gte|time_of_latest_position_between=60,NaN")\n```\n\n\n### Use Proxies\n\n```python\nfrom aisexplorer.AIS import AIS\n\nAIS(return_df = True, Proxy = True).get_data_by_url("https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=time_of_latest_position:desc,flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,area,lat_of_latest_position,lon_of_latest_position,speed,length,width&area_in|in|West%20Mediterranean,East%20Mediterranean|area_in=WMED,EMED&time_of_latest_position_between|gte|time_of_latest_position_between=60,NaN")\n\n```\n\n\n## Next Steps\n\n- Add more potential proxy lists\n- Find a way to change the number of retrys\n- Reset new filters\n\n## Changelog\n\n### 2021-12-10\n\n- Added Fallback if proxy has died\n- Added get data by url\n- Added Check if requests was filtered by cloudflare\n\n### 2021-12-5\n\n- Added Filters early stage\n- Added Retry Options\n- Added some new exceptions\n\n### 2021-11-27\n\n- Added Proxy Option\n\n\n\n\n\n\n',
    'author': 'reyemb',
    'author_email': 'reyemb.coding@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reyemb/AISExplorer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
