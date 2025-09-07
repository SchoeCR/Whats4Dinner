# Whats4Dinner
### Video demo: 
### Description: 
<ins>**Overview:**</ins>

Whats4Dinner is a web application that helps users decide what to cook for dinner based on the ingredients they have at home. Users can input their available ingredients, and the app will suggest recipes that can be made with those ingredients. 
The app also allows users to save their favorite recipes and create a shopping list for missing ingredients and create a meal plan using found recipes.

<ins>**Features:**</ins>

***

*Technologies Used:*
- Frontend: Flask, HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: SQLite
- APIs: Spoonacular API for recipe suggestions
- Authentication: Flask-Login for user authentication

***

*Data source -> Spoonacular API:* 
> Spoonacular API Documentation:
> https://spoonacular.com/food-api

Spoonacular API is a comprehensive food and recipe API that provides access to a vast database of recipes, ingredients, and nutritional information. 
It offers various endpoints for searching recipes, retrieving recipe details, and generating meal plans.

***

*User Control:*

The app provides users with the ability to register a profile, providing additional features beyond just recipe searching and suggestions.
From the profile page, users can:
- View saved recipes for easy access later.
- View and manage their shopping list, which includes ingredients needed for their chosen recipes.
- Create a meal plan by selecting recipes for specific days of the week.
- Update their profile information, such as username and password.

***

***Recipe Search and Suggestions:***

Once logged in, from the 'Home' page, users have a couple of options for 'searching' or 'querying' the API data source for suggested recipes.

The first option is using a simple keyword search, whereby entering a keyword (e.g., "chicken") into the search bar will return a list of recipes that include that keyword in their title or description. 

The returned results is by design limited to 5 random results per search. This is to keep the application performance optimal and avoid overwhelming users with too many options. To requery the search (that is, to get a new set of 5 random results), users can simply re-enter the same keyword and hit search again.

To refine the search results further, users can use the second option, which is to input a list of ingredients they want included or excluded; e.g. Include - Chicken, Carrots, Exclude - Tomato. 
The app will then return recipes that can be made using those ingredients.

Further refinements can be made by specifying any intolerances or allergens (e.g., Gluten, Nuts, Seafood), and any specific diets (e.g., Paleo, Vegetarian, Vegan).

***

***Detailed Recipe View:***

Upon selecting a recipe from the search results, users are taken to a detailed view of the recipe. This view provides the following key information:
- Recipe Title
- Image of the dish
- Preparation and cooking duration in minutes
- Dietary and allergen information (e.g. Gluten-free) if any
- List of ingredients required for the recipe including the required quantity
- Step-by-step cooking instructions
- Dietary and allergen information (e.g. Gluten-free)
- Nutritional information (including % of recommended daily amount)
- Any similar recipes that users might be interested in
- Suggested wine pairings, if any

In addition to viewing the recipe information above, users can also interact with the recipe in the following ways:


***

***Saving Favourite Recipes:***

