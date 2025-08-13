import unittest

from Whats4Dinner.service import save_new_favourite
from Whats4Dinner.utils import db_delete, db_select

class TestService(unittest.TestCase):

    def test_save_favourite_returns_error_message_when_no_user_id_provided(self):
        
        # Arrange
        user_id = 1
        recipe_id = 1
        recipe_name = "Spicy chicken"
        recipe_summary = "Super spicy chicken that will knock your socks off!"
        recipe_image_url = "https://google.com/image.png"

        # Act 
        error_message = save_new_favourite("", recipe_id, recipe_name, recipe_summary, recipe_image_url)

        # Assert
        self.assertEqual(error_message, "Invalid user")

    def test_save_favourite_returns_error_message_when_no_recipe_name_provided(self):
        
        # Arrange
        user_id = 1
        recipe_id = 1
        recipe_name = "Spicy chicken"
        recipe_summary = "Super spicy chicken that will knock your socks off!"
        recipe_image_url = "https://google.com/image.png"

        # Act 
        error_message = save_new_favourite(user_id, recipe_id, "", recipe_summary, recipe_image_url)

        # Assert
        self.assertEqual(error_message, "Invalid recipe")

    def test_save_new_favourite(self):
        
        # I wouldn't normally write unit tests against the db, but this is my first one as I refactor.

        # Arrange
        user_id = 99
        recipe_id = 1
        recipe_name = "Spicy chicken"
        recipe_summary = "Super spicy chicken that will knock your socks off!"
        recipe_image_url = "https://google.com/image.png"

        # Act 
        error_message = save_new_favourite(user_id, recipe_id, recipe_name, recipe_summary, recipe_image_url)

        # Assert
        db_result = db_select("favourite_Recipes", where={"user_id":user_id})
        self.assertIsNotNone(db_result)
        self.assertEqual(db_result[0]["user_id"], user_id)
        self.assertEqual(db_result[0]["recipe_id"], recipe_id)
        self.assertEqual(db_result[0]["recipe_name"], recipe_name)
        self.assertEqual(db_result[0]["recipe_summary"], recipe_summary)
        self.assertEqual(db_result[0]["recipe_image"], recipe_image_url)
        
        db_delete("favourite_Recipes", where={"user_id":user_id})

if __name__ == '__main__':
    unittest.main()