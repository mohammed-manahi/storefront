from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Custom serializer for base djoser serializer for creating a user.
    All default serializers are available at:
    https://djoser.readthedocs.io/en/latest/settings.html?highlight=serializer#serializers
    """

    class Meta(BaseUserCreateSerializer.Meta):
        # Inherit the meta class of the default base class to add customized fields (first name and last name)
        fields = ["id", "username", "password", "email", "first_name", "last_name"]
