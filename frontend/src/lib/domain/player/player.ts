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

export const getPlayerFromReponse = (response: PlayerResponse): Player => ({
    playerId: response.player_id,
    username: response.username,
    rating: response.rating,
    ratingDeviation: response.rating_deviation,
});

export interface RatingHistoryResponse {
    player_name: string;
    rating: number;
    rating_deviation: number;
    date: string;
}

export interface RatingHistory {
    playerName: string;
    rating: number;
    ratingDeviation: number;
    date: Date;
}

export const getRatingHistoryFromResponse = (response: RatingHistoryResponse): RatingHistory => ({
    playerName: response.player_name,
    rating: response.rating,
    ratingDeviation: response.rating_deviation,
    date: new Date(response.date),
});
