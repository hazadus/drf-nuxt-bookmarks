<template>
  <Title>About the project | Bookmarks</Title>

  <h2 class="title is-size-2">About this project</h2>
  <div class="content">
    <h3>The Idea</h3>

    <div class="columns">
      <div class="column is-9">
        <p>
          The idea behind this project is to create a web app to collect, classify and store links to
          various useful web resources. I use it myself every day and find it very convenient.
        </p>
        <p>
          Why create your own app, you would say, if we already have Pocket, Notion and built-in browser tools?..
        </p>
        <p>
          First of all, it's fun to use <em>your own tool</em>, which you can extend and adjust to your liking. The second
          thing is that
          I just love to build thing on the web, use new tools and frameworks, learn new stuff every day!
          I also love using Telegram for all the things, and I wanted a tool tightly integrated with it.
        </p>
        <p>
          The project is in active development right now, so expect daily updates if you're interested.
        </p>
      </div>

      <div class="column is-3">
        <figure class="image">
          <img src="/images/logo.jpg" class="logo">
          <figcaption>
            Logo created by Kandinsky 2.1
          </figcaption>
        </figure>
      </div>
    </div>

    <h3>Realisation</h3>
    <p>
      Project was built with love using these amazing tools. I just can't express how great and fun they are!
    </p>

    <div class="columns">
      <div class="column is-6">
        <ul>
          <li>
            <Icon name="logos:django-icon" /> <b>Django</b> as backend framework.
          </li>
          <li>
            <Icon name="logos:python" /> <b>Python</b> for backend programming.
          </li>
          <li>
            <b>Django REST Framework</b> for API.
          </li>
          <li>
            <Icon name="logos:gunicorn" /> <b>Gunicorn</b> as WSGI server.
          </li>
          <li>
            <Icon name="logos:nodejs" /> <b>Node</b> and <b>Nitro</b> to serve frontend.
          </li>
          <li>
            <b>Celery</b> for background tasks.
          </li>
          <li>
            <Icon name="logos:redis" /> <b>Redis</b> as message broker for <b>Celery</b>.
          </li>
          <li>
            <Icon name="logos:nginx" /> <b>Nginx</b> as reverse proxy.
          </li>
          <li>
            <Icon name="logos:telegram" /> <b>Telegram API</b> for bot implementation.
          </li>
          <li>
            <Icon name="logos:docker-icon" /> <b>Docker Compose</b> <em>to run them all</em> on
            <Icon name="logos:ubuntu" /> <b>Ubuntu</b> server!
          </li>
          <li>
            <Icon name="logos:pycharm" /> Backend written in <b>PyCharm Professional</b>.
          </li>
          <li>
            Proudly hosted on <a href="https://timeweb.cloud">Timeweb.cloud</a>.
          </li>
        </ul>
      </div>

      <div class="column is-6">
        <ul>
          <li>
            <Icon name="logos:nuxt-icon" /> <b>Nuxt</b> framework, based on
            <Icon name="logos:vue" /> <b>Vue</b>, for frontend.
          </li>
          <li>
            <Icon name="logos:typescript-icon" /> <b>TypeScript</b> for frontend programming. <i>Much</i> more reliable
            and fun to code than JavaScript!
          </li>
          <li>
            <Icon name="logos:vueuse" /> <b>VueUse</b> for data fetching and other stuff.
          </li>
          <li>
            <b>Pinia</b> for state management.
          </li>
          <li>
            <b>@nuxtjs/i18n</b> for intetnationalization.
          </li>
          <li>
            <Icon name="logos:bulma" /> <b>Bulma</b> for styling.
          </li>
          <li>
            <b>Icônes</b> for icons.
          </li>
          <li>
            <Icon name="logos:visual-studio-code" /> Frontend written in <b>Visual Studio Code</b>.
          </li>
        </ul>
      </div>
    </div>

    <h3>References and links</h3>
    <p>
      Project source code:
      <Icon name="logos:github-octocat" /> <a
        href="https://github.com/hazadus/drf-nuxt-bookmarks">hazadus/drf-nuxt-bookmarks</a>.
    </p>
    <p>
      Any questions or ideas are welcome in <a href="https://github.com/hazadus/drf-nuxt-bookmarks/issues">project's
        Issues</a> section on GitHub.
    </p>
    <p>
      See also: <a href="https://github.com/hazadus/drf-nuxt-bookmarks/blob/main/changelog.md">change log</a>,
      <a href="https://github.com/users/hazadus/projects/4/views/1">project board</a> and
      <a href="https://github.com/hazadus/drf-nuxt-bookmarks/discussions">discussions</a>.
    </p>
  </div>
</template>

<style scoped>
.logo {
  width: 256px;
  height: 256 px;
}
</style>