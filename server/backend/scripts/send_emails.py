from collections import defaultdict
import django
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'carebackend.settings'
sys.path.append(os.path.dirname(__file__) + '/..')
django.setup()
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core import mail

from places.models import EmailSubscription

really_send = len(sys.argv) > 1 and (sys.argv[1] == "send")

if len(sys.argv) > 2:
    limit = int(sys.argv[2])
else:
    limit = 1

by_place = defaultdict(list)
for sub in EmailSubscription.objects.filter(
    processed=False,
    place__gift_card_url__isnull=True,
    place__email_contact__isnull=False
):
    by_place[sub.place.place_id].append(sub)

by_place_items = sorted(by_place.items(), key=lambda x: len(x[1]), reverse=True)

with mail.get_connection() as connection:
    for (_, subs) in by_place_items[0:limit]:
        emails_to_notify_about = [x.email for x in subs]
        place = subs[0].place
        if place.gift_card_url:
            print("Skipping", place.name, "because we have a gift card URL for it")
            continue
        sub_pks = [sub.pk for sub in subs]
        place_name = place.name
        to_address = place.email_contact

        plain_emails_to_notify_about = "\n".join(emails_to_notify_about)
        html_emails_to_notify_about = "<br />".join(['<a href="mailto:%s">%s</a>' % (x, x) for x in emails_to_notify_about])

        plain_email_body = f"""
Hi there from the SustainIndyFoods.com team! We’re a volunteer website trying to support Indiana businesses during the COVID-19 crisis. The following people told us via our site that they want to buy gift cards from {place_name}:

{plain_emails_to_notify_about}

We encourage you to email them a link where they can buy gift cards online. If you don’t have an online gift card service yet, one that we like is Gift Fly (https://giftfly.com), since they don’t charge too much and they will deposit funds directly to your bank account. Otherwise you can ask customers to call you so you can do it over the phone.

We’d also like to post your link on SustainIndyFoods.com so more people can buy from you. Share your link with us here: https://sustainindyfoods.com/#/addplace

Thank you, and sending you the best during this crazy time.

Cheers,
The SustainIndyFoods team
    """
        html_email_body = f"""
        <p>Hi there from the <a href="https://sustainindyfoods.com/">SustainIndyFoods.com</a> team! We’re a volunteer website trying to support Indiana businesses during the COVID-19 crisis. The following people told us via our site that they want to buy gift cards from {place_name}:</p>

        <p>
        {html_emails_to_notify_about}</p>

        <p>We encourage you to email them a link where they can buy gift cards online. If you don’t have an online gift card service yet, one that we like is <a href="http://www.giftfly.com/">Gift Fly</a>, since they don’t charge too much and they will deposit funds directly to your bank account. Otherwise you can ask customers to call you so you can do it over the phone.</p>

        <p>We’d also like to post your gift card link on SustainIndyFoods.com so more people can buy from you. <a href="https://sustainindyfoods.com/#/addplace">Share your link with us here</a>.</p>

        <p>Thank you, and sending you the best during this crazy time.</p>

        <p>Cheers,<br/>
        The SustainIndyFoods team</p>
        """
        if not really_send:
            print("Would have sent to %s: %s" % (to_address, place_name))
            continue
        message = EmailMultiAlternatives(
            subject=f"Buying a gift card to support {place_name}",
            body=plain_email_body,
            from_email="SustainIndyFoods Team <info@sustainindyfoods.com>",
            to=[to_address],
            bcc=['m@mikeyk.co'],
            connection=connection,
        )
        message.attach_alternative(html_email_body, 'text/html')
        message.send()
        print("Sent email to", place_name, to_address)
        EmailSubscription.objects.filter(pk__in=sub_pks).update(processed=True)
