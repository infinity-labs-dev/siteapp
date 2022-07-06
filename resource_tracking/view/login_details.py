from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    default_error_messages = {
        'no_active_account': 'Username or Password is incorrect.'
    }
    def validate(self, attrs):
        try:
            # request = self.context["request"]
            # databody=request.data
            print(attrs)

            data = super().validate(attrs)
            groupdata=self.user.groups.all().order_by("hierarchy_level").first()
            groupname=groupdata.name
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            # Add extra responses here
            data['username'] = self.user.username
            data['first_name'] = self.user.first_name
            data['last_name'] = self.user.last_name
            data['user_id'] = self.user.id
            data['groups'] = groupname
            data['suceess']=True
            return data
        except Exception as e:
             return {"suceess":False,"details":"OS error: {0}".format(e)}






class GetLoginDetails(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

