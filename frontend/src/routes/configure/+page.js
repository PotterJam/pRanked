import { PUBLIC_BASE_URL } from '$env/static/public'

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    const response = await fetch(PUBLIC_BASE_URL + 'player/');

    return {
        players: await response.json()
    };
}