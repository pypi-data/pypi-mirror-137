# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utm_tracker', 'utm_tracker.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<5.0']

setup_kwargs = {
    'name': 'django-utm-tracker',
    'version': '1.1',
    'description': 'Django app for extracting and storing UTM tracking values.',
    'long_description': '# Django UTM Tracker\n\nDjango app for extracting and storing UTM tracking values.\n\n## Django support\n\nThis package support Django 3.2+, and Python 3.7+\n\n## Background\n\nThis app has been designed to integrate the standard `utm_*` querystring\nparameters that are used by online advertisers with your Django project.\n\nIt does _not_ replace analytics (e.g. Google Analytics) and Adwords tracking,\nbut does have one crucial difference - it allows you to assign a specific user\nto a campaign advert.\n\nThis may be useful if you are trying to assess the value of multiple channels /\ncampaigns.\n\n### Supported querystring parameters\n\nParameter | Definition\n:-- | :--\nutm_medium | Identifies what type of link was used.\nutm_source | Identifies which site sent the traffic, and is a required parameter.\nutm_campaign | Identifies a specific product promotion or strategic campaign.\nutm_term | Identifies search terms.\ngclid | Identifies a google click, is used for ad tracking in Google Analytics via Google Ads.\naclk | Identifies a Microsoft Ad click (bing), is used for ad tracking.\nmsclkid | Identifies a Microsoft Ad click (MS ad network), is used for ad tracking.\ntwclid | Identifies a Twitter Ad click, is used for ad tracking.\nfbclid | Identifies a Facebook Ad click, is used for ad tracking.\n\nIn addition to the fixed list above, you can also specify custom tags\nusing the `UTM_TRACKER_CUSTOM_TAGS` setting. Any querystring params that\nmatch these tags are stashed in a JSONField called `custom_tags`.\n\n## How it works\n\nThe app works as a pair of middleware classes, that extract `utm_`\nvalues from any incoming request querystring, and then store those\nparameters against the request.user (if authenticated), or in the\nrequest.session (if not).\n\nThe following shows this workflow (pseudocode - see\n`test_utm_and_lead_source` for a real example):\n\n```python\nclient = Client()\n# first request stashes values, but does not create a LeadSource as user is anonymous\nclient.get("/?utm_medium=medium&utm_source=source...")\nassert utm_values_in_session\nassert LeadSource.objects.count() == 0\n\n# subsequent request, with authenticated user, extracts values and stores LeadSource\nuser = User.objects.create(username="fred")\nclient.force_login(user, backend=settings.FORCED_AUTH_BACKEND)\nclient.get("/")\nassert not utm_values_in_session\nassert LeadSource.objects.count() == 1\n```\n\n### Why split the middleware in two?\n\nBy splitting the middleware into two classes, we enable the use case where we\ncan track leads without `utm_` querystring parameters. For instance, if you have\nan internal referral program, using a simple token, you can capture this as a\n`LeadSource` by adding sentinel values to the `request.session`:\n\n```python\ndef referral(request, token):\n    # do token handling\n    ...\n    # medium and source are mandatory for lead source capture\n    request.session["utm_medium"] = "referral"\n    request.session["utm_source"] = "internal"\n    # campaign, term and content are optional fields\n    request.session["utm_campaign"] = "july"\n    request.session["utm_term"] = token\n    request.session["utm_content"] = "buy-me"\n    return render(request, "landing_page.html")\n```\n\n## Configuration\n\nAdd the app to `INSTALLED_APPS`:\n\n```python\n# settings.py\nINSTALLED_APPS = [\n    ...\n    "utm_tracker"\n]\n\nUTM_TRACKER_CUSTOM_TAGS = ["tag1", "tag2"]\n```\n\nand add both middleware classes to `MIDDLEWARE`:\n\n```python\n# settings.py\nMIDDLEWARE = [\n    ...\n    "utm_tracker.middleware.UtmSessionMiddleware",\n    "utm_tracker.middleware.LeadSourceMiddleware",\n]\n```\n\nThe `UtmSession` middleware must come before `LeadSource` middleware.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-utm-tracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
