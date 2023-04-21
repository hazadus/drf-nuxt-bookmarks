// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000",
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
        detectBrowserLanguage: {
          // https://v8.i18n.nuxtjs.org/guide/browser-language-detection
          useCookie: true,
          cookieKey: "i18n_redirected",
          redirectOn: "root",
        },
      },
    ],
  ],
  ssr: false,
});
