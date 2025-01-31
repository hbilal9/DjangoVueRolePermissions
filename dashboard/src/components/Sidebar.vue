<script setup lang="ts">
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();
type MenuItem = { name: string; icon: string; path: string; condition: string };
const menuItems: MenuItem[] = [
	{ name: "Dashboard", icon: "template", path: "/dashboard", condition: "view_dashboard" },
	{ name: "Companies", icon: "folder", path: "/companies", condition: "view_company" },
];
</script>

<template>
	<div class="w-64 h-screen bg-white shadow-lg p-4">
		<h1 class="text-xl font-semibold text-gray-800">Role Base System</h1>
		<div class="space-y-4 mt-12">
			<template v-for="item in menuItems" :key="item.name">
				<router-link
					:to="item.path"
					class="flex items-center p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
					v-if="authStore.hasPermission(item.condition)"
				>
					{{ item.name }}
				</router-link>
			</template>
		</div>
	</div>
</template>

<style scoped>
.router-link-active {
	@apply bg-gray-100 text-indigo-600;
}
</style>
