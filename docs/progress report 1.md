# Rasoi (Progress Report 1)

<img src='../web/public/icon-512.png' width="64">

_A social media for recipes 🍳._

[Logo Source](https://www.flaticon.com/free-icon/frying-pan_1222796?term=frying+pan&related_id=1222796)

> NOTE: all of the specifications given below are not finalized, may change if required.

## Features

- Recommended recipes (based on a recommendation engine / most popular rating wise).
- Search for recipes through dish name / ingredients list.
- Show recipe image (if possible), ratings.
- Comments, reactions (like, share).
- Posts (like Recipe images).

## Future Prospects

- We will try to detect the ingredient name from ingredient's image, if possible.
- A mobile app, possibly in [Flutter](https://flutter.dev/), [React Native](https://reactnative.dev/) or even Kotlin (native android).
- Add a post or video tutorial about the recipe.

## Technologies

### Backend

- We will develop a REST API.
- A python based backend (so that it will be easier to integrate ML features later).
- We are using [FastAPI](https://fastapi.tiangolo.com/), it has lot of features, fast and super simple to implement. Later we may move to [Flask](https://flask.palletsprojects.com/en/3.0.x/), if we face any major issue.
- [Uvicorn](https://www.uvicorn.org/) and [nginx](https://nginx.org/en/) for production deployment.
- A [postgresql](https://www.postgresql.org/) database.

### ML / Dataset

- There are multiple datasets for recipes, with their own pros and cons:
  - [The one we are using, but need to scrape ratings, has no images 🙁.](https://www.kaggle.com/datasets/paultimothymooney/recipenlg/data)
  - [Very detailed dataset, but ingredients need to be cleaned.](https://eightportions.com/datasets/Recipes/)
  - [Detailed interactions, but no ingredients list.](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv)
- This [medium article](https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b) might be helpful later, for extracting ingredients.

### Frontend

- A social media website like instagram, X (twitter) is often used daily, for them a mobile app can be a better option. Our website will be used less frequently (similar to sites like StackOverflow), thus website is a better fit for frontend.
- Following the trend, we are using [NextJs](https://nextjs.org/) and [Tailwind](https://tailwindcss.com/) for styling. Both of them have massive advantages over traditional web frameworks.
- We are not using complex styles / components, because we have future plans to develop an app, possibly in [React Native](https://reactnative.dev/). React Native is a bit fragile, so the compromise.

## Applications

- Cooking.
- Learning / Education.
- Social interaction.
