from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from ai.models import Conversation
from django.urls import reverse

User = get_user_model()


class ConversationViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username="testuser", password="testpassword", email="test@test.com"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_conversation(self):
        url = reverse("conversation-list")
        response = self.client.post(url, {"title": "My Chat"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(Conversation.objects.first().title, "My Chat")

    def test_list_conversations(self):
        Conversation.objects.create(user=self.user, title="Chat 1")
        url = reverse("conversation-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_conversation(self):
        convo = Conversation.objects.create(user=self.user, title="Chat 1")

        url = reverse("conversation-detail", args=[convo.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Chat 1")

    def test_delete_conversation(self):
        convo = Conversation.objects.create(user=self.user, title="Chat 1")

        url = reverse("conversation-detail", args=[convo.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_user_cannot_see_others_conversations(self):
        other_user = User.objects.create_user(username="other", password="pass")
        Conversation.objects.create(user=other_user, title="Secret Chat")

        url = reverse("conversation-list")
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
