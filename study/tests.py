from django.test import TestCase
from .models import Study
from django.contrib.auth import get_user_model
from .forms import StudyForm
from django.urls import reverse


class StudyFormTest(TestCase):

    # 正しい学習内容を入力した場合、バリデーションを通過することを確認
    def test_valid_content(self):
        form = StudyForm(
            data={
                "content": "Pythonを勉強する"
            }
        )

        self.assertTrue(form.is_valid())


    # 短すぎる学習内容を入力した場合、バリデーションエラーになることを確認
    def test_short_content(self):
        form = StudyForm(
            data={
                "content": " a "
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


    # 空白のみの学習内容を入力した場合、バリデーションエラーになることを確認
    def test_whitespace_only_content(self):
        form = StudyForm(
            data={
                "content": "   "
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


class StudyModelTest(TestCase):

    # 各テストで使用するダミーユーザーを作成
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )


    # Studyを作成し、内容とユーザーが正しくDBに保存されることを確認（Create）
    def test_create_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.assertEqual(Study.objects.count(), 1)
        self.assertEqual(study.content, "Pythonを勉強する")
        self.assertEqual(study.user, self.user)


    # 既存Studyのcontentを変更し、DBにも更新内容が保存されることを確認（Update）
    def test_update_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        study.content = "Djangoを勉強する"
        study.save()

        study.refresh_from_db()

        self.assertEqual(study.content, "Djangoを勉強する")


    # Studyを削除した場合、DBから対象データが削除されることを確認（Delete）
    def test_delete_study(self):
        study = Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        self.assertEqual(Study.objects.count(), 1)

        study.delete()

        self.assertEqual(Study.objects.count(), 0)


    # ユーザーに紐づくStudyをDBから取得できることを確認（Read）
    def test_read_study(self):
        Study.objects.create(
            content="Pythonを勉強する",
            user=self.user
        )

        study = Study.objects.get(
            user=self.user
        )

        self.assertEqual(study.content, "Pythonを勉強する")


class StudyViewTest(TestCase):

    # 認証・Viewテストで使用するダミーユーザーを作成
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )


    # 正しいユーザー名・パスワードでログインできることを確認
    def test_login_success(self):
        logged_in = self.client.login(
            username="testuser",
            password="testpass"
        )

        self.assertTrue(logged_in)


    # 未ログイン状態でDashboardへアクセスした場合、Login画面へリダイレクトされることを確認
    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("dashboard")
        )


    # 間違ったパスワードではログインできないことを確認
    def test_login_failure(self):
        logged_in = self.client.login(
            username="testuser",
            password="testpppp"
        )

        self.assertFalse(logged_in)


    # 正しいSignup情報をPOSTした場合、新しいユーザーがDBに作成されることを確認
    def test_signup_success(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "newuser",
                "password1": "Testpass123!",
                "password2": "Testpass123!"
            }
        )

        User = get_user_model()

        new_user = User.objects.get(
            username="newuser"
        )

        self.assertEqual(User.objects.count(), 2)


    # パスワードが一致しない場合、Signupに失敗しユーザーが追加されないことを確認
    def test_signup_failure(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "newuser",
                "password1": "Testpass123!",
                "password2": "Different123!"
            }
        )

        User = get_user_model()

        self.assertEqual(User.objects.count(), 1)


    # ログアウト後は未認証状態となり、DashboardへアクセスするとLoginへ戻されることを確認
    def test_logout(self):
        self.client.login(
            username="testuser",
            password="testpass"
        )

        self.client.logout()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertRedirects(
            response,
            reverse("login") + "?next=" + reverse("dashboard")
        )


    # 次：ログインユーザーには自分のStudyだけが表示されることを確認
    # def test_dashboard_shows_only_own_studies(self):