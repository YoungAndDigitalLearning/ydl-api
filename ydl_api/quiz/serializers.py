from rest_framework import serializers
from quiz import models as m

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Answer
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True, source = 'answer_set')

    def get_answers(self, task):
        return [AnswerSerializer(answer).data for answer in task.answer_set.all()]
    class Meta:
        model = m.Task
        fields = "__all__"

class TestSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, source='task_set')
    score = serializers.IntegerField(source='get_score', read_only = True)
    max_score = serializers.IntegerField(source='get_max_score', read_only = True)

    def update(self, instance, validated_data):
        tasks_data = validated_data.pop("task_set")
        super().update(instance, validated_data)
        
        tasks = instance.task_set.all()
        answers = m.Answer.objects.filter(task__in = tasks)
        for task_data, task in zip(tasks_data, tasks):
            answers_data = task_data["answer_set"]
            old_answers_objects = m.Answer.objects.filter(task = task)
            for new_answer_data, old_answer_object in zip(answers_data, old_answers_objects):
                old_answer_object.answer = new_answer_data["answer"]
                old_answer_object.checked = new_answer_data["checked"]
                old_answer_object.max_score = new_answer_data["max_score"]
                old_answer_object.score = new_answer_data["score"]
                old_answer_object.order = new_answer_data["order"]
                old_answer_object.save()

    def get_tasks(self, test):
        return [TaskSerializer(task).data for task in m.Task.objects.filter(test=test)]

    class Meta:
        model = m.Test
        fields = ["tasks","score", "max_score"]