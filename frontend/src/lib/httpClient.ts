import { PUBLIC_BASE_URL } from '$env/static/public'
import axios, { AxiosError } from 'axios';

const axiosOptions = import.meta.env.PROD ? { baseURL: PUBLIC_BASE_URL } : undefined;
const httpClient = axios.create(axiosOptions);

export default httpClient;

export function isAxiosError<ResponseType>(error: unknown): error is AxiosError<ResponseType> {
    return axios.isAxiosError(error);
}