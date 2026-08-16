from django import forms
from .models import Study
from django.core.exceptions import ValidationError

class StudyForm(forms.ModelForm):

    content = forms.CharField(
        error_messages={
            "required": "学習内容を入力してください。"
        }
    )

    class Meta:
        model = Study
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data["content"]

        # 前後の空白を取り除く
        content = content.strip()

        # 空白しか入力されていなかった場合
        if not content:
            raise ValidationError(
                "学習内容を入力してください。"
            )

        # 3文字以下だった場合
        if len(content) <= 3:
            raise ValidationError(
                "学習内容は4文字以上入力してください。"
            )

        return content