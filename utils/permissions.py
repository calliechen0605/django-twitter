from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
   To check if obg.user == request.user
    Permission 会一个一个执行：
    - if detail = False, 只查 has_permission
    - if detail = True, 查 has_permission and has_object_permission
   -  如果出错， 会display IsObjectOwner.message
   - details = false， 方法中， API中， 没有ID的， 比如list， create
    """

    message = "You do not have permission to access this object"

    def has_permission(self, request, view):
        return True

    #request --> 当前请求，
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user