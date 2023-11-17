import type { Game } from "./games/games"
import type { Player, RatingHistory } from "./player/player"


export interface ConfigureLoadData {
    players: Player[]
    games: Game[]
}


export interface ConfigureLeaderboardData {
    players: Player[]
}

export interface GraphsLoadData {
    ratingHistoryGraphData: RatingHistory[]
}
