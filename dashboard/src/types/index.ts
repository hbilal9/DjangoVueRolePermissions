export * from "./auth";

export type ErrorType<T> = Record<keyof T, string[]>;

export type Pagination<T> = {
	total_pages: number;
	total: number;
	results: T[];
	per_page: number;
	current_page: number;
	next: string;
	previous: string;
};
