# messaging_app/chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Conversation, Message

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ("username", "email", "role", "created_at")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (None, {"fields": ("phone_number", "role", "user_id")}),
    )
    readonly_fields = ("user_id",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "conversation", "sent_at")
    readonly_fields = ("message_id",)
