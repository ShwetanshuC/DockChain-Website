from django.test import TestCase

# Create your tests here.
# In Django shell or a view
from django.urls import resolve
from django.urls.exceptions import Resolver404

try:
    match = resolve('/truckmanagement/arduino/active_jobs/0/')
    print(f"Matched view: {match.func}")
    print(f"URL name: {match.url_name}")
    print(f"Args: {match.args}")
    print(f"Kwargs: {match.kwargs}")
except Resolver404:
    print("URL not found")