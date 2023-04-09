<script setup>
const route = useRoute();
</script>

<template>
  <nav class="navbar has-shadow is-link">
    <div class="container is-widescreen">

      <div class="navbar-brand">
        <a class="navbar-item">
          <img src="/images/logo.jpg">
        </a>
        <div class="navbar-burger burger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <!-- Site title -->
          <div class="navbar-item">
            <div>
              <small>Hazadus Bookmarks App</small>
            </div>
          </div>
          <!-- Menu items -->
          <a class="navbar-item" href="#">
            Add
          </a>
          <NuxtLink to="/bookmarks/" class="navbar-item" :class="route.path === '/bookmarks/' ? 'is-active' : ''">
            Bookmarks
          </NuxtLink>
          <NuxtLink to="/about/" class="navbar-item" :class="route.path === '/about/' ? 'is-active' : ''">
            About
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <!-- Buttons -->
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">
                Log in
              </a>
            </div>
          </div>

          <!-- Profile drop-down -->
          <div class="navbar-item has-dropdown is-hoverable">
            <div class="navbar-link">
              <figure class="image is-32x32 mr-2">
                <img class="is-rounded" src="/images/logo.jpg">
              </figure>
              hazadus
            </div>
            <div class="navbar-dropdown is-right">
              <a class="navbar-item">
                <div>
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  Profile
                </div>
              </a>
              <a class="navbar-item">
                <div>
                  <span class="icon">
                    <Icon name="mdi:logout" />
                  </span>
                  Sign Out
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>