import type { RatingHistory } from "$lib/domain/player/player";
import type { GraphsLoadData } from "$lib/domain/routeLoadReturns";
import httpClient from "$lib/httpClient";


export async function load(): Promise<GraphsLoadData> {
    const ratingsHistoryResp = await httpClient.get<RatingHistory[]>('/api/players/rating-history');

    return {
        ratingHistoryGraphData: ratingsHistoryResp.data
    }
}