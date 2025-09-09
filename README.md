# Whats4Dinner
#### Video Demo: https://youtu.be/tPYAudRxH-A
#### Description: 
<ins>**Overview:**</ins>

Whats4Dinner is a web application that helps users decide what to cook for dinner based on the ingredients they have at home. Users can input their available ingredients, and the app will suggest recipes that can be made with those ingredients. 
The app also allows users to save their favorite recipes and create a shopping list for missing ingredients and create a meal plan using found recipes.

***

<ins>**Technologies/languages Used:**</ins>

- Frontend: Flask, HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: SQLite
- APIs: Spoonacular API for recipe suggestions
- Authentication: Flask-Login for user authentication

***

<ins>**Data source -> Spoonacular API:**</ins> 
> Spoonacular API Documentation:
> https://spoonacular.com/food-api

Spoonacular API is a comprehensive food and recipe API that provides access to a vast database of recipes, ingredients, and nutritional information. 
It offers various endpoints for searching recipes, retrieving recipe details, and generating meal plans.

***

<ins>**User Control:**</ins>

The app provides users with the ability to register a profile, providing additional features beyond just recipe searching and suggestions.
From the profile page, users can:
- View saved recipes for easy access later.
- View and manage their shopping list, which includes ingredients needed for their chosen recipes.
- Create a meal plan by selecting recipes for specific days of the week.
- Update their profile information, such as username and password.

***

<ins>**Recipe Search and Suggestions:**</ins>

Once logged in, from the 'Home' page, users have a couple of options for 'searching' or 'querying' the API data source for suggested recipes.

The first option is using a simple keyword search, whereby entering a keyword (e.g., "chicken") into the search bar will return a list of recipes that include that keyword in their title or description. 

The returned results is by design limited to 5 random results per search. This is to keep the application performance optimal and avoid overwhelming users with too many options. To requery the search (that is, to get a new set of 5 random results), users can simply re-enter the same keyword and hit search again.

To refine the search results further, users can use the second option, which is to input a list of ingredients they want included or excluded; e.g. Include - Chicken, Carrots, Exclude - Tomato. 
The app will then return recipes that can be made using those ingredients.

Further refinements can be made by specifying any intolerances or allergens (e.g., Gluten, Nuts, Seafood), and any specific diets (e.g., Paleo, Vegetarian, Vegan).

***

<ins>**Detailed Recipe View:**</ins>

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
- Add recipe to favourites
- Add ingredients to shopping list
- Add recipe to meal plan

***

<ins>**Saving Favourite Recipes:**</ins>

Should a user find a recipe they particularly like and wish to save it for future reference, they can do so by clicking the "Add to favourites" button on the detailed recipe view page.
This action saves the recipe to the user's profile, allowing them to easily access it later from their profile page.

>*When designing the project, the concious decision was made to go against data normalisation conventions and store information (other than just the unique identification number)* 
*regarding the recipe (e.g. Recipe name, Image, description) in the project database.<br> The justification for this decision was due to the limitations of available daily credit in the free API plan.*<br>
*By storing this information in the project database, it reduces the number of API calls required to retrieve recipe information, thus conserving the daily credit limit.*<br>

***

<ins>**Shopping List:**</ins>

When viewing a recipe on the detail page, users have the option to add the ingredients required for that recipe to their shopping list. 
<br>Each ingredient has a shopping cart icon associated with it and when clicked, the application will provide feedback to the user; whether successful or not.<br>

The shopping list is accessible from the user's profile page, where users can view all the ingredients they have added from various recipes. Should multiple of the same igredient
be added from different recipes, the application will automatically consolidate them into a single entry with the total quantity required.<br>
Shopping list items can be individually removed from the shopping list by pressing the &#128465; symbol.
<br><br>
>*As per the saving recipes section, the decision was made to oppose data normalisation convention by storing ingredient information when adding ingredients to the shopping list for the purpose of*
*preserving available daily API credit*
***

<ins>**Meal Planning:**</ins>

From the detailed recipe view page, users can press the "Add to plan" button to add the recipe to their meal plan.
Upon clicking the button, a modal dialog appears, prompting the user to select a day of the week to which they want to add the recipe.
Upon selecting a day, the app will provide feedback to the user, indicating whether the addition was successful or not.
<br><br>
The users meal plan is accessible from their profile page. By default the page loads to display the current week (as per their system date) from Sunday to Monday.
Using the date input, the page will reload and display any recipes that were planned for that particular date.
<br><br>From the meal plan, the user has the option to either remove a recipe by pressing the &#128465; symbol, or view the recipe
detail page by pressing the &#128269; symbol.
<br><br>
>*As per the saving recipes section, the decision was made to oppose data normalisation convention by storing ingredient information when adding ingredients to the shopping list for the purpose of*
*preserving available daily API credit*

***

<ins>**User Profile Control:**</ins>

From the profile page, the user can view basic account information such as their username and email address.
They also have the option to update their password by clicking the "Change Password" button.
The user is then redirected to a separate page where to make the change they must enter their existing password, enter a new one, and then confirm the
change by re-entering the new password. <br><br>
Upon submission, the app will provide feedback to the user, indicating whether the password change was successful or not.
