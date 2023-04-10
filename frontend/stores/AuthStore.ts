import { defineStore } from "pinia";
import type { User } from "@/types";

interface StateShape {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore("AuthStore", {
  state: (): StateShape => ({ 
    token: null,
    user: null,
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

      const userInfo = localStorage.getItem("user");
      if (userInfo) {
        this.user = JSON.parse(userInfo);
      } else {
        localStorage.setItem("user", JSON.stringify(this.user));
      }
    },
    logIn(token: string, user: User) {
      this.token = token;
      this.user = user;
      this.isAuthenticated = true;
      localStorage.setItem("token", this.token);
      localStorage.setItem("user", JSON.stringify(this.user));
    },
    logOut() {
      this.token = "";
      this.user = null;
      this.isAuthenticated = false;
      localStorage.setItem("token", this.token);
      localStorage.setItem("user", JSON.stringify(this.user));
    },
  },
})