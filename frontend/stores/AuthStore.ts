import { defineStore } from "pinia";

interface StateShape {
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('AuthStore', {
  state: (): StateShape => ({ 
    token: null,
    isAuthenticated: false, 
  }),
  getters: {
  },
  actions: {
    initializeStore() {
      if (localStorage.getItem("token")) {
        this.token = localStorage.getItem("token");
        this.isAuthenticated = true;
      } else {
        this.token = null;
        this.isAuthenticated = false;
      }
    },
    logIn(token: string) {
      this.token = token;
      this.isAuthenticated = true;
      localStorage.setItem("token", this.token);
    },
    logOut() {
      this.token = "";
      this.isAuthenticated = false;
      localStorage.setItem("token", this.token);
    },
  },
})