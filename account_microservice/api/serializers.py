from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from account_microservice.api.models import Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        lookup_field = "name"
        model = Role


class CustomUserSerializer(serializers.ModelSerializer):
    """CustomUser serializer without roles, for basic functions."""
    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'username',)
        model = User

    def create(self, validated_data):
        """
        This creation method creates and returns only the user
        :return: created user
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hashed password
        user.save()  # no need for transaction
        return user


class CustomUserSerializerWithRoles(CustomUserSerializer):
    """CustomUser serializer with roles support, for admin functions."""
    roles = RoleSerializer(many=True, required=False)  # TODO: check how roles work
    # serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ('id', 'firstName', 'lastName', 'username', "roles",)
        model = User

    def create(self, validated_data):
        """
        This creation method creates both user and roles (if needed) in 1 transaction
        :return: created user
        """
        roles = validated_data.pop("roles", [])  # roles are assigned with get_or_create + M2M role.users.add(...

        new_user = super().create(validated_data)  # CustomUser fields remain in validated_data

        for role_name in roles:
            new_role, created = Role.objects.get_or_create(name=role_name)  # new roles have to be created
            new_user.roles.add(new_role)  # after the user is created, roles can be assigned.
        return new_user

    def update(self, instance, validated_data):
        """
        This creation updates both user and roles (if needed) in 1 transaction
        :return: updated user
        """
        roles = validated_data.pop("roles", [])  # roles are assigned with get_or_create, old ones are pruned!

        with transaction.atomic():
            super().update(instance, validated_data)  # update the rest data

            for role_name in roles:
                new_role, created = Role.objects.get_or_create(name=role_name)  # new roles have to be created
                instance.roles.add(new_role)  # after the user is created, roles can be assigned.

            for role in instance.roles.all():  # prune roles
                if role.name not in roles and role.users.all().count() == 1:
                    role.delete()  # role isn't in the list and is used only here
        return instance

