import httpClient from '$lib/httpClient';
import { getPlayerFromReponse, type PlayerResponse } from '$lib/domain/player/player';
import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns'
import { getGameFromReponse, type GameResponse } from '$lib/domain/games/games';
import { authenticated } from '$lib/auth';

export async function load(): Promise<ConfigureLoadData> {
    try {
        const result = await httpClient.post('/authenticate/');
        if (result.status === 200) {
            authenticated.set(result.data.authenticated);
        }
    } catch (e) {}
    
    const playersResp = await httpClient.get<PlayerResponse[]>('players/');
    const players = playersResp.data.map(getPlayerFromReponse);

    const gamesResp = await httpClient.get<GameResponse[]>('games/');
    const games = gamesResp.data.map(getGameFromReponse);

    return {
        players: players,
        games: games,
    };
}