from django.http import HttpResponse
from robots.models import Rule, Url
from django.contrib.sites.models import Site

def create_robots_rules():
    site = Site.objects.get(id=1)
    site.domain = '127.0.0.1:8000'
    site.name = 'Gaf Blog'
    site.save()
    
    # Delete existing rules and URLs
    Rule.objects.all().delete()
    Url.objects.all().delete()
    
    # Create new rule
    rule = Rule.objects.create(
        robot='*',
        crawl_delay=1,
    )
    rule.sites.add(site)
    
    # Create URL patterns
    homepage = Url.objects.create(pattern='/$')
    admin_url = Url.objects.create(pattern='/admin/')
    security_url = Url.objects.create(pattern='/security/')
    
    # Allow/Disallow URLs
    rule.allowed.add(homepage)
    rule.disallowed.add(admin_url)
    rule.disallowed.add(security_url)