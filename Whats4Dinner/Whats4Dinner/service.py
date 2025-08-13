from Whats4Dinner.utils import db_select, db_insert

def save_new_favourite(user_id, recipe_id, recipe_name, recipe_summary, recipe_image_url) :
    
    error_message = ""

    # Validate inputs
    if not user_id:
        error_message = "Invalid user"
    if not recipe_id or not recipe_name:
        error_message = "Invalid recipe"

    if not error_message:
    
        # Save to Database
        try:

            # Check to see if it's already favourited. 
            existing_favourite_id = db_select("favourite_Recipes","favourite_id",where={"user_id":user_id,"recipe_id":recipe_id})

            if not existing_favourite_id:
                db_insert("favourite_Recipes",insertvalues={"user_id":user_id, "recipe_id":recipe_id, "recipe_name":recipe_name, "recipe_summary":recipe_summary, "recipe_image":recipe_image_url})
            else:
                error_message = "You've already favourited this recipe. ;)"
                
        except Exception as e:
            error_message = str(e)
    
    return error_message