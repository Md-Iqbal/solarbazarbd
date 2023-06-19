from rest_framework.exceptions import ValidationError
from customer_profile_api.models import CustomerProfile


class SectionOwner:
    # def is_owner(self, user):
    #     try:
    #         vendor = Vendor.objects.get(user=user)
    #     except Vendor.DoesNotExist:
    #         raise ValidationError('This access is only for admin')
    #     return vendor

    def is_customer(self, user):
        try:
            customer = CustomerProfile.objects.get(user=user)
        except CustomerProfile.DoesNotExist:
            raise ValidationError('Only customer can access this')
        return customer
