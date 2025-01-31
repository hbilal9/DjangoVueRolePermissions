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
			// dont allow access to this route if user dont have permission view_company
			{
				path: "companies",
				name: "dashboard.companies",
				meta: {
					requiresPermission: "view_company", // Define the required permission
				},
				component: () => import("@/views/dashboard/Companies.vue"),
			},
		],
		beforeEnter: (to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
			const authStore = useAuthStore();

			// Check if the user is logged in
			if (!authStore.isLoggedIn) next("/login");
			// Check if the route requires a specific permission
			if (to.meta.requiresPermission) {
				const requiredPermission = to.meta.requiresPermission as string;
				if (!authStore.hasPermission(requiredPermission)) {
					// Redirect to a fallback route (e.g., dashboard or 403 page)
					return next("/dashboard");
				}
			}
			// Allow access to the route
			next();
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
