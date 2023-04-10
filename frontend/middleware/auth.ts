import { useAuthStore } from "@/stores/AuthStore";

const authStore = useAuthStore();

// Reference: https://nuxt.com/docs/getting-started/routing#route-middleware
export default defineNuxtRouteMiddleware((to, from) => {
  if (!authStore.isAuthenticated) {
    return navigateTo('/login/')
  }
});