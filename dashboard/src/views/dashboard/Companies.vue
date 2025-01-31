<script setup lang="ts">
import { useAuthStore } from "@/stores/useAuthStore";
import {} from "vue";

const authStore = useAuthStore();
</script>

<template>
	<div class="flex justify-between">
		<div class="text-2xl font-bold">Companies</div>

		<button
			@click=""
			v-if="authStore.hasPermission('add_company')"
			class="bg-blue-500 text-white px-4 py-2 rounded-md"
		>
			Add Company
		</button>
	</div>
</template>
