from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """
    Allows access only to authenticated users as a Customer.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users as an Admin.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)


class IsVendor(BasePermission):
    """
    Allows access only to authenticated users as an Admin or Vendor.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_vendor)


class IsVendorOrAdmin(BasePermission):
    """
    Allows access only to authenticated users as an Admin or Vendor.
    """

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_admin or request.user.is_vendor))
