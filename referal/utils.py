import random
import string


DONT_USE=['create']
def random_string_generator(size=20, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_code_generator(instance, new_code=None):
	code = instance.user.username
	if code in DONT_USE:
		new_code = "{code}-{randomstr}".format(
					code=code,
					randomstr=random_string_generator(size=4)
				)
		return unique_code_generator(instance,new_code=new_code)
	Klass =instance.__class__
	qs_exists = Klass.objects.filter(code=code).exists()
	if qs_exists:
		new_code = "{code}-{randomstr}".format(
					code=code,
					randomstr=random_string_generator(size=4)
				)
		return unique_code_generator(instance,new_code=new_code)
	return code