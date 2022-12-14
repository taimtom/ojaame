from django.db import models
# from django.contrib.postgres.search import SearchVector, SearchQuery
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator
from company.models import Company

from reviews.models import Review

User=settings.AUTH_USER_MODEL



class ProductQuerySet(models.QuerySet):
  def search(self,query=None):
    qs=self
    if query is not None:
      

      look_up=Q()
      for word in query.split():
        look_up &= (Q(name__icontains=query)|
          Q(brand__icontains=query)|
          Q(color__icontains=query)|
          Q(sub_category__icontains=query)|
          Q(category__iexact=query))


      qs=qs.filter(look_up).distinct()
    return qs
  def cat_search(self,category_search=None):
    qs=self
    if category_search is not None:
      look_up=(Q(category__iexact=category_search)|
      Q(name__icontains=category_search)|
      Q(sub_category__iexact=category_search)|
      Q(description__iexact=category_search))
      qs=qs.filter(look_up).distinct()
    return qs

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def search(self,query=None):
		return self.get_queryset().search(query)
  # def cat_search(self,query=None):
	# 	return self.get_queryset().search(category_search)
class Products(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    category=models.TextField()
    sub_category=models.CharField(max_length=100, null=True,blank=True )
    price=models.IntegerField()
    discount=models.IntegerField(default=0)
    discounted_from=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=30, default="New" )
    availability=models.IntegerField(default=0)
    brand=models.CharField(max_length=100)
    size=models.CharField(max_length=100, null=True, blank=True)
    description=models.TextField()
    color=models.CharField(max_length=30,null=True, blank=True)
    rating=models.FloatField(default=0)
    images=models.FileField(upload_to='product/images',null=True, blank=True)
    images_left=models.FileField(upload_to='product/images',null=True, blank=True)
    images_right=models.FileField(upload_to='product/images',null=True, blank=True)
    image=models.FileField(upload_to='product/image')
    timestamp=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(null=True, blank=True)

    objects=ProductManager()

    class Meta:
      ordering=["-timestamp"]


    def __str__(self):
      return self.name
    
    def get_absolute_url(self):
      return reverse("products:detail", kwargs={'slug':self.slug})
    
    @property
    def get_content_type(self):
      instance=self
      content_type=ContentType.objects.get_for_model(instance.__class__)
      return content_type


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	instance.name = instance.name.capitalize()
	if not instance.slug:
		instance.slug =unique_slug_generator(instance)
pre_save.connect(rl_pre_save_receiver, sender=Products)

