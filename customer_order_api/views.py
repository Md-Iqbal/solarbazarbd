import datetime
import json

from django.contrib import messages
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.verification import Verification
# from .models import UserRole, TaxList
from .serializers import *


# Create your views here.


def send_notification(user_from, user_to, title):
    user_from_instance = User.objects.get(username=user_from)
    user_to_instance = User.objects.get(username=user_to)
    Notification.objects.create(
        user_from=user_from_instance,
        user_to_instance=user_to_instance,
        title=title
    )


# class CreateOrder
class OrderList(generics.ListAPIView):
    """
    endpoint for viewing order only for admin
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ShopOrderList(generics.ListAPIView):
    """
    vendor owner order list. Only owner of the store can view this list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(
            vendor__user=self.request.user
        )
        return queryset


class PaymentDetailsView(generics.RetrieveUpdateAPIView):
    """
    vendor owner order list. Only owner of the store can view this list
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentDetailsSerializer
    queryset = PaymentDetails.objects.all()


class OrderCreate(generics.CreateAPIView):
    """
    endpoint for creating order
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    # queryset = Order.objects.all()

    def perform_create(self, serializer):
        sub_total = 0
        grand_total = 0
        total_price = 0
        user = self.request.user
        # vendor_user = serializer.validated_data['vendor']
        # search shop tax list
        # shop_tax_list = TaxList.objects.filter(
        #     shop=vendor_user)
        #
        # total_tax_value = 0
        # for i in shop_tax_list:
        #     total_tax_value += i.tax_value
        print('Accessed by request:   ' + self.request.data['ordered_by'])
        customer_ins = None
        customer_address = None
        if serializer.validated_data['ordered_by'] == 'ecommerce':
            ordered_by = 'ecommerce'
            print(serializer.validated_data['ordered_by'])
            try:
                customer_ins = CustomerProfile.objects.get(user=self.request.user)
                customer_ins.name = self.request.data['name']
                customer_ins.phone = self.request.data['phone']
                customer_ins.email = self.request.data['email']
                customer_ins.short_address = self.request.data['short_address']
                customer_ins.save()
                if CustomerAddress.objects.filter(customer=customer_ins).exists():
                    customer_address = CustomerAddress.objects.filter(customer=customer_ins).update(
                        **self.request.data['delivery_address']
                    )
                    customer_address = CustomerAddress.objects.get(customer=customer_ins)
                else:
                    customer_address = CustomerAddress.objects.create(
                        customer=customer_ins,
                        **self.request.data['delivery_address']
                    )
            except Exception as e:
                print(e)
                raise ValidationError('You must have to logged in as a customer' + str(e))

        else:
            ordered_by = self.request.user.username
            if CustomerProfile.objects.filter(phone=self.request.data['phone']).exists():
                customer_ins = CustomerProfile.objects.get(phone=self.request.data['phone'])
                customer_ins.short_address = self.request.data['short_address']
                customer_ins.save()
            else:
                if not (self.request.data['phone'] is None or self.request.data['phone'] == ''):
                    customer_ins = CustomerProfile.objects.create(
                        phone=self.request.data['phone'],
                        name=self.request.data['name'],
                        short_address=self.request.data['short_address']
                    )
        try:
            item_count = 0
            p_codes = ''
            # order items
            for i in serializer.validated_data['order_items']:
                product_code = i['product']
                quantity = i['quantity']
                try:
                    single_product = product_code  # Product.objects.get(pk=product_code)
                except Product.DoesNotExist:
                    raise ValidationError(
                        '{} is not available'.format(product_code))

                total_price = float(single_product.discounted_price) * float(quantity)
                sub_total += total_price
                item_count = item_count + quantity
                p_codes += p_codes + ', ' + str(product_code)

            # customer_order = Order.objects.filter(customer=customer_ins)
            #
            # # cheking for incomplete order
            # check_previous_order = Order.objects.filter(
            #     (Q(status="PENDING") | Q(status="ACCEPTED") | Q(status="SHIPPING")),
            #     customer=customer_ins
            # )

            # grand total
            # grand_total = float(total_tax_value) + float(sub_total)
            grand_total = sub_total
            promo_code_instance = None
            promo_discount = 0
            try:
                promo_code = self.request.data['promo_code_value']
                print('Promocode is: ' + promo_code)
                # promo limit check
                promo_query = Order.objects.filter(
                    promo_code__code__iexact=promo_code,
                    customer=customer_ins
                ).count()
                try:
                    promo_code_instance = PromoCode.objects.get(
                        code__iexact=promo_code,  # vendor=vendor_user
                    )
                    if promo_query < promo_code_instance.limit and promo_code_instance.is_valid:
                        if promo_code_instance.discount_type == 'PERCENTAGE':
                            promo_discount = float(grand_total * float(promo_code_instance.discount) / 100)
                            grand_total = grand_total - promo_discount
                        else:
                            promo_discount = float(promo_code_instance.discount)
                            grand_total = grand_total - promo_discount
                except Exception as e:
                    print(e)
                    raise ValidationError('Invalid promo code')
                # try:
                # payment_instance = PaymentDetails.objects.create(
                #
                # )

            except Exception as e:

                promo_query = 0
            # try:
            #     pd = PaymentDetails.objects.create(
            #         payment_method=serializer.validated_data['payment_method'],
            #         payment_status=serializer.validated_data['payment_status'],
            #         amount_paid=serializer.validated_data['amount_paid'],
            #         transaction_id=serializer.validated_data['transaction_id'],
            #         is_failed=serializer.validated_data['is_failed']
            #     )
            # except Exception as e:
            #     pd = None
            other_discount = 0
            if promo_code_instance == None:
                try:
                    other_discount = float(self.request.data['other_discount'])
                except Exception as e:
                    other_discount = 0
                if other_discount > 0:
                    grand_total = grand_total - other_discount

            try:
                other_charges = float(self.request.data['other_charges'])
            except:
                other_charges = 0
            if other_charges > 0:
                grand_total = grand_total + other_charges

            dt = datetime.datetime.now()
            now = int(dt.strftime("%Y%m%d%H%M%S"))
            order_details = {
                'total_amount': grand_total,
                'tran_id': 'TRX' + str(now) + str(customer_ins.id),
                'cus_name': customer_ins.name,
                'cus_email': customer_ins.email,
                'cus_phone': customer_ins.phone,
                'cus_add1': customer_ins.short_address,
                'cus_city': customer_address.city,
                'cus_country': 'Bangladesh',
                'shipping_method': 'No',
                'num_of_item': item_count,
                'product_name': p_codes,
                'product_category': "NA"
            }
            serializer.save(
                customer=customer_ins,
                promo_code=promo_code_instance,
                order_total=grand_total,
                delivery_address=customer_address,
                promo_discount=promo_discount,
                ordered_by=ordered_by,
                item_count=item_count,
                product_list=p_codes,
            )
            messages.success(self.request, 'Your order has been placed!')
            data = json.dumps(order_details, indent=4)
            # return Response(data,status=200,template_name=None, headers=None, content_type=None)


        except Exception as e:
            return Response({
                'status': False,
                'status_code': 400,
                'detail': 'Failed to create order',
                'order_details': None
            })
        # # if customer has atleast one incomplete order
        # if customer_order.count() <= 0:
        #     serializer.save(customer=customer_ins, total_price=grand_total)
        # else:
        #     if len(check_previous_order) >= 1:
        #         raise ValidationError(
        #             'You can not order. You have an incomplete order')
        #     elif promo_query >= 3:
        #         raise ValidationError('Promo code limit exceeded')
        #     else:
        #         serializer.save(customer=customer_ins,
        #             total_price=grand_total, status="pending")


