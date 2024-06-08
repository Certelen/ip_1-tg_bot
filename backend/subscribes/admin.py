from django.contrib import admin

from .models import Channel, FAQ


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass
