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
        tasks = Task.objects.filter(test=self)
        return Answer.objects.filter(task__in = tasks).aggregate(models.Sum('max_score'))['max_score__sum']

    def get_score(self):
        tasks = Task.objects.filter(test=self)
        return Answer.objects.filter(task__in = tasks).aggregate(models.Sum('score'))['score__sum']
    
    def __str__(self):
        return "Test Nr. {} for: {}".format(self.t_id, self.course)

#Task is 'Reporter'
class Task(models.Model):
    RENDER_TYPES = (
        ("MC","Multiple Choice"),
        ("VT","Vocabulary Test")
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=512)
    render_type = models.CharField(max_length=2, choices=RENDER_TYPES)

#Answer is 'Article'
class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)
    checked = models.BooleanField(default = False)
    correct_answer = models.CharField(max_length=256)
    max_score = models.IntegerField()
    score = models.IntegerField(default = 0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order']