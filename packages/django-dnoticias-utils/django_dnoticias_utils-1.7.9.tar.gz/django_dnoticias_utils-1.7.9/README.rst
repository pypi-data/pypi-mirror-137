# Utils module (dnoticias.pt)

Django package used in subscriptions, editions, comments and mail system.
This package has the most common functions used in every project, like http error handlers, delete functions,
checkers, etc.

## Views

### Select2View

View used to construct the select2 inputs data

To make this view works, you will need to replace this attrs:

| Attribute | Description |
| :--- | :--- |
| SEARCH_PARAMS | The model attribute you will search for. I.e: Name, dni, etc |
| SEARCH_TYPE | Django search type (icontains, lte, gte, etc) |
| ORDER_BY_PARAMS | The model attribute you will order for |
| MODEL | Model used in the input |
| MODEL_VERBOSE_NAMES | Input name |

### GenericDeleteView

View used to delete an object from database.


### LivenessCheckView

This view is used to do the liveness check. This will check the following things:

1. Database connection
2. Homepage load (optional)

And, in case of failure, will send an email (if configured) to the DEFAULT_IT_EMAIL.

| Setting | Type | Description |
| :--- | :--- | :--- |
| DEFAULT_IT_EMAIL | String | Email address that will be notified in case of failure |
| EMAIL_TEMPLATE_LIVENESS_FAIL_UUID | String | Email template UUID |
| LIVENESS_CHECK_HOMEPAGE | Boolean | Check homepage? |
| LIVENESS_SEND_EMAIL_ON_FAILURE | Boolean | Send email on failure? |
| LIVENESS_CACHE_NAME | String | Cache cooldown name |
| LIVENESS_EMAIL_COOLDOWN | String | Cache cooldown time |

In case of having middleware (yes), you will need to add the liveness check url to the OIDC_EXEMPT_URLS and AUTH_EXEMPT_URLS 
regex list

```
re.compile(r'(?:\/check\/health)(.*)'),
```

And now, remember to add the liveness to the main path urls.py

```
from django.urls import path
...
from dnoticias_utils.views import LivenessCheckView
...

urlpatterns = [
    ...

    # Liveness check url
    path('check/health/', LivenessCheckView.as_view(), name="liveness-check"),
]
```

## Error views (error_views.py)
This file contains functions to handle the different http errors. Instead of use different views in html, we have
only one view with context.
