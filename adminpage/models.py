from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin


from django.utils.functional import cached_property

class User(models.Model):
	id = models.CharField(primary_key=True, verbose_name="아이디",max_length=200)
	user_name = models.CharField(verbose_name="이름",max_length=200)
	user_pass = models.CharField(verbose_name="비밀번호",max_length=200)
	recent_login = models.DateTimeField( verbose_name="최근 로그인", )
	updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일", )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )
	user_img_url = models.CharField(verbose_name="유저 이미지 주소",max_length=200, null=True, blank=True)
 
	friend = models.ManyToManyField("self", blank=True)
 
 
	achives = models.ManyToManyField(
        'Achivement', through='UserAchivement')
 
 
	def achivesAll(self):
		return self.achives.all()
 
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
  
  
class Address(models.Model):
	id = models.AutoField(primary_key=True)
	addr1 = models.CharField(verbose_name="주소 1",max_length=200)
	addr2 = models.CharField(verbose_name="주소 2",max_length=200)
	postcode = models.CharField(verbose_name="우편번호",max_length=200)
	updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일", )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )

	user_id = models.ForeignKey(User,  on_delete=models.CASCADE, db_column="user_id", related_name="userAddr")
 
	def __str__(self):
		return f"[{self.postcode}] {self.addr1},{self.addr2}"


	class Meta:
		managed = True
		db_table = 'address' 
		verbose_name_plural = '주소' 
  
  
class Achivement(models.Model):
	id = models.AutoField(primary_key=True)
	achiv_name = models.CharField(verbose_name="업적명",max_length=200)
 
	def __str__(self):
		return f"{self.achiv_name}"

	class Meta:
		managed = True
		db_table = 'achivement' 
		verbose_name_plural = '업적' 
  
class UserAchivement(models.Model):
	id = models.AutoField(primary_key=True)
	user_id= models.ForeignKey(User,  on_delete=models.CASCADE, db_column="user_id", related_name="userAchiv_user")
	achiv_id= models.ForeignKey(Achivement,  on_delete=models.CASCADE, db_column="achiv_id", related_name="userAchiv_achiv")
	visible_chk= models.BooleanField(default=True)
 
	def __str__(self):
		return f"{self.user_id}_{self.achiv_id}"

	class Meta:
		managed = True
		db_table = 'user_achivement' 
		verbose_name_plural = '유저-업적' 
  
  
  
class Survey(models.Model):
	id = models.AutoField(primary_key=True)
	surv_name = models.CharField(verbose_name="설문조사명",max_length=200)
	updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일", )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )
 
	def __str__(self):
		return f"{self.surv_name}"

	class Meta:
		managed = True
		db_table = 'survey' 
		verbose_name_plural = '설문조사' 
  
class SurveyQ(models.Model):
	id = models.AutoField(primary_key=True)
	surv_id= models.ForeignKey(Survey,  on_delete=models.CASCADE, db_column="surv_id", related_name="surv_survQ")
	surv_q_content= models.CharField(verbose_name="설문조사 질문",max_length=200)
	updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일", )
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )
 
 
	def __str__(self):
		return f"[{self.surv_id}]{self.surv_q_content}"

	class Meta:
		managed = True
		db_table = 'survey_q' 
		verbose_name_plural = '설문조사 질문' 
  
class SurveyA(models.Model):
	id = models.AutoField(primary_key=True)
	surv_q_id= models.ForeignKey(SurveyQ,  on_delete=models.CASCADE, db_column="surv_q_id", related_name="survQ_survA")
	user_id= models.ForeignKey(User,  on_delete=models.CASCADE, db_column="user_id", related_name="user_survA")
	surv_a_content= models.CharField(verbose_name="설문조사 응답",max_length=200)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", )
 
	def __str__(self):
		return f"[{self.surv_q_id}/{self.user_id}]{self.surv_a_content}"

	class Meta:
		managed = True
		db_table = 'survey_a' 
		verbose_name_plural = '설문조사 응답' 
  