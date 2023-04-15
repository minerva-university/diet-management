from . import db
from models import Meals, MealsLabel

# Your models here (Meals, MealsPhotos, MealsLabel)

def add_meal(name, calories, serving_size, recipe, labels):
    meal = Meals(name=name, calories=calories, serving_size=serving_size, recipe=recipe)
    db.session.add(meal)
    db.session.flush()

    for label in labels:
        meal_label = MealsLabel(meal_id=meal.id, label=label)
        db.session.add(meal_label)

    db.session.commit()

meals_data = [
    # Breakfast meals
    {
        'name': 'Oatmeal',
        'calories': 300,
        'serving_size': 1,
        'recipe': '1 cup of rolled oats, 2 cups of water, pinch of salt, toppings',
        'labels': ['breakfast']
    },
    {
        'name': 'Scrambled eggs',
        'calories': 350,
        'serving_size': 1,
        'recipe': '2 eggs, 1 tablespoon butter, salt and pepper, 1/4 cup shredded cheese',
        'labels': ['breakfast']
    },
    # ... Add 18 more breakfast meals here
    {
        'name': 'Banana pancakes',
        'calories': 400,
        'serving_size': 3,
        'recipe': '1 ripe banana, 2 eggs, 1/4 cup of milk, 1 cup of flour, 1 tsp of baking powder, salt, butter for frying',
        'labels': ['breakfast']
    },
    {
        'name': 'French toast',
        'calories': 350,
        'serving_size': 2,
        'recipe': '4 slices of bread, 2 eggs, 1/4 cup milk, 1 tsp vanilla extract, 1 tsp cinnamon, butter for frying, syrup for serving',
        'labels': ['breakfast']
    },
    {
        'name': 'Yogurt parfait',
        'calories': 250,
        'serving_size': 1,
        'recipe': '1 cup yogurt, 1/2 cup granola, 1/2 cup mixed berries, honey for drizzling',
        'labels': ['breakfast']
    },
    {
        'name': 'Bagel with cream cheese',
        'calories': 300,
        'serving_size': 1,
        'recipe': '1 bagel, 2 tbsp cream cheese, optional toppings (sliced cucumber, tomato, smoked salmon)',
        'labels': ['breakfast']
    },
    {
        'name': 'Breakfast burrito',
        'calories': 450,
        'serving_size': 1,
        'recipe': '1 tortilla, 2 eggs, 1/4 cup shredded cheese, 1/4 cup black beans, 1/4 cup salsa, 1 tbsp sour cream',
        'labels': ['breakfast']
    },
    {
        'name': 'Avocado toast',
        'calories': 320,
        'serving_size': 1,
        'recipe': '1 slice of bread, 1/2 avocado, salt and pepper, red pepper flakes, optional toppings (poached egg, sliced radish)',
        'labels': ['breakfast']
    },
    {
        'name': 'Granola with milk',
        'calories': 350,
        'serving_size': 1,
        'recipe': '1 cup granola, 1/2 cup milk, optional toppings (sliced banana, honey)',
        'labels': ['breakfast']
    },
    {
        'name': 'Fruit smoothie',
        'calories': 200,
        'serving_size': 1,
        'recipe': '1 banana, 1/2 cup mixed berries, 1/2 cup yogurt, 1/2 cup milk, 1 tbsp honey',
        'labels': ['breakfast']
    },
    {
        'name': 'Belgian waffle',
        'calories': 400,
        'serving_size': 1,
        'recipe': '1 cup flour, 1 tsp baking powder, 1 tbsp sugar, 1 egg, 3/4 cup milk, 2 tbsp melted butter, toppings (syrup, whipped cream, fruit)',
        'labels': ['breakfast']
    },
    {
        'name': 'Quiche Lorraine',
        'calories': 450,
        'serving_size': 1,
        'recipe': '1 pie crust, 4 eggs, 1 cup heavy cream, 1 cup diced ham, 1 cup shredded cheese, salt and pepper, pinch of nutmeg',
        'labels': ['breakfast']
    },
    {
        'name': 'Breakfast sandwich',
        'calories': 420,
        'serving_size': 1,
        'recipe': '1 English muffin, 1 fried egg, 1 slice of ham, 1 slice of cheese, optional toppings (lettuce, tomato)',
        'labels': ['breakfast']
    },
    {
        'name': 'Blueberry muffins',
        'calories': 250,
        'serving_size': 1,
    'recipe': '1 cup flour, 1/2 cup sugar, 1 tsp baking powder, 1/4 tsp salt, 1/4 cup milk, 1/4 cup melted butter, 1 egg, 1 tsp vanilla extract, 3/4 cup blueberries',
    'labels': ['breakfast']
    },
    {
    'name': 'Pancakes',
    'calories': 370,
    'serving_size': 3,
    'recipe': '1 cup flour, 1 tbsp sugar, 1 tsp baking powder, 1/2 tsp baking soda, 1/4 tsp salt, 3/4 cup milk, 1 egg, 2 tbsp melted butter, toppings (syrup, butter)',
    'labels': ['breakfast']
    },
    {
    'name': 'Breakfast casserole',
    'calories': 420,
    'serving_size': 1,
    'recipe': '4 eggs, 1/2 cup milk, 2 cups frozen hash browns, 1 cup shredded cheese, 1/2 cup diced ham, 1/4 cup diced bell pepper, 1/4 cup diced onion, salt and pepper',
    'labels': ['breakfast']
    },
    {
    'name': 'Porridge',
    'calories': 250,
    'serving_size': 1,
    'recipe': '1/2 cup oats, 1 cup water or milk, pinch of salt, optional toppings (sliced fruit, honey, cinnamon)',
    'labels': ['breakfast']
    },
    {
    'name': 'Eggs Benedict',
    'calories': 450,
    'serving_size': 1,
    'recipe': '2 English muffins, 4 poached eggs, 4 slices of ham, Hollandaise sauce (butter, egg yolks, lemon juice), fresh parsley for garnish',
    'labels': ['breakfast']
    },
    {
    'name': 'Breakfast quesadilla',
    'calories': 400,
    'serving_size': 1,
    'recipe': '1 tortilla, 2 eggs, 1/4 cup shredded cheese, 2 tbsp diced bell pepper, 2 tbsp diced onion, salt and pepper, salsa for serving',
    'labels': ['breakfast']
    },
    {
    'name': 'Smoothie bowl',
    'calories': 300,
    'serving_size': 1,
    'recipe': '1 frozen banana, 1/2 cup frozen berries, 1/2 cup yogurt, 1/4 cup milk, toppings (granola, sliced fruit, nuts, seeds, honey)',
    'labels': ['breakfast']
    },
    {
    'name': 'Veggie omelette',
    'calories': 350,
    'serving_size': 1,
    'recipe': '3 eggs, 1 tbsp butter, 1/4 cup diced bell pepper, 1/4 cup diced tomato, 1/4 cup diced onion, 1/4 cup shredded cheese, salt and pepper, fresh parsley for garnish',
    'labels': ['breakfast']
    },
    {
    'name': 'Crepes',
    'calories': 280,
    'serving_size': 2,
    'recipe': '1 cup flour, 1 cup milk, 1 egg, 1 tbsp melted butter, pinch of salt, toppings (Nutella, sliced fruit, whipped cream, powdered sugar)',
    'labels': ['breakfast']
    },


    # Lunch meals
    {
        'name': 'Grilled chicken salad',
        'calories': 450,
        'serving_size': 1,
        'recipe': '2 cups mixed greens, 4 oz grilled chicken, 1/4 cup cherry tomatoes, 1/4 cup cucumber, 2 tbsp salad dressing',
        'labels': ['lunch']
    },
    {
        'name': 'Turkey sandwich',
        'calories': 350,
        'serving_size': 1,
        'recipe': '2 slices of bread, 4 oz turkey breast, lettuce, tomato, 1 tbsp mayo, salt and pepper',
        'labels': ['lunch']
    },
    # ... Add 18 more lunch meals here
    {
        'name': 'Tuna salad wrap',
        'calories': 380,
        'serving_size': 1,
        'recipe': '1 can of tuna, 2 tbsp mayo, 1/4 cup chopped celery, 1/4 cup chopped onion, salt and pepper, 1 large tortilla',
        'labels': ['lunch']
    },
    {
    'name': 'Veggie burger',
    'calories': 400,
    'serving_size': 1,
    'recipe': '1 veggie burger patty, 1 whole wheat bun, lettuce, tomato, onion, pickles, 1 tbsp ketchup, 1 tbsp mustard',
    'labels': ['lunch']
    },
    {
        'name': 'Quinoa salad',
        'calories': 370,
        'serving_size': 1,
        'recipe': '1 cup cooked quinoa, 1/2 cup diced cucumber, 1/2 cup diced bell pepper, 1/4 cup chopped olives, 1 tbsp olive oil, 1 tbsp lemon juice, salt and pepper',
        'labels': ['lunch']
    },
    {
        'name': 'Caprese salad',
        'calories': 300,
        'serving_size': 1,
        'recipe': '2 cups fresh spinach, 1 sliced tomato, 4 oz fresh mozzarella, 1 tbsp balsamic glaze, 1 tbsp olive oil, salt and pepper',
        'labels': ['lunch']
    },
    {
        'name': 'BLT sandwich',
        'calories': 420,
        'serving_size': 1,
        'recipe': '2 slices of bread, 4 slices of bacon, lettuce, tomato, 1 tbsp mayo, salt and pepper',
        'labels': ['lunch']
    },
    {
        'name': 'Chicken Caesar wrap',
        'calories': 490,
        'serving_size': 1,
        'recipe': '1 large tortilla, 4 oz grilled chicken, 1 cup chopped romaine lettuce, 1/4 cup grated parmesan cheese, 2 tbsp Caesar dressing',
        'labels': ['lunch']
    },
    {
        'name': 'Greek salad',
        'calories': 320,
        'serving_size': 1,
        'recipe': '2 cups mixed greens, 1/4 cup feta cheese, 1/4 cup olives, 1/4 cup sliced cucumber, 1/4 cup cherry tomatoes, 2 tbsp Greek dressing',
        'labels': ['lunch']
    },
    {
        'name': 'Egg salad sandwich',
        'calories': 360,
        'serving_size': 1,
        'recipe': '2 slices of bread, 2 boiled eggs (chopped), 1 tbsp mayo, 1 tsp mustard, salt and pepper, lettuce',
        'labels': ['lunch']
    },
    {
        'name': 'Grilled cheese sandwich',
        'calories': 410,
        'serving_size': 1,
        'recipe': '2 slices of bread, 2 slices of cheddar cheese, 1 tbsp butter, tomato (optional)',
        'labels': ['lunch']
    },
    {
        'name': 'Cobb salad',
        'calories': 500,
        'serving_size': 1,
        'recipe': '2 cups mixed greens, 4 oz grilled chicken, 1 boiled egg (sliced), 1/4 cup diced avocado, 1/4 cup crumbled bacon, 1/4 cup blue cheese, 2 tbsp ranch dressing',
        'labels': ['lunch']
    },
    {
        'name': 'Pasta salad',
        'calories': 380,
        'serving_size': 1,
        'recipe': '1 cup cooked pasta, 1/4 cup cherry tomatoes, 1/4 cup diced cucumber, 1/4 cup chopped bell pepper, 1/4 cup sliced black olives, 2 tbsp Italian dressing, salt and pepper',
    'labels': ['lunch']
    },
    {
    'name': 'Sushi roll',
    'calories': 320,
    'serving_size': 1,
    'recipe': '1 nori sheet, 1/2 cup sushi rice, 4 slices of cucumber, 2 slices of avocado, 2 oz cooked shrimp, soy sauce and wasabi for dipping',
    'labels': ['lunch']
    },
    {
    'name': 'Chicken noodle soup',
    'calories': 280,
    'serving_size': 1,
    'recipe': '1 cup chicken broth, 1/2 cup cooked chicken, 1/2 cup cooked egg noodles, 1/4 cup diced carrots, 1/4 cup diced celery, salt and pepper, parsley for garnish',
    'labels': ['lunch']
    },
    {
    'name': 'Ham and cheese sandwich',
    'calories': 330,
    'serving_size': 1,
    'recipe': '2 slices of bread, 4 oz ham, 1 slice of Swiss cheese, lettuce, tomato, 1 tbsp mayo, 1 tsp mustard',
    'labels': ['lunch']
    },
    {
    'name': 'Taco salad',
    'calories': 470,
    'serving_size': 1,
    'recipe': '2 cups shredded lettuce, 4 oz cooked ground beef, 1/4 cup shredded cheese, 1/4 cup diced tomatoes, 1/4 cup black beans, 1/4 cup tortilla chips, 2 tbsp sour cream, 2 tbsp salsa',
    'labels': ['lunch']
    },
    {
    'name': 'Tomato soup with grilled cheese croutons',
    'calories': 410,
    'serving_size': 1,
    'recipe': '1 cup tomato soup, 2 slices of bread, 1 slice of cheddar cheese, 1 tbsp butter (for grilled cheese), cut grilled cheese into small squares for croutons',
    'labels': ['lunch']
    },
    {
    'name': 'Chicken and rice bowl',
    'calories': 420,
    'serving_size': 1,
    'recipe': '1 cup cooked rice, 4 oz grilled chicken, 1/4 cup steamed broccoli, 1/4 cup sliced carrots, 2 tbsp teriyaki sauce, sesame seeds for garnish',
    'labels': ['lunch']
    },
    {
    'name': 'Roast beef sandwich',
    'calories': 390,
    'serving_size': 1,
    'recipe': '2 slices of bread, 4 oz roast beef, 1 slice of provolone cheese, lettuce, tomato, 1 tbsp horseradish sauce',
    'labels': ['lunch']
    },
    {
    'name': 'Bean and cheese burrito',
    'calories': 450,
    'serving_size': 1,
    'recipe': '1 large tortilla, 1/2 cup refried beans, 1/4 cup shredded cheese, 1/4 cup diced tomatoes, 2 tbsp sour cream, 2 tbsp salsa',
    'labels': ['lunch']
    },
    # Dinner meals
    {
        'name': 'Spaghetti Bolognese',
        'calories': 500,
        'serving_size': 1,
        'recipe': '8 oz ground beef, 1/2 cup chopped onion, 1/2 cup chopped carrot, 1/2 cup chopped celery, 1 cup tomato sauce, 8 oz spaghetti',
        'labels': ['dinner']
    },
    {
        'name': 'Grilled salmon',
        'calories': 550,
        'serving_size': 1,
        'recipe': '6 oz salmon fillet, 1 tbsp olive oil, salt and pepper, 1 cup steamed broccoli, 1/2 cup cooked quinoa',
        'labels': ['dinner']
    },
    # ... Add 18 more dinner meals here
    {
        'name': 'Chicken stir-fry',
        'calories': 450,
        'serving_size': 1,
        'recipe': '6 oz chicken breast, 1 tbsp vegetable oil, 1/2 cup sliced bell pepper, 1/2 cup sliced onion, 1/2 cup sliced zucchini, 2 tbsp soy sauce',
        'labels': ['dinner']
    },
    {
        'name': 'Tofu stir-fry',
        'calories': 480,
        'serving_size': 1,
        'recipe': '6 oz tofu, 1 tbsp vegetable oil, 1/2 cup sliced bell pepper, 1/2 cup sliced onion, 1/2 cup sliced zucchini, 2 tbsp soy sauce',
        'labels': ['dinner']
    },
    {
    'name': 'Beef Stroganoff',
    'calories': 580,
    'serving_size': 1,
    'recipe': '8 oz beef sirloin, 1/2 cup chopped onion, 1 cup sliced mushrooms, 1/2 cup beef broth, 1/2 cup sour cream, 1/2 cup cooked egg noodles',
    'labels': ['dinner']
    },
    {
        'name': 'Chicken Alfredo',
        'calories': 620,
        'serving_size': 1,
        'recipe': '6 oz chicken breast, 1/2 cup heavy cream, 1/4 cup grated Parmesan, 1 tbsp butter, 1/2 cup cooked fettuccine',
        'labels': ['dinner']
    },
    {
        'name': 'Lemon Garlic Tilapia',
        'calories': 420,
        'serving_size': 1,
        'recipe': '6 oz tilapia fillet, 1 tbsp olive oil, 1 clove garlic, juice of 1 lemon, salt and pepper, 1 cup steamed asparagus',
        'labels': ['dinner']
    },
    {
        'name': 'Vegetable Curry',
        'calories': 350,
        'serving_size': 1,
        'recipe': '1/2 cup chopped potato, 1/2 cup chopped carrot, 1/2 cup peas, 1/4 cup coconut milk, 1 tbsp curry powder, 1/2 cup cooked rice',
        'labels': ['dinner']
    },
    {
        'name': 'Pork Chop with Apples',
        'calories': 510,
        'serving_size': 1,
        'recipe': '6 oz pork chop, 1 tbsp olive oil, 1/2 cup sliced apples, 1 tbsp brown sugar, 1/2 cup cooked green beans',
        'labels': ['dinner']
    },
    {
        'name': 'Chicken Marsala',
        'calories': 540,
        'serving_size': 1,
        'recipe': '6 oz chicken breast, 1/2 cup sliced mushrooms, 1/4 cup Marsala wine, 1 tbsp butter, 1/2 cup cooked linguine',
        'labels': ['dinner']
    },
    {
        'name': 'Shrimp Scampi',
        'calories': 460,
        'serving_size': 1,
        'recipe': '6 oz shrimp, 1 tbsp olive oil, 2 cloves garlic, 1/4 cup white wine, 1 tbsp lemon juice, 1/2 cup cooked spaghetti',
        'labels': ['dinner']
    },
    {
        'name': 'Chicken Parmesan',
        'calories': 660,
        'serving_size': 1,
        'recipe': '6 oz breaded chicken breast, 1/2 cup marinara sauce, 1/4 cup shredded mozzarella, 1 tbsp grated Parmesan, 1/2 cup cooked penne',
        'labels': ['dinner']
    },
    {
        'name': 'Black Bean Tacos',
        'calories': 380,
        'serving_size': 1,
        'recipe': '1/2 cup black beans, 1/2 cup chopped tomatoes, 1/4 cup shredded lettuce, 1/4 cup shredded cheese, 2 small tortillas',
        'labels': ['dinner']
    },
    {    'name': 'Beef and Broccoli',
        'calories': 460,
        'serving_size': 1,
        'recipe': '6 oz beef slices, 1 cup broccoli florets, 1 tbsp oyster sauce, 1 tbsp soy sauce, 1 tbsp cornstarch, 1/2 cup cooked jasmine rice',
        'labels': ['dinner']
    },
    {
        'name': 'Stuffed Bell Peppers',
        'calories': 420,
        'serving_size': 1,
        'recipe': '2 bell peppers, 4 oz ground beef, 1/4 cup cooked rice, 1/4 cup diced tomatoes, 1/4 cup shredded cheese, 1/4 cup marinara sauce',
        'labels': ['dinner']
    },
    {
        'name': 'Baked Ziti',
        'calories': 550,
        'serving_size': 1,
        'recipe': '1 cup cooked ziti pasta, 1/2 cup marinara sauce, 1/4 cup ricotta cheese, 1/4 cup shredded mozzarella, 1 tbsp grated Parmesan, 1/4 cup ground beef',
        'labels': ['dinner']
    },
    {
        'name': 'Chicken Quesadilla',
        'calories': 510,
        'serving_size': 1,
        'recipe': '6 oz cooked chicken, 1/2 cup shredded cheese, 1/2 cup diced tomatoes, 1/4 cup diced onions, 2 large tortillas, 1 tbsp sour cream',
        'labels': ['dinner']
    },
    {
        'name': 'Sweet and Sour Pork',
        'calories': 560,
        'serving_size': 1,
        'recipe': '6 oz pork cubes, 1/2 cup pineapple chunks, 1/2 cup bell pepper slices, 1/4 cup sweet and sour sauce, 1/2 cup cooked jasmine rice',
        'labels': ['dinner']
    },
    {
        'name': 'Eggplant Parmesan',
        'calories': 470,
        'serving_size': 1,
        'recipe': '1 medium eggplant, 1/2 cup marinara sauce, 1/4 cup shredded mozzarella, 1 tbsp grated Parmesan, 1/2 cup cooked spaghetti',
        'labels': ['dinner']
    },
    {
        'name': 'Beef Tacos',
        'calories': 480,
        'serving_size': 1,
        'recipe': '4 oz ground beef, 1/2 cup diced tomatoes, 1/4 cup shredded lettuce, 1/4 cup shredded cheese, 2 small tortillas',
        'labels': ['dinner']
    },
    {
        'name': 'Spinach and Ricotta Stuffed Shells',
        'calories': 440,
        'serving_size': 1,
        'recipe': '4 jumbo pasta shells, 1/2 cup ricotta cheese, 1/2 cup chopped spinach, 1/4 cup marinara sauce, 1/4 cup shredded mozzarella',
        'labels': ['dinner']
    },
    {
        'name': 'Lentil Soup',
        'calories': 350,
        'serving_size': 1,
        'recipe': '1/2 cup lentils, 1/2 cup diced carrots, 1/2 cup diced celery, 1/2 cup diced tomatoes, 2 cups vegetable broth, 1 tbsp olive oil',
        'labels': ['dinner']
    },
    {
        'name': 'Chicken Caesar Salad',
        'calories': 410,
        'serving_size': 1,
        'recipe': '6 oz grilled chicken, 2 cups romaine lettuce, 1/4 cup croutons, 1/4 cup Caesar dressing, 1 tbsp grated Parmesan',
        'labels': ['dinner']
    },
    {
        'name': 'Pesto Pasta',
        'calories': 480,
        'serving_size': 1,
        'recipe': '1 cup cooked penne pasta, 1/4 cup pesto sauce, 1/4 cup cherry tomatoes, 1/4 cup diced mozzarella, 1 tbsp pine nuts',
        'labels': ['dinner']
    },
    {
        'name': 'BBQ Chicken Pizza',
        'calories': 550,
        'serving_size': 1,
        'recipe': '1 small pizza crust, 1/4 cup BBQ sauce, 4 oz cooked chicken, 1/4 cup diced red onion, 1/4 cup shredded cheese, 1 tbsp chopped cilantro',
        'labels': ['dinner']
    },
    {
        'name': 'Goulash',
        'calories': 510,
        'serving_size': 1,
        'recipe': '6 oz beef cubes, 1/2 cup diced onions, 1/2 cup diced bell peppers, 1/2 cup diced tomatoes, 1 cup beef broth, 1 tbsp paprika',
        'labels': ['dinner']
    },
    {
        'name': 'Vegetarian Chili',
        'calories': 390,
        'serving_size': 1,
        'recipe': '1/2 cup black beans, 1/2 cup kidney beans, 1/2 cup diced tomatoes, 1/2 cup corn, 1/2 cup vegetable broth, 1 tbsp chili powder',
        'labels': ['dinner']
    },
    {
        'name': 'Chicken Curry',
        'calories': 460,
        'serving_size': 1,
        'recipe': '6 oz chicken breast, 1/2 cup diced onions, 1/2 cup diced tomatoes, 1/4 cup coconut milk, 1 tbsp curry powder, 1/2 cup cooked basmati rice',
        'labels': ['dinner']
    },
    {
        'name': 'Seafood Paella',
        'calories': 600,
        'serving_size': 1,
        'recipe': '4 oz shrimp, 2 oz mussels, 2 oz squid, 1/2 cup diced tomatoes, 1/2 cup diced bell peppers, 1 cup cooked paella rice, 1/4 tsp saffron',
        'labels': ['dinner']
    },
    {
        'name': 'Beef Burritos',
        'calories': 520,
        'serving_size': 1,
        'recipe': '4 oz ground beef, 1/2 cup cooked rice, 1/4 cup black beans, 1/4 cup shredded cheese, 1/4 cup diced tomatoes, 2 large tortillas',
        'labels': ['dinner']
    },
    {
    'name': 'Spinach and Feta Stuffed Chicken Breast',
    'calories': 350,
    'serving_size': 1,
    'recipe': '1 boneless, skinless chicken breast, 1/4 cup chopped spinach, 1/4 cup crumbled feta cheese, 1 tbsp olive oil, salt and pepper to taste',
    'labels': ['dinner']
    },
    {
    'name': 'Shrimp and Avocado Salad',
    'calories': 300,
    'serving_size': 1,
    'recipe': '1 cup cooked shrimp, 1/2 avocado, 1 cup mixed greens, 1/2 cup cherry tomatoes, 1 tbsp olive oil, 1 tbsp lemon juice, salt and pepper to taste',
    'labels': ['lunch']
    },
    {
    'name': 'Vegetable Omelette',
    'calories': 200,
    'serving_size': 1,
    'recipe': '2 eggs, 1/4 cup diced bell pepper, 1/4 cup diced onion, 1/4 cup chopped spinach, 1/4 cup shredded cheese, 1 tsp olive oil, salt and pepper to taste',
    'labels': ['breakfast']
    },
    {
    'name': 'Loaded Nachos',
    'calories': 650,
    'serving_size': 1,
    'recipe': '1 cup tortilla chips, 1/2 cup shredded cheese, 1/4 cup black beans, 1/4 cup diced tomatoes, 1/4 cup sliced jalapenos, 1/4 cup sour cream, 1/4 cup guacamole',
    'labels': ['lunch']
    },
    {
    'name': 'Pancakes with Bacon and Maple Syrup',
    'calories': 600,
    'serving_size': 2,
    'recipe': '1 cup flour, 1 cup milk, 1 egg, 1 tbsp melted butter, pinch of salt, 4 slices of bacon, 2 tbsp maple syrup',
    'labels': ['breakfast']
    },
    {
    'name': 'Chicken Alfredo Pasta',
    'calories': 700,
    'serving_size': 1,
    'recipe': '8 oz cooked pasta, 1/2 cup alfredo sauce, 1/2 cup cooked chicken breast, 1/4 cup grated parmesan cheese, 1 tbsp chopped parsley',
    'labels': ['dinner']
    },
    {
    'name': 'Quinoa Salad with Grilled Vegetables',
    'calories': 350,
    'serving_size': 1,
    'recipe': '1/2 cup cooked quinoa, 1/2 cup grilled vegetables (zucchini, bell peppers, red onions), 1/4 cup chickpeas, 1/4 cup crumbled feta cheese, 2 tbsp lemon juice, 1 tbsp olive oil, salt and pepper to taste',
    'labels': ['lunch']
    },
    {
    'name': 'Baked Salmon with Asparagus',
    'calories': 400,
    'serving_size': 1,
    'recipe': '1 salmon fillet, 1/2 bunch asparagus, 1 tbsp olive oil, 1 tbsp lemon juice, 1 tsp minced garlic, salt and pepper to taste',
    'labels': ['dinner']
    },
    {
    'name': 'Smoothie Bowl',
    'calories': 350,
    'serving_size': 1,
    'recipe': '1 cup frozen mixed berries, 1/2 banana, 1/2 cup almond milk, 1/2 cup Greek yogurt, toppings (granola, nuts, seeds, sliced fruit)',
    'labels': ['breakfast']
    },
    {
    'name': 'Chicken Caesar Wrap',
    'calories': 550,
    'serving_size': 1,
    'recipe': '1 large tortilla, 1/2 cup cooked chicken breast, 1 cup chopped romaine lettuce, 1/4 cup Caesar dressing, 1/4 cup grated parmesan cheese',
    'labels': ['lunch']
    },
    {
    'name': 'French Toast',
    'calories': 450,
    'serving_size': 2,
    'recipe': '2 slices of bread, 2 eggs, 1/4 cup milk, 1 tsp vanilla extract, 1 tsp cinnamon, 1 tbsp butter, toppings (maple syrup, powdered sugar, sliced fruit)',
    'labels': ['breakfast']
    },
    {
    'name': 'Vegetable Stir Fry with Tofu',
    'calories': 400,
    'serving_size': 1,
    'recipe': '1/2 cup diced tofu, 1 cup mixed vegetables (broccoli, bell peppers, carrots, snap peas), 1/2 cup cooked rice, 2 tbsp soy sauce, 1 tbsp sesame oil, 1 tsp minced garlic, 1 tsp grated ginger',
    'labels': ['dinner']
    },
]


if __name__ == '__main__':
    db.create_all()

    for meal_data in meals_data:
        add_meal(meal_data['name'], meal_data['calories'], meal_data['serving_size'], meal_data['recipe'], meal_data['labels'])
