'''
    Copyright (C) 2017 Gitcoin Core 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
from django.core.management.base import BaseCommand
from dashboard.views import profile_keywords_helper
from marketing.models import EmailSubscriber
from app.github import search
import time


def get_github_user(email):
    result = search(email)
    if not result.get('total_count', 0):
        #print(result)
        raise Exception("no users found")

    return result['items'][0]


class Command(BaseCommand):

    help = 'pulls all github login info'

    def handle(self, *args, **options):
        emailsubscribers = EmailSubscriber.objects.filter(github='')
        success = 0
        exceptions = 0
        for es in emailsubscribers:
            #print(es.email)
            try:
                ghuser = get_github_user(es.email)
                es.github = ghuser['login']
                es.keywords = profile_keywords_helper(es.github)
                es.save()
                #print(es.email, es.github, es.keywords)
                success += 1
            except Exception as e:
                #print(e)
                exceptions += 1
                pass
            time.sleep(2)

        print("success: {}".format(success))
        print("total: {}".format(emailsubscribers.count()))
        print("pct: {}".format(round(success / emailsubscribers.count(), 2)))


        print("success: {}".format(exceptions))
        print("total: {}".format(emailsubscribers.count()))
        print("pct: {}".format(round(exceptions / emailsubscribers.count(), 2)))
