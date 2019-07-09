from django.core.management import BaseCommand, CommandError
from django.contrib.sites import requests
from sanity_check.models import Site, Check
import requests, concurrent, requests
from concurrent.futures import ThreadPoolExecutor
from sanitycheck_cli import settings
from django.utils import timezone


def check_site(site):
    print("Starting to check site: %s" % site.url)
    return requests.head(site.url, allow_redirects=True)


class Command(BaseCommand):
    help = "Check Website"

    def store_response(self, site, response):
        site.last_response_code = str(response.status_code)
        site.last_time_checked = timezone.now()
        try:
            site.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error updating site:"))

        try:
            new_check_entry = Check(site=site, response_code=str(response.status_code))
            new_check_entry.save()
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error adding check: %s - %s" % (e, new_check_entry)))


    def handle(self, *args, **options):
        self.stdout.write("[*] Checking all sites...")
        
        with ThreadPoolExecutor(max_workers=settings.MAX_SITE_THREADS) as executor:
            future_to_responses = {executor.submit(check_site, site): site for site in Site.objects.all()}
            for future in concurrent.futures.as_completed(future_to_responses):
                site = future_to_responses[future]
                response = future.result()
                self.stdout.write(self.style.SUCCESS("Response for %s: %s" % (site.url, response.status_code)))
                self.store_response(site, response)

      
            
        #     site.last_response_code = str(response.status_code)
        #     site.last_check = datetime.now()
        #     site.save()

        # try:
        #     new_check = Check(site=site, response_code=str(response.status_code))
        #     new_check.save()
        # except Exception as e:
        #     self.stdout.write(self.style.ERROR("Error adding Check: %s - %s" % (e, new_check)))