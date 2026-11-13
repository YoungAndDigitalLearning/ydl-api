from rest_framework import serializers
from quiz import models as m


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Answer
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, source="answer_set", read_only=True)

    class Meta:
        model = m.Task
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, source="task_set", read_only=True)
    score = serializers.IntegerField(source="get_score", read_only=True)
    max_score = serializers.IntegerField(source="get_max_score", read_only=True)

    class Meta:
        model = m.Test
        # Include IDs for selecting a test by course instead of assuming quiz pk == course pk.
        fields = ["id", "course", "t_id", "tasks", "score", "max_score"]
