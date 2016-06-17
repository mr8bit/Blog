from django.forms import ModelForm
from .models import Comments
from captcha.fields import ReCaptchaField

class CommentForm(ModelForm):
	captcha = ReCaptchaField()
	class Meta:
		model = Comments
		fields = ['name','email','comment','anser_on']
