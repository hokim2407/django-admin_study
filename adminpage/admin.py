from django.contrib import admin
from .models import User, Address

admin.ModelAdmin.list_per_page = 20
admin_site = admin.AdminSite(name='yourwish')

from django.utils import timezone
from datetime import timedelta

from django.utils.html import mark_safe
from .baseAdmin import BaseAdmin




class AddrInline(admin.TabularInline):
    model = Address
    readonly_fields = ('created_at', 'updated_at')
    extra = 0
    

class UserAdmin(BaseAdmin):
    list_display = ('id', 'user_name', 'recent_login','isRecentlyLogined2')
    fields =  ('id', 
               ('user_img_url', 'imgThumbnail'),
               'user_name','user_pass', 
               ('recent_login','isRecentlyLogined2'))
    readonly_fields =  ('isRecentlyLogined2', 'imgThumbnail')
    inlines=[AddrInline]

    @admin.display(
		boolean=True,
  		description="최근 로그인 여부"
	)
    def isRecentlyLogined2(self, obj):
        try:
            recent = timezone.now() - timedelta(days=10)
            return obj.recent_login > recent
        except Exception as e:
            return False
    
    @admin.display(
  		description="이미지 미리보기"
	)
    def imgThumbnail(self,obj):
        return mark_safe(f"""
                         <img src='{obj.user_img_url}' id='previewImg'/>
                         <button type='button' id='previewBtn'> 이미지 미리보기</button>
                         """)
        
    def changelist_view(self, request, extra_context=None):
        if(extra_context is None):
            extra_context = {}
        extra_context.update({'buttons':[
            {'name':'네이버', 'url':'https://www.naver.com/'},
            {'name':'구글','url':'https://www.google.com/'},
        ]})
        return super().changelist_view(request, extra_context)
        
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if(extra_context is None):
            extra_context = {}
        extra_context.update({'buttons':[
            {'name':'알럿 메세지', 'script':'alert("Hello")'},
            {'name':'콘솔 메세지','script':'console.log("World")'},
        ]})
        return super().changeform_view(request, object_id, form_url, extra_context)
        
    class Media:
        js = ( '/static/js/imgPreview.js', )
        css = {'all': ('/static/css/custom.css', )}
		

admin_site.register(User, UserAdmin)
admin_site.register(Address)