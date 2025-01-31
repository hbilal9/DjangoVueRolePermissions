export type ICredentials = {
	email: string;
	password: string;
};

export type LoginResponse = {
	user: IUser;
	access_token: string;
};

export interface IUser {
	id: number;
	first_name: string;
	last_name: string;
	full_name: string;
	username: string;
	phone: string;
	email: string;
	role: string;
	user_permissions: string[];
	is_active: boolean;
	date_joined: string;
}

export interface ICreateBaseUser {
	first_name: string;
	last_name: string;
	username: string;
	email: string;
}
