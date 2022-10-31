from django.contrib import admin
from .models import User
# Register your models here.

admin.ModelAdmin.list_per_page = 20
admin_site = admin.AdminSite(name='yourwish')

from django.utils import timezone
from datetime import timedelta

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'recent_login','isRecentlyLogined2')
    fields =  ('id', 'user_name','user_pass', ('recent_login','isRecentlyLogined2'))
    readonly_fields =  ('isRecentlyLogined2', )

    @admin.display(
		boolean=True,
  		description="최근 로그인 여부"
	)
    def isRecentlyLogined2(self, obj):
        recent = timezone.now() - timedelta(days=10)
        return obj.recent_login > recent
		

admin_site.register(User, UserAdmin)