from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin
class User(models.Model):
	id = models.CharField(primary_key=True, verbose_name="아이디",max_length=200)
	user_name = models.CharField(verbose_name="이름",max_length=200)
	user_pass = models.CharField(verbose_name="비밀번호",max_length=200)
	recent_login = models.DateTimeField( verbose_name="최근 로그인", )
	updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일", )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )
 
	user_img_url = models.CharField(verbose_name="유저 이미지 주소",max_length=200, null=True, blank=True)
 
	def __str__(self):
		return f"{self.id} ({self.user_name})"

	@admin.display(
		boolean=True,
  		description="최근 로그인 여부"
	)
	def isRecentlyLogined(self):
		recent = timezone.now() - timedelta(days=10)
		return self.recent_login > recent
		
	class Meta:
		managed = True
		db_table = 'user' 
		verbose_name_plural = '유저' 