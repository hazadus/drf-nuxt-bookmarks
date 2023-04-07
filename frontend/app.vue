<script setup lang="ts">
import { createDOMCompilerError } from '@vue/compiler-dom';
import type { Bookmark } from './types';

const config = useRuntimeConfig()
const { data } = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`);

console.log(config.public.apiBase)

</script>

<template>
  <nav class="navbar has-shadow">
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
        <div class="navbar-item">
          <div>
            <small>Hazadus Bookmarks App</small>
          </div>
        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item has-dropdown is-hoverable">
          <div class="navbar-link">
            Username
          </div>
          <div class="navbar-dropdown is-right">
            <a class="navbar-item">
              <div>
                <span class="icon is-small">
                  <i class="fa fa-user-circle-o"></i>
                </span>
                Profile
              </div>
            </a>
            <a class="navbar-item">
              <div>
                <span class="icon is-small">
                  <i class="fa fa-sign-out"></i>
                </span>
                Sign Out
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <section class="section">
    <div class="columns">
      <div class="column is-4-tablet is-3-desktop is-2-widescreen">
        <nav class="menu">
          <p class="menu-label">
            Menu
          </p>
          <ul class="menu-list">
            <li>
              <a class="is-active" href="#">
                <span class="icon">
                  <i class="fa fa-tachometer"></i>
                </span>
                Inbox
              </a>
            </li>
            <li>
              <a href="books.html">
                <span class="icon">
                  <i class="fa fa-book"></i>
                </span>
                Favorites
              </a>
            </li>
            <li>
              <a href="customers.html">
                <span class="icon">
                  <i class="fa fa-address-book"></i>
                </span>
                Trash
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <div class="column">
        <h1 class="title ">Bookmarks</h1>

        <nav class="level">
          <div class="level-left">
            <div class="level-item">
              <p class="subtitle is-5">
                <strong>{{ data?.length }}</strong> total
              </p>
            </div>
            <div class="level-item is-hidden-tablet-only">
              <div class="field has-addons">
                <p class="control">
                  <input class="input" type="text" placeholder="Title, description…">
                </p>
                <p class="control">
                  <button class="button">
                    Search
                  </button>
                </p>
              </div>
            </div>
          </div>

          <div class="level-right">
            <p class="level-item"><strong>All</strong></p>
            <p class="level-item"><a>Unread</a></p>
            <p class="level-item"><a>Read</a></p>
          </div>
        </nav>

        <table class="table is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>
                <Icon name="material-symbols:star" />
              </th>
              <th>Title</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <th>
                <Icon name="material-symbols:star" />
              </th>
              <th>Title</th>
              <th>Actions</th>
            </tr>
          </tfoot>
          <tbody>
            <tr v-for="bookmark in data" :key="bookmark.id">
              <td>
                <Icon name="material-symbols:star" v-if="bookmark.is_favorite" />
              </td>
              <td>
                <a :href="bookmark.url" target="_blank">{{ bookmark.title }}</a>
                <template v-if="bookmark.tags.length">
                  <span class="tag is-info is-light ml-1" v-for="tag in bookmark.tags">{{ tag.title }}</span>
                </template>
              </td>
              <td></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<style>
@import 'bulma/css/bulma.css'
</style> 