import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.repositories.users_repository import get_user_by_login, register

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        # Setup test data
        self.test_user_data = {
            "login": "test_user",
            "name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123"
        }
        
    def test_user_registration(self):
        # Check if test_user exists and delete if necessary
        existing_user = get_user_by_login("test_user")
        if existing_user:
            from src.repositories.users_repository import delete_user
            delete_user("test_user")
            
        # Test registration
        result = register(self.test_user_data)
        self.assertTrue(result, "User registration should succeed")
        
        # Verify user was created
        user = get_user_by_login("test_user")
        self.assertIsNotNone(user, "User should be found after registration")
        self.assertEqual(user["login"], "test_user", "Login should match")
        self.assertEqual(user["name"], "Test", "Name should match")
        
        # Cleanup
        from src.repositories.users_repository import delete_user
        delete_user("test_user")

if __name__ == '__main__':
    unittest.main()
