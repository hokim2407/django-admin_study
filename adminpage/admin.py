from django.contrib import admin
from .models import User

admin.ModelAdmin.list_per_page = 20
admin_site = admin.AdminSite(name='yourwish')

from django.utils import timezone
from datetime import timedelta

from django.utils.html import mark_safe

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'recent_login','isRecentlyLogined2')
    fields =  ('id', 
               ('user_img_url', 'imgThumbnail'),
               'user_name','user_pass', 
               ('recent_login','isRecentlyLogined2'))
    readonly_fields =  ('isRecentlyLogined2', 'imgThumbnail')

    @admin.display(
		boolean=True,
  		description="최근 로그인 여부"
	)
    def isRecentlyLogined2(self, obj):
        recent = timezone.now() - timedelta(days=10)
        return obj.recent_login > recent
    
    @admin.display(
  		description="이미지 미리보기"
	)
    def imgThumbnail(self,obj):
        return mark_safe(f"""
                         <img src='{obj.user_img_url}' id='previewImg'/>
                         <button type='button' id='previewBtn'> 이미지 미리보기</button>
                         """)
    class Media:
        js = ( '/static/js/imgPreview.js', )
        css = {'all': ('/static/css/custom.css', )}
		

admin_site.register(User, UserAdmin)