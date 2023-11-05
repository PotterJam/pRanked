import httpClient from '$lib/httpClient';
import { GetPlayerFromReponse, type PlayerResponse } from '$lib/domain/player/player';
import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns'

export async function load(): Promise<ConfigureLoadData> {
    const { data } = await httpClient.get<PlayerResponse[]>('players/');

    const players = data.map(GetPlayerFromReponse);

    return {
        players: players
    };
}