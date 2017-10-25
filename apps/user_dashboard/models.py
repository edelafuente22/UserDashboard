# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must enter a valid email address."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Name field must be at least two characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Name field must be at least two characters."
        if len(postData['password']) < 8 or len(postData['confirm']) < 8:
            errors['password_length'] = "Password must be 8 or more characters."
        if postData['password'] != postData['confirm']:
            errors['password_match'] = "Passwords must match."
        return errors

    def validate_login(self, postData):
        errors = {}
        user_check = User.objects.filter(email = postData['email'])
        if len(user_check) > 0:
            user_check = user_check[0]
            if not bcrypt.checkpw(postData['password'].encode(), user_check.password.encode()):
                errors['error'] = "Email/password combination is invalid."
                return errors
        else:
            errors['error'] = "Email/password combination is invalid."
            return errors

class User(models.Model):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class MessageManager(models.Manager):
    def validate_message(self, postData):
        errors = {}
        if len(postData['message_content']) < 1:
            errors['new_message'] = "Message field must not be left blank."
            return errors
        # else:
        #     message = Message.objects.create(content=postData['message_content'], sender=User.objects.get(id = sender_id, receiver=User.objects.get(id = receiver_id)))

class Message(models.Model):
    content = models.TextField(null=True)
    sender = models.ForeignKey(User, related_name="messages_sent")
    receiver = models.ForeignKey(User, related_name="messages_received")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()

# To get all messages SENT by user w/ ID=1:
# userOne = Person.objects.get(id=1)
# userOne.messages_sent.all()

class Comment(models.Model):
    content = models.CharField(max_length=255)
    message = models.ForeignKey(Message, related_name="comments")
    commenter = models.ForeignKey(User, related_name="comments_sent")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)