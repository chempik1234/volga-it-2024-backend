from rest_framework import serializers
from django.db import transaction

from .models import Hospital, Room
from .authenticator import CustomSimpleJWTScheme


class RoomSerializer(serializers.ModelSerializer):
    """
    Simple Room serializer needed for list[str] display in HospitalSerializer
    """
    class Meta:
        model = Room
        fields = ("name",)
        lookup_field = "name"

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


class HospitalSerializer(serializers.ModelSerializer):
    """
    Hospital serializer with rooms (no need for extension, as I did with users)
    """
    contactPhone = serializers.CharField(source="contact_phone")
    rooms = RoomSerializer(many=True, required=False)

    class Meta:
        model = Hospital
        fields = ("id", "name", "address", "contactPhone", "rooms")
        lookup_field = "id"

    def create(self, validated_data):
        """
        This creation creates both hospital and rooms (if needed) in 1 transaction
        :return: created hospital
        """
        room_names = validated_data.pop('rooms', [])  # rooms are popped from validated_data to not bother the super()

        with transaction.atomic():  # this big hospital & rooms creation operation must be atomic!
            new_hospital = super().create(validated_data)  # let the rest framework handle hospital creation
            for room_name in room_names:  # create the unique rooms (with repeating names, maybe, that's OK!)
                new_room = Room()
                new_room.hospital = new_hospital
                new_room.name = room_name
                new_room.save()

        return new_hospital

    def update(self, instance, validated_data):
        """
        This creation updates both hospital and rooms (if needed) in 1 transaction
        :return: updated hospital
        """
        room_names = validated_data.pop('rooms', [])  # rooms are popped from validated_data to not bother the super()
        # [{"name": name}, ..]
        room_names = [i["name"] for i in room_names]  # [name, ...]

        with transaction.atomic():  # this big hospital & rooms creation operation must be atomic!
            instance = super().update(instance, validated_data)  # let the rest framework handle hospital creation
            for room_name in room_names:  # create the unique rooms (with repeating names, maybe, that's OK!)
                Room.objects.get_or_create(name=room_name, hospital=instance)

            for room in instance.rooms.all():  # prune rooms!
                if room.name not in room_names:  # role isn't listed
                    room.delete()

        return instance



