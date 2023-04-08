# drf-nuxt-bookmarks

Site bookmarking service consisting of Telegram bot to receive URLs, DRF API, Celery worker (process tasks passed by
telegram bot), and Nuxt/Vue UI.

## Tech stack used

### Frameworks and libraries

- Backend: [Django](https://www.djangoproject.com/)
  - [Django REST Framework](https://www.django-rest-framework.org/): REST API on the backend was built using this battle-tested framework. It's powerful, well-documented and easy to use.
  - [djoser](https://djoser.readthedocs.io/en/latest/introduction.html): REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation.
- Telegram bot: [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
  - [requests](https://requests.readthedocs.io/en/latest/): Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data.
- Frontend:
  - [Nuxt 3](https://nuxt.com/)
    - [@vueuse/nuxt](https://nuxt.com/modules/vueuse): Collection of essential Vue Composition Utilities.
    - [nuxt-icon](https://nuxt.com/modules/icon): Icon module for Nuxt with 100,000+ ready to use icons from Iconify.
      - [Icones](https://icones.js.org) catalogue.
  - [Bulma](https://www.npmjs.com/package/bulma): [Bulma](https://bulma.io/) is a modern CSS framework based on Flexbox.

### References

- Nuxt
  - [Exposing Runtime Config](https://nuxt.com/docs/guide/going-further/runtime-config)
- Vue
  - [TypeScript with Composition API](https://vuejs.org/guide/typescript/composition-api.html)
    - [Typing component props](https://vuejs.org/guide/typescript/composition-api.html#typing-component-props)

### Notes

#### Frontend

##### Naming Conventions

"The" in the component name means there's indended to be only one instance of this component in the app, e.g. `TheNavbar`.

## Deploying

### Running with Docker Compose

...Yet to be written in detail...

- Install docker & compose
  - [Install Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
  - [Install Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
