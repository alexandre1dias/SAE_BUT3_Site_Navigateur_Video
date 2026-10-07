from neomodel import (
    StructuredNode,
    StringProperty,
    DateProperty,
    UniqueIdProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredRel,
    DateTimeProperty,
    ZeroOrMore,
    BooleanProperty,
    ZeroOrOne,
    RegexProperty,
    EmailProperty,
    ZeroOrOne,
)
from datetime import date


class PositionExtraitRel(StructuredRel):
    """
    Relation Postion Extrait
    """

    position = IntegerProperty(required=True)


class DateHeureRel(StructuredRel):
    """
    Relation Date Heure
    """

    date_heure = DateTimeProperty(default_now=True)


class Artiste(StructuredNode):
    """
    Noeud Artiste
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, required=True, expression=r".+")


class Occasion(StructuredNode):
    """
    Noeud Occasion
    Pour quel occasion la playlist existe
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, required=True, expression=r".+")


class Interview(StructuredNode):
    """
    Noeud Interview
    """

    uuid = UniqueIdProperty()
    titre = RegexProperty(index=True, expression=r".+")
    date = DateProperty(index=True)
    description = StringProperty()

    occasion = RelationshipTo("Occasion", "OCCASION", ZeroOrOne)
    tags_interview = RelationshipTo("Tag", "TAGS_INTERVIEW", ZeroOrMore)


class Extrait(StructuredNode):
    """
    Noeud Extrait
    """

    uuid = UniqueIdProperty()
    titre = RegexProperty(index=True, expression=r".+")
    description = StringProperty()
    youtube_url = StringProperty()
    vimeo_url = StringProperty()
    lieu = StringProperty()
    uploaded_at = DateProperty(default=date.today())
    duree = IntegerProperty(required=True)  # Nombre de seconde

    interviewer = RelationshipTo("Artiste", "PARTICIPER", ZeroOrOne)
    interviews = RelationshipTo(
        "Interview", "APPARTIENT_A", ZeroOrMore, PositionExtraitRel
    )
    question = RelationshipTo("Question", "POSE", ZeroOrOne)
    audios = RelationshipTo("Audio", "AUDIOS", ZeroOrMore)
    tags_extrait = RelationshipTo("Tag", "TAGS_EXTRAIT", ZeroOrMore)


class Audio(StructuredNode):
    """
    Noeud Audio
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, required=True, expression=r".+")


class Question(StructuredNode):
    """
    Noeud Question
    """

    uuid = UniqueIdProperty()
    texte = RegexProperty(unique_index=True, required=True, expression=r".+")

    theme = RelationshipTo("Theme", "A_THEME", ZeroOrOne)


class Theme(StructuredNode):
    """
    Noeud Theme
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, required=True, expression=r".+")


class Utilisateur(StructuredNode):
    """
    Noeud Utilisateur
    """

    uuid = UniqueIdProperty()
    pseudo = RegexProperty(unique_index=True, required=True, expression=r".+")
    prenom = RegexProperty(required=True, expression=r".+")
    nom = RegexProperty(required=True, expression=r".+")
    email = StringProperty(required=True, unique_index=True)
    # TODO La propriété email est définie comme une StringProperty au lieu d'une EmailProperty car l'EmailProperty de neomodel a un fonctionnement particulier
    # email = EmailProperty(required=True, unique_index=True)
    password = StringProperty(required=True)
    is_admin = BooleanProperty(default=False)

    recherches_artistes = RelationshipTo(
        "Artiste", "RECHERCHES_ARTISTES", ZeroOrMore, DateHeureRel
    )
    regarder_interviews = RelationshipTo(
        "Interview", "REGARDER_INTERVIEWS", ZeroOrMore, DateHeureRel
    )
    regarder_extraits = RelationshipTo(
        "Extrait", "REGARDER_EXTRAITS", ZeroOrMore, DateHeureRel
    )
    recherches_questions = RelationshipTo(
        "Question", "RECHERCHES_QUESTIONS", ZeroOrMore, DateHeureRel
    )


class Tag(StructuredNode):
    """
    Noeud Tag
    """

    uuid = UniqueIdProperty()
    name = RegexProperty(unique_index=True, required=True, expression=r".+")


class CSVImportJob(StructuredNode):
    uuid = UniqueIdProperty()
    status = StringProperty(
        choices={v: v for v in ["pending", "success", "error", "in_progress"]},
        default="pending",
    )
    message = StringProperty(default="")
