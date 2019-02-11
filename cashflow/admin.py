from django.contrib import admin

from .models import Account, Category, Institution, Statement, Transaction

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Statement)
admin.site.register(Transaction)
