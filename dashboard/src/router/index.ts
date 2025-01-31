import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/useAuthStore";
import type { RouteLocationNormalized, NavigationGuardNext } from "vue-router";

const routes = [
	{
		path: "/",
		redirect: "/dashboard",
	},
	{
		path: "/",
		name: "dashboard",
		component: () => import("@/views/dashboard/Layout.vue"),
		children: [
			{
				path: "dashboard",
				name: "dashboard.home",
				component: () => import("@/views/dashboard/Home.vue"),
			},
			{
				path: "companies",
				name: "dashboard.companies",
				component: () => import("@/views/dashboard/Companies.vue"),
			},
		],
		beforeEnter: (_to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
			const authStore = useAuthStore();
			if (authStore.isLoggedIn) {
				next();
			} else {
				next("/login");
			}
		},
	},
	{
		path: "/login",
		name: "login",
		component: () => import("../views/Login.vue"),
	},
	{
		path: "/:pathMatch(.*)*",
		name: "not-found",
		component: () => import("../views/NotFound.vue"),
	},
];

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: routes,

	linkActiveClass: "active",
	linkExactActiveClass: "active",
});

router.beforeEach((to, _from, next) => {
	const authStore = useAuthStore();
	if (to.matched.some((record) => record.meta.requiredAuth)) {
		if (authStore.isLoggedIn) {
			next();
		} else {
			next({
				path: "/login",
				query: { redirect: to.fullPath },
			});
		}
	} else {
		next();
	}
});

export default router;
