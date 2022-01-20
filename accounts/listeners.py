
def user_changed(sender, instance, **kwargs):
    # import 写在函数里面避免循环依赖
    from accounts.services import UserService
    UserService.invalidate_user(instance.id)

def user_profile_changed(sender, instance, **kwargs):
    # import 写在函数里面避免循环依赖
    from accounts.services import UserService
    UserService.invalidate_user_profile(instance.id)