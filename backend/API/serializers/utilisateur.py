from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ..models import Utilisateur
from . import BaseSerializer


class UtilisateurSerializer(BaseSerializer):
    """
    Sérializer du node Utilisateur

    Champs aditionnels :
        - pseudo : pseudo de l'utilisateur (obligatoire)
        - prenom : prénom de l'utilisateur (obligatoire)
        - nom : nom de l'utilisateur (obligatoire)
        - email : email de l'utilisateur (obligatoire)
        - password : mot de passe de l'utilisateur (obligatoire, write_only)
        Relations :
            - recherches_artistes : les artistes recherchés par l'utilisateur
            - regarder_interviews : les interviews regardées par l'utilisateur
            - regarder_extraits : les extraits regardés par l'utilisateur
            - recherches_questions : les questions recherchées par l'utilisateur
        Champs en read_only :
            - is_admin : indique si l'utilisateur est un administrateur
    """

    pseudo = serializers.CharField(required=True)
    prenom = serializers.CharField(required=True)
    nom = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    is_admin = serializers.BooleanField(read_only=True)

    # Outputs
    recherches_artistes = serializers.SerializerMethodField(read_only=True)
    regarder_interviews = serializers.SerializerMethodField(read_only=True)
    regarder_extraits = serializers.SerializerMethodField(read_only=True)
    recherches_questions = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        """
        node : Utilisateur
        """
        super().__init__(Utilisateur, *args, **kwargs)

    def get_recherches_artistes(self, utilisateur):
        """
        Renvoie un lien propre vers les artistes :
        """
        return self.get_url(
            "artiste-list", kwargs={"utilisateur_uuid": utilisateur.uuid}
        )

    def get_regarder_interviews(self, utilisateur):
        """
        Renvoie un lien propre vers les interviews :
        """
        return self.get_url(
            "interview-list", kwargs={"utilisateur_uuid": utilisateur.uuid}
        )

    def get_regarder_extraits(self, utilisateur):
        """
        Renvoie un lien propre vers les extraits :
        """
        return self.get_url(
            "extrait-list", kwargs={"utilisateur_uuid": utilisateur.uuid}
        )

    def get_recherches_questions(self, utilisateur):
        """
        Renvoie un lien propre vers les questions :
        """
        return self.get_url(
            "question-list", kwargs={"utilisateur_uuid": utilisateur.uuid}
        )

    def create(self, validated_data):
        """
        Création d'un utilisateur
        """
        # hash password
        validated_data["password"] = make_password(validated_data.pop("password"))
        return super().create(validated_data)

    def update(self, utilisateur, validated_data):
        """
        Modification d'un utilisateur
        """
        # hash password
        pwd = validated_data.pop("password", None)
        if pwd:
            validated_data["password"] = make_password(pwd)
        return super().update(utilisateur, validated_data)
