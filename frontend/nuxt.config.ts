// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000",
    },
  },
  app: {
    head: {
      script: [
        {
          src: "https://stats.hazadus.ru/script.js",
          async: true,
          "data-website-id": "34bc330a-3f55-48ef-b7fc-051a6f309fcf",
        },
      ],
    },
  },
  modules: [
    "@vueuse/nuxt",
    "nuxt-icon",
    "@pinia/nuxt",
    [
      "@nuxtjs/i18n",
      {
        locales: [
          {
            code: "en",
            name: "🇬🇧 English",
          },
          {
            code: "ru",
            name: "🇷🇺 Русский",
          },
        ],
        defaultLocale: "en",
        fallbackLocale: "en",
        strategy: "no_prefix",
        // https://v8.i18n.nuxtjs.org/guide/browser-language-detection
        detectBrowserLanguage: false,
      },
    ],
  ],
  ssr: false,
});
