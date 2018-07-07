#creates a quiz for debug purposes

import quiz as q
from quiz.models import Answer
from quiz.models import Test
from quiz.models import Task
t1 = Test()
t1.save()
ta1 = Task(test = t1, question = "Was macht der Teddy?")
ta1.save()
ta2 = Task(test = t1, question = "Was macht der Tiger?")
ta2.save()
a1 = Answer(task = ta1, answer = "Nichts", max_score = 95)
a1.save()
a2 = Answer(task = ta1, answer = "LOL", max_score = 5)
a2.save()
a3 = Answer(task = ta2, answer = "Den Elefefante", max_score = 6)
a3.save()