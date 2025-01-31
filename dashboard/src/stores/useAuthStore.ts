import { ref, computed } from "vue";
import { defineStore } from "pinia";
import type { ICredentials, ErrorType, IUser, LoginResponse } from "@/types";
import { useRouter, useRoute } from "vue-router";
import { http } from "@/services/http";
import * as authService from "@/services/authService";

export const useAuthStore = defineStore("authStore", () => {
	const isLoggedIn = ref(false);
	const user = ref<IUser | null>(null);
	const loginError = ref<loginError>();
	const allowdRoles = ["superadmin", "admin", "company", "manager"];

	const router = useRouter();
	const route = useRoute();

	type loginError = {
		message: string;
		errors: ErrorType<ICredentials>;
	};

	const login = async (credentials: ICredentials) => {
		loginError.value = {} as loginError;
		try {
			const response = await authService.loginService(credentials);
			isLoggedIn.value = true;
			user.value = response.user;
			localStorage.setItem("user", JSON.stringify(response.user));
			localStorage.setItem("access_token", response.access_token);
			const redirect = (route.query.redirect as string) || `/dashboard`;
			router.push(redirect);
			return response.user;
		} catch (error: any) {
			loginError.value = error.response.data;
		}
	};

	const setUser = (data: IUser) => {
		user.value = data;
	};

	const getAccessToken = () => {
		return localStorage.getItem("access_token") || null;
	};

	const getProfile = async () => {
		try {
			const response = await authService.getProfileService();
			user.value = response;
			isLoggedIn.value = true;
		} catch (error) {
			logout();
		}
	};

	const logout = async () => {
		isLoggedIn.value = false;
		user.value = null;
		clearCookies();
	};

	const getFullName = computed(() => {
		return `${user.value?.first_name} ${user.value?.last_name}`;
	});

	const hasPermission = (permission: string) => {
		if (!user.value) return false;
		if (user.value.user_permissions.includes(permission)) return true;
		return false;
	};

	const clearCookies = () => {
		localStorage.removeItem("user");
		localStorage.removeItem("access_token");
		router.push("/login");
	};

	return {
		isLoggedIn,
		user,
		loginError,
		login,
		setUser,
		getAccessToken,
		getProfile,
		logout,
		clearCookies,
		getFullName,
		hasPermission,
	};
});
