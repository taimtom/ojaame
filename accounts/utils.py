import random
import string

from django.utils.text import slugify

DONT_USE=['create']
def random_string_generator(size=13, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_pkg_generator(instance, package_number=None):


	package_number = "{randomstr}".format(
					randomstr=random_string_generator(size=10)
				)
	Klass =instance.__class__
	qs_exists = Klass.objects.filter(package_number=package_number).exists()
	if qs_exists:
		package_number = "{randomstr}".format(
					randomstr=random_string_generator(size=11)
				)
		return unique_pkg_generator(instance,package_number=package_number)
	return package_number