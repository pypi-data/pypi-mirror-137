from django_socio_grpc import generics
from django_socio_grpc.decorators import grpc_action
from fakeapp.serializers import BasicServiceSerializer


class BasicService(generics.GenericService):
    @grpc_action(
        request=[{"name": "user_name", "type": "string"}],
        response=BasicServiceSerializer,
    )
    async def FetchDataForUser(self, request, context):
        # INFO - AM - 14/01/2022 - Do something here as filter user with the user name
        print(request.user_name)

        user_data = {
            "email": "fake_email@email.com",
            "birth_date": "25/01/1996",
            "slogan": "Do it better",
        }

        serializer = BasicServiceSerializer(
            {"user_name": request.user_name, "user_data": user_data}
        )
        return serializer.message

    @grpc_action(
        request=[],
        response="google.protobuf.Empty",
    )
    async def TestEmptyMethod(self, request, context):
        print("TestEmptyMethod")

    @grpc_action(request=[], response=BasicServiceSerializer, use_response_list=True)
    async def GetMultiple(self, request, context):
        # INFO - AM - 14/01/2022 - Do something here as filter user with the user name
        print(request.user_name)

        user_datas = [
            {
                "user_name": "fake",
                "user_data": {
                    "email": "fake_email@email.com",
                    "birth_date": "25/01/1996",
                    "slogan": "Do it better",
                },
            },
            {
                "user_name": "fake2",
                "user_data": {
                    "email": "fake_email2@email.com",
                    "birth_date": "25/01/1996",
                    "slogan": "Do it better2",
                },
            },
        ]

        serializer = BasicServiceSerializer(user_datas, many=True)
        return serializer.message
