

from django.ojaale.major.models import Company

from django.template import loader
from django.core.mail import send_mail
# from ojaale.settings import EMAIL_HOST_USER

from views import daily_mails

import datetime
import time
# Create your views here.
User=get_user_model()

	
def send_email_at(send_time):
	time.sleep(send_time.timestamp()-time.time())
	daily_mails()

first_email_time=datetime.datetime(2021,1,26,9,50,0)
interval=datetime.timedelta(days=1)

send_time=first_email_time

while True:
	send_email_at(send_time)
	send_time=send_time+interval