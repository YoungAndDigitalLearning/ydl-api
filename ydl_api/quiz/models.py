from django.db import models
from django.db.models import Q


# Create your models here.
class Test(models.Model):
    #DEBUG: blank=True
    course = models.ForeignKey('api.Course', blank=True, null=True, on_delete=models.CASCADE)
    t_id = models.IntegerField(default=1)
    #not sure if this is correct, maybe this results in unwanted behavior (user is deleted)
    scored_by = models.ForeignKey('api.User', blank=True, null=True, on_delete=models.CASCADE)

    def get_max_score(self):
        #dynamically compose OR query filter
        q_objects = Q()
        tasks = Task.objects.filter(test=self)
        for task in tasks:
            q_objects.add(Q(task=task), Q.OR)

        return Answer.objects.filter(q_objects).aggregate(models.Sum('max_score'))

    def get_score(self):
        #to be implemented @Rene
        pass
    
    def __str__(self):
        return "Test Nr. {} for: {}".format(self.t_id, self.course)

#Task is 'Reporter'
class Task(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=512)

#Answer is 'Article'
class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)
    max_score = models.IntegerField()
    score = models.IntegerField(default = 0)