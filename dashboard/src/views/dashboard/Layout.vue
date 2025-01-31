<script setup lang="ts">
import Header from "@/components/Header.vue";
import Sidebar from "@/components/Sidebar.vue";
</script>

<template>
	<div class="min-h-screen bg-gray-100 flex">
		<Sidebar />
		<div class="flex-1">
			<Header />
			<main class="container mx-auto p-6">
				<router-view />
			</main>
		</div>
	</div>
</template>
