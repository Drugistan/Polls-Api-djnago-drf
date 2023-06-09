from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import  ChoiceSerializer, VoteSerializer, QuestionResultPageSerializer, QuestionListPageSerializer, QuestionDetailPageSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import * 
# Create your views here.



@api_view(['GET', 'POST'])
def questions_view(request):
    if request.method == 'GET':
        instance = Question.objects.all()
        serializer = QuestionListPageSerializer(instance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question= serializer.data['question']
            pub_date = serializer.data['pub_date']
            Question.objects.create(question=question, pub_date=pub_date)
            return Response({"response" : serializer.data, "message" : "Question Created Succssfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.method == "GET":
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data = request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
        choice.votes +=1
        choice.save()
        return Response({"response" : "vote for this choice {}".format(choice.choice_text)})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def question_result_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)