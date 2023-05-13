from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.test import APIClient
import pytest
from accounts.models import Profile
from ..models import Post, Category


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = get_user_model().objects.create_user(
        email="test@test.com", password="a/@123456", is_verified=True
    )
    return user


@pytest.fixture
def post_object(common_user):
    profile = Profile.objects.get(user=common_user)
    post = Post.objects.create(
        author=profile,
        title="test title",
        content="test content",
        status=True,
        published_date=now(),
    )
    return post


@pytest.fixture
def common_user_2():
    user = get_user_model().objects.create_user(
        email="test2@test.com", password="a/@123456", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestPostApi:
    def test_get_post_list_response_200_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_post_detail_response_200_status(self, api_client, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self, api_client):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
            "status": True,
            "published_date": now(),
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_delete_post_response_401_status(self, api_client, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})

        response = api_client.delete(url)
        assert response.status_code == 401

    def test_edit_post_response_401_status(self, api_client, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        data = {
            "title": "new test title",
            "content": "new test content",
            "status": True,
            "published_date": now(),
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 401
        data2 = {"title": "edited title"}
        response = api_client.patch(url, data=data2)
        assert response.status_code == 401

    # user is authenticated from force_authenticate called
    def test_create_post_response_201_status(self, api_client, common_user):
        url = reverse("blog:api-v1:post-list")
        category = Category.objects.create(name="cat_name")
        data = {
            "title": "test title",
            "content": "test content",
            "category": [category.id],
            "tags": ["string"],
            "status": True,
            "published_date": now(),
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Post.objects.get(title="test title")

    def test_create_post_invalid_data_response_400_status(
        self, api_client, common_user
    ):
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "test title",
            "content": "test content",
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_delete_post_response_204_status(
        self, api_client, common_user, post_object
    ):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        # api_client.login(email="test@test.com", password="a/@123456")
        api_client.force_authenticate(user=common_user)
        print(api_client.__dict__["renderer_classes"]["json"])
        print(api_client.__dict__["renderer_classes"]["multipart"])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()

    def test_edit_post_response_200_status(self, api_client, common_user, post_object):
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        # data = {
        #     "title": "new test title",
        #     "content": "new test content",
        #     "status": True,
        #     "published_date": now(),
        # }
        category = Category.objects.create(name="new_cat_name")
        data = {
            "title": "new test title",
            "content": "new test content",
            "category": [category.id],
            "tags": ["string"],
            "status": True,
            "published_date": now(),
        }
        api_client.force_authenticate(user=common_user)
        # api_client.login(email="test@test.com", password="a/@123456")
        response = api_client.put(url, data=data)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "new test title"
        data2 = {"title": "edited title"}
        response = api_client.patch(url, data=data2)
        assert response.status_code == 200
        post.refresh_from_db()
        assert post.title == "edited title"

    # user2 is authenticated from force_authenticate called
    def test_delete_post_response_403_status(
        self, api_client, common_user_2, post_object
    ):
        user2 = common_user_2
        api_client.logout()
        api_client.force_authenticate(user=user2)
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        response = api_client.delete(url)
        assert response.status_code == 403
        assert Post.objects.get(id=post.id)

    def test_edit_post_response_403_status(
        self, api_client, common_user_2, post_object
    ):
        user2 = common_user_2
        post = post_object
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": post.id})
        data = {
            "title": "new test title",
            "content": "new test content",
            "status": True,
            "published_date": now(),
        }
        # api_client.login(email="test2@test.com", password="a/@123456")
        api_client.force_authenticate(user=user2)
        response = api_client.put(url, data=data)
        assert response.status_code == 403
        data2 = {"title": "edited title"}
        response = api_client.patch(url, data=data2)
        assert response.status_code == 403