class OrderDetail(APIView):
    """
    endpoint for retriving,patching
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderUpdateSerializer

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.request.user
        is_owner = Order.objects.filter(Q(
            pk=pk, customer__user=user
        ) | Q(
            pk=pk, vendor__user=user
        ))
        if is_owner.exists() or user.is_superuser:
            instace = self.get_object(pk)
            serializer = OrderSerializer(instace)
            return Response(serializer.data)
        else:
            raise ValidationError(
                'You do not have permissions to view this item or order does not exist')

    def put(self, request, pk, format=None):
        response = {}
        user = self.request.user
        query = Order.objects.filter(
            pk=pk, vendor__user=user)
        is_completed = Order.objects.filter(
            pk=pk,
            status='DONE'
        )
        print(query.exists())
        if is_completed.exists():
            raise ValidationError('You can not update a completed order')
        elif query.exists():
            instance = self.get_object(pk)
            serializer = OrderUpdateSerializer(
                instance,
                data=request.data
            )

            if serializer.is_valid():
                response['success'] = "Order status updated successfully"
                serializer.save()

                # if order is accepted send email to customer
                if serializer.validated_data['status'] == "ACCEPTED":
                    subject = "Order accepted"
                    msg = "Your order no: {} has been accepted".format(
                        instance.id)
                    Verification().send_order_confirmation_email(
                        instance.customer.user.email,
                        subject,
                        msg
                    )
                # if order is completed send email to customer
                elif serializer.validated_data['status'] == "DONE":
                    subject = "Order completed"
                    msg = "Your order no: {} has been completed".format(
                        instance.id)
                    Verification().send_order_confirmation_email(
                        instance.customer.user.email,
                        subject,
                        msg
                    )
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError(
                'You do not have permissions to update this order')


# active order
class ActiveOrders(generics.ListAPIView):
    """
    endpoint for viewing active orders
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    # queryset = Order.objects.all()
    def get_queryset(self):
        user = self.request.user
        try:
            queryset = Order.objects.get(
                (
                        Q(status="PENDING") | Q(status="ACCEPTED")
                        | Q(status="SHIPPING")
                ),
                customer__user=user
            )
        except Order.DoesNotExist:
            queryset = None
            # raise ValidationError('Not found')
        return queryset


# previous order


class PreviousOrder(generics.RetrieveAPIView):
    """
    endpoint for users previous order
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_object(self):
        user = self.request.user
        queryset = Order.objects.filter(
            customer__user__username=user,
            status="DONE"
        ).latest('id')
        return queryset
