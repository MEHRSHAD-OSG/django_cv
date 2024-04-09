from django.contrib.auth.models import User

# for login with email:
class EmailBackend:

    def authenticate(self,request,username=None,password=None):
        # if there is no username:
        try:
            user = User.objects.get(email=username)

            # check password
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None


    def get_user(self,user_id):
        try:

            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
