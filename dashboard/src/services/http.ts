import Axios, { type AxiosInstance, type Method } from "axios";
import { useAuthStore } from "@/stores/useAuthStore";

class Http {
	client: AxiosInstance;
	token = "";

	public request<T>(method: Method, url: string, data: Record<string, any> = {}, onUploadProgress?: any) {
		return this.client.request({
			url,
			data,
			method,
			onUploadProgress,
			headers:
				data instanceof FormData
					? { "Content-Type": "multipart/form-data" }
					: { "Content-Type": "application/json" },
		}) as Promise<{ data: T }>;
	}

	public async get<T>(url: string) {
		return (await this.request<T>("get", url)).data;
	}

	public async post<T>(url: string, data: Record<string, any>, onUploadProgress?: any, headers?: any) {
		if (headers) {
			this.client.defaults.headers = headers;
		}
		return (await this.request<T>("post", url, data, onUploadProgress)).data;
	}

	public async put<T>(url: string, data: Record<string, any>) {
		return (await this.request<T>("put", url, data)).data;
	}

	public async delete<T>(url: string, data: Record<string, any> = {}) {
		return (await this.request<T>("delete", url, data)).data;
	}

	constructor() {
		this.token = "";
		this.client = Axios.create({
			headers: {
				"Content-Type": "application/json",
			},
		});

		// Intercept the request to make sure the token is injected into the header.
		this.client.interceptors.request.use((config) => {
			config.baseURL = "http://localhost:8000/api";
			if (useAuthStore().getAccessToken())
				config.headers.Authorization = `Bearer ${useAuthStore().getAccessToken()}`;
			return config;
		});

		// Intercept the response and…
		this.client.interceptors.response.use(
			(response) => {
				return response;
			},
			(error) => {
				// Also, if we receive a Bad Request / Unauthorized error
				if (error.response?.status === 400 || error.response?.status === 401) {
					// and we're not trying to log in
					if (!(error.config.method === "post" && error.config.url === "profile")) {
						// the token must have expired. Log out.
					}
				}

				return Promise.reject(error);
			}
		);
	}
}

export const http = new Http();
