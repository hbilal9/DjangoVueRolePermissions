<script setup lang="ts">
interface Props {
	title: string;
	description: string;
	isNew?: boolean;
}

defineProps<Props>();
</script>

<template>
	<div class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6 relative">
		<div v-if="isNew" class="absolute top-4 right-4 bg-blue-500 text-white text-xs px-2 py-1 rounded-full">NEW</div>
		<h3 class="text-xl font-semibold mb-2">{{ title }}</h3>
		<p class="text-gray-600 mb-4">{{ description }}</p>
		<div class="flex space-x-3">
			<button class="bg-gray-900 text-white px-4 py-2 rounded-md hover:bg-gray-800 transition-colors">
				Watch tutorial
			</button>
			<button class="border border-gray-300 px-4 py-2 rounded-md hover:bg-gray-50 transition-colors">
				Get this template
			</button>
		</div>
	</div>
</template>
