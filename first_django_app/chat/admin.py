from django.contrib import admin
from .models import Message
from .models import Chat

class MessageAdmin(admin.ModelAdmin):    
    fields = ('chat','text','created_at', 'author', 'receiver')    # Für Detailansicht
    list_display = ('created_at', 'author', 'text', 'receiver')    # Für Überssichtsseite 
    search_fields = ('text',) # Für Suche in Übersichtsseite
    
# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)