<script setup lang="ts">
import TemplateCard from "./TemplateCard.vue";

const templates = [
	{
		title: "Create Your Education App",
		description: "In this tutorial you will learn how to simply create an education application.",
		isNew: true,
	},
	{
		title: "AI Finance App",
		description: "Build a modern finance application with AI integration.",
		isNew: false,
	},
	{
		title: "Chat AI",
		description: "Create a real-time chat application with AI capabilities.",
		isNew: false,
	},
];
</script>

<template>
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
		<TemplateCard
			v-for="template in templates"
			:key="template.title"
			:title="template.title"
			:description="template.description"
			:isNew="template.isNew"
		/>
	</div>
</template>
