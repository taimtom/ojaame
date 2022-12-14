# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import  CompanySerializers

#python


from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView
from .models import Company, BankAccountDetail
from product.models import Products
from django.http import HttpResponseRedirect,Http404
from django.contrib import messages
from .forms import CompanyForm,CompanyAccountForm#, ProductForm
from accounts.models import SaleRecord
# Create your views here.

class Companies(ListView):
   template_name='main/company/companies.html'
   queryset=Company.objects.all()

class CompanyProfile(DetailView):
   def get_object(self):
       slug= self.kwargs.get("slug")
       if slug is None:
           raise Http404
       return get_object_or_404(Company,slug__iexact=slug)
   template_name="main/company/profile.html"
   def get_context_data(self, *args, **kwargs):
       context=super(CompanyProfile,self).get_context_data(*args, **kwargs)
       company=self.get_object()
       sale_record=SaleRecord.objects.filter(product__company=company)
       delivered_record=SaleRecord.objects.filter(product__company=company, status__iexact="delivered", paid=True)
       requested_record=SaleRecord.objects.filter(product__company=company, paid=True)
       returned_record=SaleRecord.objects.filter(product__company=company, status__iexact="returned", paid=True)
       top_rated=Company.objects.order_by("rating")
       context={
           "object":company,
           "top_rated":top_rated,
           "delivered":delivered_record,
           "requested":requested_record,
           "returned":returned_record,
       }
       return context
@login_required()
def companyaccount(request,slug=None):
    instance=get_object_or_404(Company, slug=slug)
    mysales=SaleRecord.objects.filter(paid=True, product__company=instance)
    customers=[sale.user for sale in mysales]
    if request.user != instance.owner:
        return HttpResponseRedirect(f"/{slug}")
    
    context={
       "account":instance.account,
       "object":instance,
       "customers":set(customers)
       
       }
    template_name='main/company/profile-acc.html'
   
        
    
    return render(request, template_name,context)
@login_required()
def companybankaccount(request):
    obj=get_object_or_404(Company, owner=request.user)
    if not obj:
        return HttpResponseRedirect("/create/form/")
    else:
        form = CompanyAccountForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=obj
            instance.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect('/products/create/form/')  
        context={
            "object":obj,
            "form":form,
            "title":"Add Bank Account",
            "button":"Add"
        }
    template_name='main/company/form.html'
    return render(request, template_name,context)
@login_required()
def companycreate_view(request):
  company=Company.objects.filter(owner=request.user)
  if company:
    return HttpResponseRedirect("/update/form/")
  else:
    form = CompanyForm(request.POST, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.owner=request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect('/products/create/form/')
        
    if form.errors:
        print(form.errors)
        context={"form":form}
    context={
       "form":form,
       "title":"Create Your Online Store",
       "button":"Creaate Store"
       }
    template_name='main/company/form.html'
   
        
    
    return render(request, template_name,context)
@login_required()
def companyupdate_view(request):
  company=Company.objects.filter(owner=request.user)
  if not company:
    return HttpResponseRedirect("/create/form/")
  else:
    obj=get_object_or_404(Company, owner=request.user)
    if request.method=='POST':
      form = CompanyForm(request.POST, request.FILES, instance=obj)
      if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_company_url())
    else:
      form=CompanyForm(instance=obj)
    context={
       "form":form,
       "title":"Update Your Online Store",
       "button":"Update Store"
       }
    template_name='main/company/form.html'
   
        
    
    return render(request, template_name,context)
    
# def productscreate_view(request, slug=None):
#     form = ProductForm(request.POST)
#     instances=get_object_or_404(Company,slug=slug)
#     if form.is_valid():
#         instance=form.save(commit=False)
#         instance.company=instances
#         print(instance.company)
#         instance.save()
#         messages.success(request, "Successfully Created")
#         return HttpResponseRedirect(f'/company/{instances.slug}')
        
#     if form.errors:
#         print(form.errors)
#         context={"form":form}
#     context={
#        "form":form,
#        "title":"Add Product To Store",
#        "button":"Add"
#        }
#     template_name='main/company/form.html'
   
        
    
#     return render(request, template_name,context)
 

 

#Api Views-------------------------------------------------------------------------------------------------

class ApiCompanyList(APIView):
    """
    List all companys, or create a new company.
    """
    def get(self, request, format=None):
        companys = Company.objects.all()
        serializer = CompanySerializers(companys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompanySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApiCompanyDetail(APIView):
    """
    Retrieve, update or delete a Company instance.
    """
    def get_object(self, slug):
        try:
            return Company.objects.get(slug=slug)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        company = self.get_object(slug)
        serializer = CompanySerializers(company)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        company = self.get_object(slug)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        company = self.get_object(slug)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)