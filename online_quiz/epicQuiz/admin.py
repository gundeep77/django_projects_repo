from django.contrib import admin
from .models import ComputerQuiz, UserTestData
from .models import ScienceQuiz
from .models import GKQuiz


admin.site.register(ComputerQuiz)
admin.site.register(ScienceQuiz)
admin.site.register(GKQuiz)
admin.site.register(UserTestData)