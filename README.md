## Youtube Comments Classifier
The application is a youtube comments classifier, deployed on heroku.

It contains a Youtube comments scraper package (details on how to use is in the api folder), a database hosted on heroku and the app.py.

You can find the repository for the scrapping package here: https://github.com/linda-oranya/YT_comments_scrapper

The application scrapes youtube comments and classifies them as 1 or -1, where 1 is positive and -1 is negative.

## Installation
All the libraries required can be found and installed via requirements.txt in the respective folder.

## Usage
The application can be accessed via 3 end points

The base endpoint:


```
https://yt-comments-db.herokuapp.com/
```


The predict endpoint that makes a prediction with a POST request:

```
  https://yt-comments-db.herokuapp.com/predict
  ```

The predictions endpoint that returns the first 10 predictions with a GET request:

```
  https://yt-comments-db.herokuapp.com/predictions
  ```

  ## Development
  The project is currently completed but is open for contributions. You can create a pull request or raise an issue.

  ## LICENSE
  It is a free software