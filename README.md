# Rasoi

<img src='web/public/icon-512.png' width="64">

_A social media for recipes 🍳._

[Logo Source](https://www.flaticon.com/free-icon/frying-pan_1222796?term=frying+pan&related_id=1222796)

# **[Live demo](https://rasoi-devs.github.io/demo)**

> Note: all of the specifications given below are not finalized, may change if required.

> Note: running and setting up backend is complex, follow the `README.md` inside [`backend/`](backend/README.md).

## Folder Structure

- backend: fastapi backend server, ml stuff and database seeding code.
- docs: documentations like diagrams, progress report etc.
- frontend: NextJs and Tailwind, Mobile app using React Native
- res: random generated resources from web like icons, fonts etc (to be used in app and web both).
- web: web only frontend code.

## Features

- Registration (Users can create accounts.They can log in to their account using emails and passwords).
- Recommended recipes (based on a recommendation engine / most popular rating wise/user profile's engagement).
- Search for recipes through dish name / ingredients list / image of recipe.
- Show recipe image, ratings and similar / related recipes.
- Rating ,Comments.
- Posts (like Recipe images).

## Future Prospects

- We will try to detect the ingredient name from ingredient's image, if possible.
- A mobile app, possibly in [Flutter](https://flutter.dev/), [React Native](https://reactnative.dev/) or even Kotlin (native android).
- Adding related video tutorials in recipe details page, expert authored posts and blogs.
- Reporting vulgar and offensive comments
- Scalable image search solutions.
- Better recommendation system.

## Technologies

### Backend

- We developed a REST API. Templating (like PHP pages or JSP) isn’t a good option if we are planning for a mobile app. Also, a REST API in the backend with an interactive UI in the frontend gives better UX.
- A python based backend (so that it will be easier to integrate ML features later).
- We are using [FastAPI](https://fastapi.tiangolo.com/), it has lot of features, fast and super simple to implement.
- [Uvicorn](https://www.uvicorn.org/) and [nginx](https://nginx.org/en/) for production deployment.
- A [postgresql](https://www.postgresql.org/) database. It is a widely used Open Source RDBMS and it has features like support for JSON and Array data type storage and querying.
- We have also used the [pgvector](https://github.com/pgvector/pgvector) extension mainly for image search.
- Using arrays, we can provide recipe search through ingredients and recipe 
recommendations.

### ML / Dataset

- There are multiple datasets for recipes, with their own pros and cons:
  - [A good curated dataset, especially for Indian dishes but with no 
images.](https://cosylab.iiitd.edu.in/culinarydb/)
  - [The one we are using, but need to scrape ratings, has no images 🙁.](https://www.kaggle.com/datasets/paultimothymooney/recipenlg/data)

  - [This is an ideal dataset.We 
  hope to use this dataset in future.](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews)

  - [This is a small dataset about 
  13k recipes with images, which is within our hardware resources. We are currently using this dataset.](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images)
  - We have used [MobileNetV3](https://arxiv.org/abs/1905.02244) for efficient image feature extraction
- This [medium article](https://towardsdatascience.com/building-a-recipe-recommendation-system-297c229dda7b) might be helpful later, for extracting ingredients.
>Note : To make the DataSet we extract the ingredients part from [Food.com](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) and recipes from [This](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images) Site. Some Indian recipes are also taken from [Food.com](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) and some Indian recipes are manually imported by our group members.

### Frontend / UI

- A social media website like instagram, X (twitter) is often used daily, for them a mobile app can be a better option. Our website will be used less frequently (similar to sites like StackOverflow), thus website is a better fit for frontend.
- Following the trend, we are using [NextJs](https://nextjs.org/) and [Tailwind](https://tailwindcss.com/) for styling. Both of them have massive advantages over traditional web frameworks, like SEO and Image Optimization, small bundle size, multiple rendering techniques etc.
- We are not using complex styles / components, because we have future plans to develop an app, possibly in [React Native](https://reactnative.dev/). React Native is a bit fragile, so the compromise.
- We have used many libraries to provide a good user experience. Like: react-tag-input, react-toastify, react-dropzone etc.
- [This](https://www.realtimecolors.com/?colors=130e01-ffffff-6c3702-00c7a9-1902d6&fonts=Poppins-Poppins) website helped us to decide theme colours and we are using the [Itim](https://fonts.google.com/specimen/Itim) font to match the 
context.

## Applications

- Cooking.
- Learning / Education.
- Social interaction.
