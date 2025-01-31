<script setup lang="ts">
import { useAuthStore } from "@/stores/useAuthStore";
import { computed, reactive, ref } from "vue";

const authStore = useAuthStore();

const user = reactive({
	email: "hbilal@gmail.com",
	password: "password",
});

const handleLogin = async () => {
	await authStore.login(user);
};
</script>

<template>
	<div class="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
			<div>
				<h2 class="text-center text-3xl font-bold text-gray-900">Welcome to</h2>
				<h1 class="text-center text-3xl font-bold text-indigo-600 mt-2">Design School</h1>
			</div>
			<form class="mt-8 space-y-6" @submit.prevent="handleLogin">
				<div class="rounded-md shadow-sm space-y-4">
					<div>
						<label for="email" class="sr-only">Email address</label>
						<div class="relative">
							<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
								<span class="text-gray-500">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-5 h-5"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"
										/>
									</svg>
								</span>
							</div>
							<input
								v-model="user.email"
								id="email"
								name="email"
								type="email"
								required
								class="appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Email address"
							/>
						</div>
					</div>
					<div>
						<label for="password" class="sr-only">Password</label>
						<div class="relative">
							<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
								<span class="text-gray-500">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-5 h-5"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"
										/>
									</svg>
								</span>
							</div>
							<input
								v-model="user.password"
								id="password"
								name="password"
								type="password"
								required
								class="appearance-none rounded-md relative block w-full pl-10 pr-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Password"
							/>
						</div>
					</div>
				</div>

				<div class="flex items-center justify-between">
					<div class="flex items-center">
						<input
							id="remember-me"
							name="remember-me"
							type="checkbox"
							class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
						/>
						<label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
					</div>

					<div class="text-sm">
						<router-link to="/forgot-password" class="font-medium text-indigo-600 hover:text-indigo-500">
							Forgot Password?
						</router-link>
					</div>
				</div>

				<div>
					<button
						type="submit"
						class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
					>
						Login
					</button>
				</div>

				<div class="text-center text-sm">
					<span class="text-gray-600">Don't have an account?</span>
					<router-link to="/register" class="font-medium text-indigo-600 hover:text-indigo-500 ml-1">
						Register
					</router-link>
				</div>
			</form>
		</div>
	</div>
</template>

<style scoped></style>
