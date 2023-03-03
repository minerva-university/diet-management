.mode column
PRAGMA foreign_keys = ON;


CREATE TABLE user( -- table for declaring different users and their properties
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    weight INTEGER NOT NULL,
    height INTEGER NOT NULL,
    age INTEGER NOT NULL,
    activity_level TEXT CHECK(activity_level IN ('sedentary', 'lightly active', 'moderately active', 'very active', 'extra active'))
);

CREATE TABLE user_calories( -- table for tracking the calories of the current user (One user -> one number of calories)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calories INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE user_history( -- dinormalized table for historical data (log)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    height INTEGER NOT NULL,
    age INTEGER NOT NULL,
    activity_level TEXT CHECK(activity_level IN ('sedentary', 'lightly active', 'moderately active', 'very active', 'extra active')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE meals( -- table for declaring different meals and their properties
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories INTEGER NOT NULL, -- per serving
    serving_size INTEGER NOT NULL, -- in grams
    recipe TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meals_photos( -- table for having specific meal photos (One meal -> many photos)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    photo BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(meal_id) REFERENCES meals(id)
);

CREATE TABLE meals_label( -- table for having specific meal labels (One meal -> many labels)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_id INTEGER NOT NULL,
    label TEXT NOT NULL, -- we should consider having ENUM for this
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(meal_id) REFERENCES meals(id)
);

CREATE TABLE user_current_diet( -- table for tracking the current user's diet (One user -> one diet)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE user_current_diet_meals( -- table for having specific diet meals (One diet -> many meals)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_current_diet_id INTEGER NOT NULL,
    meal_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_current_diet_id) REFERENCES user_current_diet(id),
    FOREIGN KEY(meal_id) REFERENCES meals(id)
);

CREATE TABLE diet_calories( -- table for tracking the calories of the current user's diet (One diet -> one calories)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_current_diet_id INTEGER NOT NULL,
    calories INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_current_diet_id) REFERENCES user_current_diet(id)
);

