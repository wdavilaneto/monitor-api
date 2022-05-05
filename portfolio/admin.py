from django.contrib import admin

# Register your models here.
from .models import Board, Task, Objective, KeyResults, KeyResultValue

admin.site.register(Board)
admin.site.register(Task)
admin.site.register(Objective)
admin.site.register(KeyResults)
admin.site.register(KeyResultValue)
