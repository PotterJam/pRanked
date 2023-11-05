import httpClient from '$lib/httpClient';
import { getPlayerFromReponse, type PlayerResponse } from '$lib/domain/player/player';
import type { ConfigureLeaderboardData } from '$lib/domain/routeLoadReturns'

export async function load(): Promise<ConfigureLeaderboardData> {
    const playersResp = await httpClient.get<PlayerResponse[]>('players/');
    const players = playersResp.data.map(getPlayerFromReponse);

    return {
        players: players
    };
}