from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import re
from .models import *

@api_view(['GET'])
def get_similar_questions(request, question_id):
    question = Question(element_id_property=question_id)
    question.refresh()

    similar_questions = []
    for theme in question.theme.all():
        for similar_question in theme.questions.all():
            if similar_question.element_id_property != question.element_id_property:
                if (similar_question.answers.all()):
                    similar_questions.append({
                        "title": similar_question.entitled,
                        "video": similar_question.answers.all()[0].video.all()[0].element_id_property,
                        "timecode": similar_question.answers.all()[0].timecode,
                        "artist": similar_question.answers.all()[0].artist.all()[0].name
                    })
    
    return Response(similar_questions, status=status.HTTP_200_OK)
