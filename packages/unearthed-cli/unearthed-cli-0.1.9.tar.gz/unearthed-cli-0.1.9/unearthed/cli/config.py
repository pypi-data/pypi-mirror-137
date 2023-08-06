"""Unearthed Configuration."""
from os import environ

if environ.get("DEBUG") or environ.get("UNEARTHED_DEBUG"):
    LAMBDA_URL = "https://crowdml-dev.unearthed.solutions/"
    TRACKER_BASE_URL = "https://cms.development-q5nzhaa-ailver3isw3iu.au.platformsh.site"
else:
    if environ.get("UNEARTHED_TEST"):
        LAMBDA_URL = "https://crowdml-test.unearthed.solutions/"
        TRACKER_BASE_URL = "https://cms.development-q5nzhaa-ailver3isw3iu.au.platformsh.site"
    else:
        LAMBDA_URL = "https://crowdml.unearthed.solutions/"
        TRACKER_BASE_URL = "https://data-science.unearthed.solutions"
