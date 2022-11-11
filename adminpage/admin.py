from django.contrib import admin
from .models import *

from django.utils import timezone
from datetime import timedelta

from django.utils.html import mark_safe
from .baseAdmin import BaseAdmin

from django.contrib.auth.models import User as AuthUser, Group
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin,  GroupAdmin

admin.ModelAdmin.list_per_page = 20
admin_site = admin.AdminSite(name='yourwish')

class AddrInline(admin.TabularInline):
	model = Address
	readonly_fields = ('created_at', 'updated_at')
	extra = 0
	


from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class ManytoManyAdminForm(forms.ModelForm):
	AchiveList = forms.ModelMultipleChoiceField(
		queryset=Achivement.objects.all(),
		required=False,
		widget=FilteredSelectMultiple(
			verbose_name='업적',
			is_stacked=False
		),
		label='업적 리스트',
	)


	class Meta:
		model = User
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance and self.instance.pk:
			self.fields['AchiveList'].initial = self.instance.achives.all()


	def save(self, commit=True):
		obj = super().save(commit)
		initial = self.fields['AchiveList'].initial 
		diff = self.cleaned_data['AchiveList'].difference(initial).count() + initial.difference(self.cleaned_data['AchiveList']).count()
		if obj.pk and diff > 0  :
			try:
				# print("###########################\n", initial,"\n###########################\n", )
				ori_pks = list(initial.values_list('id' , flat=True))
				obj.achives.set(
					self.cleaned_data['AchiveList'], clear=True)
				# print("###########################\n", initial,"\n###########################\n", )
				self.initial['AchiveList'] = Achivement.objects.filter(pk__in=ori_pks)
			except Exception as e:
				print(e)
		return obj

class UserAdmin(BaseAdmin):
	form=ManytoManyAdminForm
	list_display = ('id', 'user_name', 'recent_login','isRecentlyLogined2')
	fields =  ('id', 
			   ('user_img_url', 'imgThumbnail'),
			   'user_name','user_pass', 
			   ('recent_login','isRecentlyLogined2'),
			   'friend',
			   'AchiveList'
			   )
	readonly_fields =  ('isRecentlyLogined2', 'imgThumbnail')
	filter_horizontal=('friend',)
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
		
from django.db.models import Count
import pandas as pd
import sqlite3
from main.settings import BASE_DIR

class SurveyQInline(admin.TabularInline):
	model = SurveyQ
	fields =  ( 'surv_q_content', 'updated_at', 'created_at', 'tableRow','tablePandasRow')
	readonly_fields = ('created_at', 'updated_at', 'tableRow','tablePandasRow')
	extra = 0
 
	@admin.display(description="전체 응답")	
	def tableRow(self, obj):
		try:
			result = """<table style='width: 100%;'>
			<thead>
				<tr>
					<th>응답</th>
					<th>응답 수</th>
				</tr>
			</thead>
			<tbody>

			"""
			string = []
	
			queryset = obj.survQ_survA.all()\
	   			.values('surv_a_content')\
			  	.annotate(total=Count('surv_a_content'))\
				.order_by('-total')
	
			for query in queryset:
				string.append("""
				<tr>
					<td>%s</td>
					<td>%s</th>
				</tr>
				"""% ( query['surv_a_content'], query['total'])) 
			
			string.append(f"""
			<tr>
				<td>모든 응답</td>
				<td>{obj.survQ_survA.all().count()}</th>
			</tr>
			""")
			string = result + ' '.join(string) + "</tbody></table>"
			return mark_safe(string)
		except Exception as e:
			print(e)
	
 
	@admin.display(description="전체 응답2")	
	def tablePandasRow(self, obj):        
		if(obj.id is None):
			return '-'

		try:
			targetColumns = ["응답", "응답 수"]
			conn  = sqlite3.connect('db.sqlite3')
			SQL_Query = pd.read_sql_query(f"""
				SELECT surv_a_content as "{targetColumns[0]}", count(surv_a_content) as "{targetColumns[1]}" 
				FROM survey_a 
				where surv_q_id={obj.id}
				group by surv_a_content 
				order by "{targetColumns[1]}" DESC;
				""", conn )
			df = pd.DataFrame(SQL_Query)
			df.loc[-1] = ['모든 응답', obj.survQ_survA.count()]
			return mark_safe("<div style='max-width:300px; max-height: 300px; overflow: auto;'> " +
							df.style.bar(
								subset=[targetColumns[1]], color='#79aec8').hide(axis="index").to_html()
							+ "</div>"
							)

		except Exception as e:
			print(e)
		
	
	
class SurveyAdmin(BaseAdmin):
	list_display = ('id', 
			   'surv_name',)
	list_display_links = ('surv_name',)
	
	fields =  ( 'surv_name', 'updated_at', 'created_at')
	readonly_fields =  ('updated_at', 'created_at')
	inlines=[SurveyQInline]
	
	
	

admin_site.register(User, UserAdmin)
admin_site.register(Address)
admin_site.register(Achivement)



# django authentication 관련 어드민
admin_site.register(AuthUser, AuthUserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Survey, SurveyAdmin)
admin_site.register(SurveyA)