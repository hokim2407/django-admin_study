from django.contrib import admin
class BaseAdmin(admin.ModelAdmin):
	def getLogMessage(self, form, add=False, formsetObj=None):
    	# form.changed_data에는 값이 변경된 필드의 리스트가 들어있다
		changed_data = {} if form is None else form.changed_data
		data = {}
		change_message = []
  
		# 인라인 추가시 상세 정보 입력
		if formsetObj is not None:
			data = {'name': str(formsetObj._meta.verbose_name_plural),
					'object': f"{str(formsetObj)}({formsetObj.pk})", }

		if add:
        	# 추가된 경우에는 별도 내용 없이 added 만 넣는다.
			change_message.append({'added': data})
		elif form.changed_data:
        	# 변경된 경우 message 배열 안에 변경사항을 쌓는다.
            
			message = []
			# 값이 변경된 필드를 모두 확인한다.
			for field in changed_data:
    			# 최초값은 form.initial에 dict 형식으로 들어있다.
				initial = form.initial[field]
                
    			# 수정값은 form.cleaned_data에 dict 형식으로 들어있다.
				cleaned_data = form.cleaned_data[field]
                
                # field는 model에 선언된 변수명이므로 
                # vervose name으로 출력하기 위해 form.fields[field].label 로 뽑는다.
                # [필드명] "기존값" => "새값"
				message.append(
					f"""[{form.fields[field].label}] "{str(initial)}" => "{str(cleaned_data)}" """)
			data['fields'] = message
			change_message.append({'changed': data})
		return change_message
	
	def construct_change_message(self, request, form, formsets, add=False):
		# 기본 폼 메세지 구성
		change_message = self.getLogMessage(form, add)
  
		# 폼셋들이 존재할 경우
		if formsets:
			# 각 폼셋에 대해
			for formset in formsets:
				# pk를 key로, form을 value로 가지는 dict 구성
				formList = {}
                
                #formset으로부터 pk 필드 이름 가져오기
				pkName = ''
				if formset.__len__() > 0:
					pkName = formset.forms[0]._meta.model._meta.pk.name
                    
                # formset이 가진 각 form을 순회
				for singleform in formset.forms:
					try:
                    	# form의 pk는 해당 pk의 인스턴스임
						obj = singleform.cleaned_data[pkName]
                        
                    	# 변경되지 않은 경우 cleaned_data에 값이 없으므로 최초값을 확인
						if(obj is None):
							obj = singleform.initial.get(pkName)
                            
                        # obj가 존재하면 formList에 obj에서 pkName에 해당하는 값을 찾아 key로,
                        # form을 value로 저장
						if(obj is not None):
							formList[getattr(obj, pkName)] = singleform
					except Exception as e:
						print(e)

				# 신규 생성 된 인스턴스 순회
				for added_object in formset.new_objects:
					message = self.getLogMessage(
						None, True, formsetObj=added_object)
					change_message += message
     
				# 변경된 인스턴스 순회
				for changed_object, changed_fields in formset.changed_objects:
                	# pk로 폼 찾기
					singleForm = formList[changed_object.pk]
					message = self.getLogMessage(
						singleForm, False, formsetObj=changed_object)
					change_message += message
					
                    # 현재 인스턴스가 아니라 해당 인라인 인스턴스의 히스토리에도 변경내용 기록
					self.log_change(request, changed_object,
									self.getLogMessage(singleForm, False))
                # 삭제된 인스턴스 순회
				for deleted_object in formset.deleted_objects:
					change_message.append({
						'deleted': {
							'name': str(deleted_object._meta.verbose_name_plural),
							'object': str(deleted_object),
						}
					})

		return change_message