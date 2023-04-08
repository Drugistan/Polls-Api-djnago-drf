from rest_framework import serializers
from .models import Choice



class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)



class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()
    was_published_recently = serializers.BooleanField(read_only=True)


    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)


class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)
    votes = serializers.IntegerField(read_only=True)
