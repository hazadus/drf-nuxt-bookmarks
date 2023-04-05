# drf-nuxt-bookmarks

Site bookmarking service consisting of Telegram bot to receive URLs, DRF API, Celery worker (process tasks passed by 
telegram bot), and Nuxt/Vue UI.

## Tech stack used

### Frameworks and libraries

- Backend: [Django](https://www.djangoproject.com/)
  - [Django REST Framework](https://www.django-rest-framework.org/): REST API on the backend was built using this battle-tested framework. It's powerful, well-documented and easy to use.
  - [djoser](https://djoser.readthedocs.io/en/latest/introduction.html): REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation.
