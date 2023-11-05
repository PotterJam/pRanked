export interface GameResponse {
    game_id: number;
    draw: boolean;
    winner_id: number;
    winner_username: string;
    loser_id: number;
    loser_username: string;
    winner_rating: number;
    loser_rating: number;
}

export interface Game {
    gameId: number;
    draw: boolean;
    winnerId: number;
    winnerUsername: string;
    loserId: number;
    loserUsername: string;
    winnerRating: number;
    loserRating: number;
}

export const getGameFromReponse = (response: GameResponse): Game => ({
    gameId: response.game_id,
    draw: response.draw,
    winnerId: response.winner_id,
    winnerUsername: response.winner_username,
    loserId: response.loser_id,
    loserUsername: response.loser_username,
    winnerRating: response.winner_rating,
    loserRating: response.loser_rating,
});

export interface SubmitGameRequest {
    winner_id: number;
    loser_id: number;
    draw: boolean;
}

export interface SubmitGameResponse {
    game_id: number;
    old_winner_rating: number;
    old_loser_rating: number;
    new_winner_rating: number;
    new_loser_rating: number;
}

export interface NewGameResult {
    gameId: number;
    oldWinnerRating: number;
    oldLoserRating: number;
    newWinnerRating: number;
    newLoserRating: number;
}

export const getGameResultFromResponse = (response: SubmitGameResponse): NewGameResult => ({
    gameId: response.game_id,
    oldWinnerRating: response.old_winner_rating,
    oldLoserRating: response.old_loser_rating,
    newWinnerRating: response.new_winner_rating,
    newLoserRating: response.new_loser_rating,
});