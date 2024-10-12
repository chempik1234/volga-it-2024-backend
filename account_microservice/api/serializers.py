from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        fields = ("name",)
        model = Role

    def validate_name(self, value):
        return value

    def to_representation(self, instance):
        return instance.name

    @property
    def data(self):
        return self.fields.get("name")

    def get_default(self):
        return "name"

    def get_initial(self):
        return self.fields["name"]


class CustomUserSerializer(serializers.ModelSerializer):
    """CustomUser serializer without roles, for basic functions."""
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'username', "password")
        model = User

    def create(self, validated_data):
        """
        This creation method creates and returns only the user
        :return: created user
        """
        user = None
        with transaction.atomic():
            password = validated_data['password']  # not popping to let django use raw value
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """
        This creation method updates and returns only the user
        :return: updated user
        """
        with transaction.atomic():
            password = validated_data['password']  # not popping to let django use raw value
            instance = super().update(instance, validated_data)
            instance.set_password(password)  # paste hashed password
            instance.save()
        return instance


class CustomUserSerializerWithRoles(CustomUserSerializer):
    """CustomUser serializer with roles support, for admin functions."""
    roles = RoleSerializer(many=True)

    # def get_roles(self, obj):
    #     return obj.roles.values_list("name", flat=True)

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'username', "roles", "password")
        model = User

    def create(self, validated_data):
        """
        This creation method creates both user and roles (if needed) in 1 transaction
        :return: created user
        """
        roles = validated_data.pop("roles", [])  # roles are assigned with get_or_create + M2M role.users.add(...
        # [{name: str}, ]
        roles = [i["name"] for i in roles]

        new_user = super().create(validated_data)  # CustomUser fields remain in validated_data

        for role_name in roles:
            new_role, created = Role.objects.get_or_create(name=role_name)  # new roles have to be created
            new_user.roles.add(new_role)  # after the user is created, roles can be assigned.
        return new_user

    def update(self, instance, validated_data):
        """
        This creation updates both user and roles (if needed) in 1 transaction

        Prunes roles
        :return: updated user
        """
        roles = validated_data.pop("roles", [])  # roles are assigned with get_or_create, old ones are pruned!
        # [{name: str}, ]
        roles = [i["name"] for i in roles]

        with transaction.atomic():
            super().update(instance, validated_data)  # update the rest data

            for role_name in roles:
                new_role, created = Role.objects.get_or_create(name=role_name)  # new roles have to be created
                instance.roles.add(new_role)  # after the user is created, roles can be assigned.

            for role in instance.roles.all():  # prune roles
                if role.name not in roles:
                    instance.roles.remove(role)  # remove unused roles
                    if role.users.all().count() == 0:
                        role.delete()  # role isn't in the list and is used only here
        return instance


class SignOutSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {"details": "signed out successfully"}

    def to_internal_value(self, data):
        return {"details": "signed out successfully"}


class CustomTokenVerifySerializer(serializers.Serializer):
    """
    Custom serializer for HTTP token validation that returns {"valid": bool}
    """
    valid = serializers.BooleanField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining a pair of tokens for a user based on username and password.
    """

    def validate(self, attrs):
        """
        Override validate method to return access and refresh tokens.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
