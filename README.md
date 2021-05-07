# How to run the application
**Note**: To avoid conflict with your current packages, please use the [venv](https://docs.python.org/3/library/venv.html) to install from the requirements.txt.
```
cd book_store
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py runserver
```

# Overview of the Django Application Structure
In this project, it uses two applications called 'account' and 'store'. For all the user authentications, the account application is responsible for handling the authentication part. The store application will handle the ecommerce functionalities.

The machine learning modeling are serialized and deserialized into django's 'store' app and 'account' app. For 'account' app, it uses joblib to deserialize the MBA model, and dump api from suprise library is used to deserialize the item-to-item collaborative filtering system. Similarly, user-to-user model is deserialized with dump api and loaded into 'account' application.

As a side note, all machine learning models are trained and serialized for the purpose of implementating current project.

# User Authentication
- Registraton
- Login
- Logout
- Editing the User Profile
- Changing the Password

# Ecommerce Functionalities
- Add To Cart
- Remove From Cart
- Checkout the Cart
- Hard Coded Purchase History for Demonstration of User-based Collaborative Filtering System

# Machine Learning Capabilities (Recommendation System)
- Affinity Analysis or Market Basket Analysis (MBA)
- Collaborative Filtering

# Explanation on Machine Learning Models
The implementation learns from amazon ecommerce gaint which is also one of the best ecommerce recommendation engine. The detail of the recommendation engine is explained on the "Explanation on Recommendation System" page of the website. The overview of the machine learning models together with their usages are as follow:
1. Market Basket Analysis
- Customers who love this book also love
- Frequently bought together

2. Item-To-Item Collaborative Filtering
- Books related to this item

3. User-To-User Collaborative Filtering
- Recommended books for you

*For MBA model, the rules.sav file is exceeded the file size limit and Git LFS is used to overcome the problem.*
