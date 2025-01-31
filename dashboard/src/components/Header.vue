<script setup lang="ts">
import { useAuthStore } from "@/stores/useAuthStore";

const title = "Dashboard";

const authStore = useAuthStore();
</script>

<template>
	<nav class="bg-white shadow-md p-4">
		<div class="container mx-auto flex justify-between items-center">
			<h1 class="text-xl font-bold">{{ title }}</h1>
			<div class="space-x-4">
				<button @click="authStore.logout" class="text-gray-600 hover:text-gray-900">Logout</button>
			</div>
		</div>
	</nav>
</template>
