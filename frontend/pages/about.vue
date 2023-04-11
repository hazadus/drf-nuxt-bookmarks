<template>
  <Title>About the project | Bookmarks</Title>

  <h2 class="title is-size-2">About this project</h2>
  <div class="content">
    <h3>The Idea</h3>

    <div class="columns">

      <div class="column is-9">
        <p>
          The idea behind this project was to create a web app to collect, classify and store links to
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
      Project was built with passion using these amazing tools. I just can't express how great and fun they are!
    </p>

    <ul>
      <li>
        <Icon name="logos:django-icon" /> <b>Django</b> for backend.
      </li>
      <li>
        <b>Django REST Framework</b> for API.
      </li>
      <li>
        <Icon name="logos:nuxt-icon" /> <b>Nuxt</b> and
        <Icon name="logos:vue" /> <b>Vue</b> for frontend.
      </li>
      <li>
        <Icon name="logos:bulma" /> <b>Bulma</b> for styling.
      </li>
      <li>
        <Icon name="logos:nginx" /> <b>Nginx</b> as reverse proxy.
      </li>
      <li>
        <Icon name="logos:docker-icon" /> <b>Docker Compose</b> <em>to run them all</em> on
        <Icon name="logos:ubuntu" /> <b>Ubuntu</b> server!
      </li>
    </ul>

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
  </div>
</template>

<style scoped>
.logo {
  width: 256px;
  height: 256 px;
}
</style>