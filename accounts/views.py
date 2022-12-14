from django.shortcuts import render,get_object_or_404
from cart.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import SaleRecord,Pack
from .serializers import SaleRecordSerializer,PackSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.views.generic import View, ListView, DetailView

from django.template import loader
from django.core.mail import send_mail
from ojaale.settings import EMAIL_HOST_USER
from referal.models import Referral


class SaleRecordApi(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = SaleRecord.objects.all()
        serializer = SaleRecordSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SaleRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.user=request.user
            model_obj=serializer.save()
            cart_,in_cart = Cart.objects.toggle_product(model_obj, request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PackApi(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Pack.objects.all()
        serializer = PackSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data=request.data

        if data:
            cart=get_object_or_404(Cart, user=request.user)
            delivery_fee=data["delivery_fee"]
            new_pack=Pack.objects.create(
                user=cart.user,
                total_price=cart.total+int(delivery_fee),
                delivery_fee=delivery_fee,
                delivery_type=cart.delivery_type

            )
            for obj in cart.content.all():
                new_pack.contents.add(obj)
                new_pack.total_price=+obj.price
                
                #company credited
                company=obj.product.company
                company_gain=obj.price*(95/100)
                company.account.ledger_balance =company.account.ledger_balance+ company_gain
                company.account.save()
                html_message = loader.render_to_string(
                    'main/emails/email1/store-order-details-email.html',
                    {
                        'company': company,
                        'order':obj,
                        'subject':  f'Hurray!!! One of your products have been requested  {obj.product.name} ',
                        
                    }
                )
                send_mail("New product Request Made","message",EMAIL_HOST_USER,[str(company.owner.email)],fail_silently=True,html_message=html_message)
                new_notification=Notification.objects.create(
                    user=request.user,
                    subject="A customer has ordered for your product",
                    message=f"A customer has ordered for your product successfully. You can check out your order information at {company.get_company_url()}/requested/"
                )

                
                #obj(sale record) update
                obj.status="requested"
                obj.paid=True
                obj.package_time=datetime.datetime.now()
                obj.save()

                #product availbability update
                obj.product.availability=obj.product.availability - 1
                obj.product.save()


            #referrer credited
            referrer=Referral.objects.filter(customers=request.user)
            if referrer.exists():
                referrer=referrer.first()
                service_charge=new_pack.total_price*(3.5/100)
                commission=int(referrer.account.percent_commition)/100
                referrer_gain=service_charge*commission
                referrer.account.ledger_balance=referrer.account.ledger_balance+referrer_gain
                referrer.account.save()
                
            html_message = loader.render_to_string(
                            'main/emails/email1/user-order-details-email.html',
                            {
                                'pack':new_pack,
                                'subject':  f'Order Successful. Thanks For Your Orders !!! '
                                
                            }
                        )
            send_mail("Your Order Is Successful","message",EMAIL_HOST_USER,[str(request.user.email)],fail_silently=True,html_message=html_message)
            new_notification=Notification.objects.create(
                user=request.user,
                subject="Your Order Is Successful",
                message="Your order is successful. You can check out your order information at https://ojaa.me/record/my-pack/"
            )
            cart.delete()
            Cart.objects.create(user=request.user)
            return Response( status=status.HTTP_201_CREATED)
        return Response( status=status.HTTP_400_BAD_REQUEST)
def credit_parties(sale_record,user):
    #credit company
    company=sale_record.product.company
    company_gain=sale_record.price*(95/100)
    company.account.available_balance =company.account.available_balance+ company_gain
    company.account.last_cash_recieved=company_gain
    company.account.save()
    html_message = loader.render_to_string(
        'main/emails/email1/store-recieved-order-email.html',
        {
            'company':company,
            "sale_record":sale_record
            
        }
    )
    send_mail(f"Your Account Has Been Credited With N{company_gain}","message",EMAIL_HOST_USER,[str(company.owner.email)],fail_silently=True,html_message=html_message)
    new_notification=Notification.objects.create(
        user=company.owner,
        subject=f"Your Account Has Been Credited With N{company_gain}",
        message=f"Your account has been credited successfully with N{company_gain}. You can check out your order information at https://ojaa.me/referral/{company.slug}"
    )
    referrer=Referral.objects.filter(customers=user)
    if referrer.exists():
        referrer=referrer.first()
        service_charge=new_pack.total_price*(3.5/100) -100
        commission=int(referrer.account.percent_commition)/100
        referrer_gain=service_charge*commission
        referrer.account.available_balance=referrer.account.available_balance+referrer_gain
        referrer.account.last_commistion_recieved=referrer_gain
        referrer.account.total_commition=referrer.account.total_commition+referrer_gain
        referrer.account.save()
        html_message = loader.render_to_string(
            'main/emails/email1/referred-recieved-order-email.html',
            {
            'referrer':referrer,
            
            }
        )
        send_mail(f"Your Account Has Been Credited With {referrer_gain}","message",EMAIL_HOST_USER,[str(referrer.user.email)],fail_silently=True,html_message=html_message)
        new_notification=Notification.objects.create(
            user=referrer.user,
            subject="Your Account Has Been Credited",
            message=f"Your account has been credited with {referrer_gain}. You can this out check at https://ojaa.me/referral/{referrer.user.username}"
        )
def debit_parties(sale_record,user):
    #credit company
    company=sale_record.product.company
    if sale_record.price >= 2000:
        company_gain=sale_record.price*(95/100)-100
    else:
        company_gain=sale_record.price*(95/100)
    company.account.ledger_balance =company.account.ledger_balance- company_gain
    company.account.save()
    referrer=Referral.objects.filter(customers=user)
    if referrer.exists():
        referrer=referrer.first()
        service_charge=new_pack.total_price*(3.5/100)
        commission=int(referrer.account.percent_commition)/100
        referrer_gain=service_charge*commission
        referrer.account.ledger_balance=referrer.account.ledger_balance-referrer_gain
        referrer.account.save()
class CustomerResponseApi(APIView):
    def post(self, request, format=None):
        data=request.data
        user=request.user
        sale_id=data.get("sale_id")
        sale_record=SaleRecord.objects.get(id=sale_id, user=user)
        if data["status"] == "shipped":
            sale_record=SaleRecord.objects.get(id=sale_id, product__company__owner=user)
            sale_record.status="shipped"
            sale_record.collected_time=datetime.datetime.now()
            sale_record.shiping_msg=data.get("ship_msg")
            sale_record.save()
            html_message = loader.render_to_string(
                'main/emails/email1/user-shipped-details-email.html',
                {
                    'order':sale_record,
                    
                }
            )
            send_mail("Your Order Has Been Shipped","message",EMAIL_HOST_USER,[str(sale_record.user.email)],fail_silently=True,html_message=html_message)
            store_message = loader.render_to_string(
                'main/emails/email1/store-shipped-details-email.html',
                {
                    'order':sale_record,
                    
                }
            )
            send_mail(f"{sale_record.user.username.capitalize()} Has Been Told That You Have Shipped His Order","message",EMAIL_HOST_USER,[str(sale_record.user.email)],fail_silently=True,html_message=store_message)
            new_notification=Notification.objects.create(
                user=sale_record.user,
                subject="Your Order Has Been Shipped",
                message="Your order has been shipped. You can check out your order information at https://ojaa.me/record/my-pack/"
            )
        elif data["status"] == "accepted":
            sale_record.status="accepted"
            sale_record.delivery_time=datetime.datetime.now()
            credit_parties(sale_record,user)
            sale_record.save()
            html_message = loader.render_to_string(
                            'main/emails/email1/user-revieved-order-email.html',
                            {
                                'order':sale_record,
                                
                            }
                        )
            send_mail(f"Thanks For Purchasing From {sale_record.product.company.name.capitalize()} Through Ojaa.me","message",EMAIL_HOST_USER,[str(sale_record.user.email)],fail_silently=True,html_message=html_message)
            new_notification=Notification.objects.create(
                user=sale_record.user,
                subject=f"Thanks For Patronizing {sale_record.product.company.name}",
                message="You can check out your order information at https://ojaa.me/record/my-pack/"
            )
            
        elif data["status"] == "rejected":
            sale_record.returned_time=datetime.datetime.now()
            sale_record.status="returned"
            sale_record.return_reason=data.get("return_reason")
            debit_parties(sale_record,user)
            sale_record.save()
            user_message = loader.render_to_string(
                'main/emails/email1/user-rejects-order-email.html',
                {
                    'order':obj,
                    
                }
            )
            html_message = loader.render_to_string(
                'main/emails/email1/store-reject-order-email.html',
                {
                    'order':obj,
                    
                }
            )
            send_mail(f"Thanks.Your Return Request Has Been Accepted ","message",EMAIL_HOST_USER,[str(sale_record.user.email)],fail_silently=True,html_message=user_message)
            new_notification=Notification.objects.create(
                user=sale_record.user,
                subject=f"Your Return Request Has Been Accepted",
                message="You can check out your order information at https://ojaa.me/record/my-pack/returned/"
            )
            send_mail(f"{sale_record.user.username} Has Returned The Package You Shipped","message",EMAIL_HOST_USER,[str(sale_record.product.company.owner.email)],fail_silently=True,html_message=html_message)
            new_notification=Notification.objects.create(
                user=sale_record.product.company.owner,
                subject="The Package You Shipped Has Been Rejected",
                message="Your package has been accepted. You can check out your order information at https://ojaa.me/record/my-pack/"
            )
        return Response(status=status.HTTP_201_CREATED)
    
class MyPack(LoginRequiredMixin,ListView):
    def get_queryset(self, *args, **kwargs):
        qs=Pack.objects.filter(user=self.request.user)
        
        return qs
    def get_context_data(self, *args, **kwargs):
       context=super(MyPack,self).get_context_data(*args, **kwargs)
       pack=Pack.objects.filter(user=self.request.user)
       recent_order=pack.filter(contents__status="requested")
       delivered_order=Pack.objects.filter(contents__status="accepted")
       returned_order=Pack.objects.filter(contents__status="returned")
       shipped_order=Pack.objects.filter(contents__status="shipped")
       context={
           "object":pack,
           "delivered":delivered_order,
           "requested":recent_order,
           "returned":returned_order,
           "shipped":shipped_order,
       }
       return context
class DeliveryResponseApi(APIView):

    def post(self, request, format=None):
        data=request.data
        user=request.user
        sale_id=data.get("sale_id")
        sale_record=SaleRecord.objects.get(id=sale_id, user=user)
        if data["status"] == "collected":
            sale_record.status="collected"
            sale_record.collected_time=datetime.datetime.now()
            sale_record.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

