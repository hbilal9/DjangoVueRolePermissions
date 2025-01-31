import type { ICredentials, IUser, LoginResponse } from "@/types";
import { http } from "./http";

export function loginService(credentials: ICredentials): Promise<LoginResponse> {
	return http.post("/auth/login/", credentials);
}

export function getProfileService(): Promise<IUser> {
	return http.get("/auth/profile/");
}
