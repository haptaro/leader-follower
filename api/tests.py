import pytest
from unittest.mock import Mock, patch
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from api.models import Note, UserMetadata
from api import services


@pytest.mark.django_db
class TestAuthenticationServices(TestCase):
    """Test cases for authentication-related services."""

    def setUp(self):
        """Set up test data."""
        self.username = "testuser"
        self.password = "testpassword123"
        self.existing_username = "existinguser"
        
        # Create an existing user for testing
        self.existing_user = User.objects.create_user(
            username=self.existing_username,
            password=self.password
        )
        UserMetadata.objects.create(user=self.existing_user)

    def test_signup_user_success(self):
        """Test successful user signup."""
        token = services.signup_user(self.username, self.password)
        
        # Check that user was created
        user = User.objects.get(username=self.username)
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.password))
        
        # Check that UserMetadata was created with token
        user_metadata = UserMetadata.objects.get(user=user)
        self.assertEqual(user_metadata.access_token, token)
        self.assertNotEqual(token, "")

    def test_signup_user_existing_username(self):
        """Test signup with existing username raises exception."""
        with self.assertRaises(Exception) as context:
            services.signup_user(self.existing_username, self.password)
        
        self.assertEqual(str(context.exception), "Username already exists")

    def test_login_user_success(self):
        """Test successful user login."""
        token = services.login_user(self.existing_username, self.password)
        
        # Check that token is returned
        self.assertIsNotNone(token)
        self.assertNotEqual(token, "")
        
        # Check that UserMetadata has the token
        user_metadata = UserMetadata.objects.get(user=self.existing_user)
        self.assertEqual(user_metadata.access_token, token)

    def test_login_user_invalid_username(self):
        """Test login with invalid username raises exception."""
        with self.assertRaises(Exception) as context:
            services.login_user("nonexistent", self.password)
        
        self.assertEqual(str(context.exception), "Invalid credentials")

    def test_login_user_invalid_password(self):
        """Test login with invalid password raises exception."""
        with self.assertRaises(Exception) as context:
            services.login_user(self.existing_username, "wrongpassword")
        
        self.assertEqual(str(context.exception), "Invalid credentials")

    def test_logout_user_success(self):
        """Test successful user logout."""
        # First login to get a token
        token = services.login_user(self.existing_username, self.password)
        self.assertNotEqual(token, "")
        
        # Then logout
        result = services.logout_user(self.existing_user)
        
        # Check result message
        self.assertEqual(result, "Logged out successfully")
        
        # Check that token was cleared
        user_metadata = UserMetadata.objects.get(user=self.existing_user)
        self.assertEqual(user_metadata.access_token, "")

    def test_logout_user_unauthenticated(self):
        """Test logout with unauthenticated user raises exception."""
        # Use AnonymousUser to simulate unauthenticated user
        unauthenticated_user = AnonymousUser()
        
        with self.assertRaises(Exception) as context:
            services.logout_user(unauthenticated_user)
        
        self.assertEqual(str(context.exception), "Authentication required")


@pytest.mark.django_db
class TestUserServices(TestCase):
    """Test cases for user-related services."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_get_authenticated_user_success(self):
        """Test getting authenticated user."""
        # The user is authenticated by default when created
        result = services.get_authenticated_user(self.user)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.user.id)
        self.assertEqual(result.username, self.user.username)

    def test_get_authenticated_user_unauthenticated(self):
        """Test getting unauthenticated user returns None."""
        # Use AnonymousUser to simulate unauthenticated user
        unauthenticated_user = AnonymousUser()
        
        result = services.get_authenticated_user(unauthenticated_user)
        
        self.assertIsNone(result)


@pytest.mark.django_db
class TestNoteServices(TestCase):
    """Test cases for note-related services."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username="user1",
            password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="password123"
        )
        
        # Create some notes for user1
        self.note1 = Note.objects.create(message="Note 1", user=self.user1)
        self.note2 = Note.objects.create(message="Note 2", user=self.user1)
        
        # Create a note for user2
        self.note3 = Note.objects.create(message="Note 3", user=self.user2)

    def test_find_my_notes_success(self):
        """Test finding notes for a user."""
        notes = services.find_my_notes(self.user1.id)
        
        # Should return 2 notes for user1
        self.assertEqual(len(notes), 2)
        
        # Should be ordered by created_at descending (newest first)
        self.assertEqual(notes[0].message, "Note 2")  # Most recent
        self.assertEqual(notes[1].message, "Note 1")  # Older
        
        # All notes should belong to user1
        for note in notes:
            self.assertEqual(note.user_id, self.user1.id)

    def test_find_my_notes_empty(self):
        """Test finding notes for user with no notes."""
        # Create a new user with no notes
        new_user = User.objects.create_user(
            username="newuser",
            password="password123"
        )
        
        notes = services.find_my_notes(new_user.id)
        
        self.assertEqual(len(notes), 0)

    def test_create_note_success(self):
        """Test creating a note for authenticated user."""
        # User created through User.objects.create_user is authenticated by default
        message = "New test note"
        note = services.create_note(self.user1, message)
        
        # Check that note was created with correct data
        self.assertIsNotNone(note)
        self.assertEqual(note.message, message)
        self.assertEqual(note.user, self.user1)
        
        # Check that note exists in database
        db_note = Note.objects.get(id=note.id)
        self.assertEqual(db_note.message, message)
        self.assertEqual(db_note.user, self.user1)

    def test_create_note_unauthenticated(self):
        """Test creating note with unauthenticated user raises exception."""
        # Use AnonymousUser to simulate unauthenticated user
        unauthenticated_user = AnonymousUser()
        
        with self.assertRaises(Exception) as context:
            services.create_note(unauthenticated_user, "Test message")
        
        self.assertEqual(str(context.exception), "Authentication required")

    def test_create_note_empty_message(self):
        """Test creating note with empty message."""
        # User created through User.objects.create_user is authenticated by default
        message = ""
        note = services.create_note(self.user1, message)
        
        # Should still create the note with empty message
        self.assertIsNotNone(note)
        self.assertEqual(note.message, message)
        self.assertEqual(note.user, self.user1)


# Additional integration tests
@pytest.mark.django_db
class TestServiceIntegration(TestCase):
    """Integration tests for services working together."""

    def test_signup_login_create_note_flow(self):
        """Test complete flow: signup -> login -> create note -> find notes."""
        username = "integrationuser"
        password = "password123"
        
        # 1. Sign up
        token1 = services.signup_user(username, password)
        user = User.objects.get(username=username)
        
        # 2. Login (should get same or new token)
        token2 = services.login_user(username, password)
        
        # 3. Create notes (user created through create_user is authenticated)
        note1 = services.create_note(user, "First note")
        note2 = services.create_note(user, "Second note")
        
        # 4. Find notes
        notes = services.find_my_notes(user.id)
        
        # Verify the flow worked correctly
        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0].message, "Second note")  # Most recent first
        self.assertEqual(notes[1].message, "First note")
        
        # 5. Logout
        result = services.logout_user(user)
        self.assertEqual(result, "Logged out successfully")
        
        # Verify token was cleared
        user_metadata = UserMetadata.objects.get(user=user)
        self.assertEqual(user_metadata.access_token, "")
