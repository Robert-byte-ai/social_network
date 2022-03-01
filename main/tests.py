import urllib
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from main.models import Post, User, Read, Follow


def url_with_params(url, **kwargs):
    return url + '?' + urllib.parse.urlencode(kwargs)


POST_URL = reverse('posts-list')

USER_LIST_URL = reverse('user-list')

USER_LIST_ORDERED_URL = url_with_params(
    USER_LIST_URL,
    ordering='posts_count'
)

POST_LIST_FILTERED_BY_FOLLOWING_URL = url_with_params(
    POST_URL,
    follow=True
)

POST_LIST_FILTERED_BY_READ_URL = url_with_params(
    POST_URL,
    read=True
)

FOLLOW_URL = reverse('follow-list')

USERNAME = 'test_username'

USERNAME2 = 'test_username2'


class Tests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.user2 = User.objects.create_user(username=USERNAME2)
        cls.post = Post.objects.create(
            title='test_post',
            text='this is test post',
            author=cls.user2
        )
        cls.POST_READ_URL = reverse(
            'posts-read',
            kwargs={'pk': cls.post.id}
        )
        cls.DELETE_FOLLOW_URL = reverse(
            'follow-detail',
            kwargs={'pk': cls.user2.id}
        )
        cls.guest_client = APIClient()
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(user=cls.user)

    def test_list_posts(self):
        response = self.guest_client.get(POST_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_post(self):
        posts_count = Post.objects.count()
        data = {
            'text': 'test',
            'title': 'test_title'
        }
        response = self.authorized_client.post(POST_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_mark_post_read(self):
        response = self.authorized_client.post(self.POST_READ_URL)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('post'), self.post.pk)
        self.assertEqual(response.data.get('user'), self.user.pk)

    def test_list_read_posts(self):
        self.authorized_client.post(self.POST_READ_URL)
        response = self.authorized_client.get(POST_LIST_FILTERED_BY_READ_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        read_content = dict(*response.data.get('results'))
        self.assertEqual(read_content.get('author'), self.post.author.username)
        self.assertEqual(read_content.get('text'), self.post.text)
        self.assertEqual(read_content.get('title'), self.post.title)

    def test_create_follow(self):
        response1 = self.authorized_client.post(FOLLOW_URL, data={'following': self.user2.username})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response1.data.get('user'), self.user.username)
        self.assertEqual(response1.data.get('following'), self.user2.username)

    def test_list_follow(self):
        self.authorized_client.post(FOLLOW_URL, data={'following': self.user2.username})
        response2 = self.authorized_client.get(POST_LIST_FILTERED_BY_FOLLOWING_URL)
        follow_content = dict(*response2.data.get('results'))
        self.assertEqual(follow_content.get('author'), self.user2.username)
        self.assertEqual(follow_content.get('text'), self.post.text)
        self.assertEqual(follow_content.get('title'), self.post.title)

    def test_users(self):
        response1 = self.authorized_client.get(USER_LIST_URL)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.authorized_client.get(USER_LIST_ORDERED_URL)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        first_user = dict(response2.data[0])
        second_user = dict(response2.data[1])
        self.assertLess(
            get_object_or_404(
                User,
                username=first_user['username']
            ).posts.count(),
            get_object_or_404(
                User,
                username=second_user['username']
            ).posts.count()
        )

