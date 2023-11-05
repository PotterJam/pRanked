export interface PlayerResponse {
    player_id: number;
    username: string;
    rating: number;
    rating_deviation: number;
}

export interface Player {
    playerId: number;
    username: string;
    rating: number;
    ratingDeviation: number;
}

export const GetPlayerFromReponse = (response: PlayerResponse): Player => ({
    playerId: response.player_id,
    username: response.username,
    rating: response.rating,
    ratingDeviation: response.rating_deviation,
});