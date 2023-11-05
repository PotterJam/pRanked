import httpClient from '$lib/httpClient';
import { getPlayerFromReponse, type PlayerResponse } from '$lib/domain/player/player';
import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns'
import { getGameFromReponse, type GameResponse } from '$lib/domain/games/games';

export async function load(): Promise<ConfigureLoadData> {
    const playersResp = await httpClient.get<PlayerResponse[]>('players/');
    const players = playersResp.data.map(getPlayerFromReponse);

    const gamesResp = await httpClient.get<GameResponse[]>('games/');
    const games = gamesResp.data.map(getGameFromReponse);

    return {
        players: players,
        games: games,
    };
}