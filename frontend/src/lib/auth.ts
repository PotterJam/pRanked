import { writable } from 'svelte/store';
import httpClient from './httpClient';

export const authenticated = writable(false)

