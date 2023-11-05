<script lang="ts">
	import type { ConfigureLeaderboardData } from "$lib/domain/routeLoadReturns";
	import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

    export let data: ConfigureLeaderboardData;
    let players = data.players;
</script>

<div class="m-5 mt-10 max-w-md m-auto">
    <Table>
        <TableHead>
            <TableHeadCell>Rank</TableHeadCell>
            <TableHeadCell>Player</TableHeadCell>
            <TableHeadCell>Rating</TableHeadCell>
        </TableHead>
        <TableBody>
            {#each players.sort((a, b) => b.rating - a.rating) as player, i}
                <TableBodyRow>
                    <TableBodyCell>{i}</TableBodyCell>
                    <TableBodyCell>{player.username}</TableBodyCell>
                    <TableBodyCell>{Math.floor(player.rating)}</TableBodyCell>
                </TableBodyRow>
            {/each}
        </TableBody>
        </Table>
</div>