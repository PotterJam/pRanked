import { PUBLIC_BASE_URL } from '$env/static/public'
import axios, { AxiosError } from 'axios';

const httpClient = axios.create({
    baseURL: PUBLIC_BASE_URL
});

export default httpClient;

export function isAxiosError<ResponseType>(error: unknown): error is AxiosError<ResponseType> {
    return axios.isAxiosError(error);
}