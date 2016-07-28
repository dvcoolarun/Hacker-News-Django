from django.contrib import admin
from .models import Link, Vote
# Register your models here.


class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)


class VoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vote, LinkAdmin)
