from rest_framework import serializers
from quiz import models as m

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Answer
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, task):
        return [AnswerSerializer(answer).data for answer in task.answer_set.all()]
    class Meta:
        model = m.Task
        fields = "__all__"

class TestSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()
    score = serializers.IntegerField(source='get_score', read_only = True)
    max_score = serializers.IntegerField(source='get_max_score', read_only = True)

    def get_tasks(self, test):
        return [TaskSerializer(task).data for task in m.Task.objects.filter(test=test)]

    class Meta:
        model = m.Test
        fields = "__all__"
