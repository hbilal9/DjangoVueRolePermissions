import type { PiniaPluginContext, SubscriptionCallbackMutation, StateTree } from "pinia";

export const usePersistAuthStore = (context: PiniaPluginContext) => {
	if (context.store.$id === "authStore") {
		const data = localStorage.getItem("authStore");
		if (data) {
			//   context.store.$state = JSON.parse(data);
			context.store.$state = JSON.parse(data);
		}

		context.store.$subscribe((event: SubscriptionCallbackMutation<StateTree>) => {
			if (context.store.$state.isLoggedIn) {
				localStorage.setItem("authStore", JSON.stringify(context.store.$state));
			} else {
				localStorage.removeItem("authStore");
			}
		});
	}
};
