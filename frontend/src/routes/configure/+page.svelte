<script lang="ts">

	import GameSubmitter from '../../components/configure/GameSubmitter.svelte';
	import AddPlayer from '../../components/configure/AddPlayer.svelte';
	import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

	import type { Game } from '$lib/domain/games/games';
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';

    export let data: ConfigureLoadData;
    let players = data.players;
    $: playerNames = players.map((p) => p.username);

	let games: Game[] = data.games;
</script>

<div class="flex flex-col items-center justify-center pt-10 pb-20 px-2">
	<AddPlayer playerNames={playerNames} bind:players={players}/>

	<GameSubmitter players={players} bind:games={games}/>

	<div class="m-3 mt-10">
		<Table>
			<TableHead>
				<TableHeadCell>Game</TableHeadCell>
				<TableHeadCell>Winner</TableHeadCell>
				<TableHeadCell>Loser</TableHeadCell>
				<TableHeadCell>Draw</TableHeadCell>
			</TableHead>
			<TableBody>
				{#each games.sort(( a, b ) => b.gameId - a.gameId) as game}
					<TableBodyRow>
						<TableBodyCell>{game.gameId}</TableBodyCell>
						<TableBodyCell>{game.winnerUsername} | {Math.floor(game.winnerRating)} (+{Math.floor(game.winnerRatingGained)})</TableBodyCell>
						<TableBodyCell>{game.loserUsername} | {Math.floor(game.loserRating)} (-{Math.floor(game.loserRatingLost)})</TableBodyCell>
						<TableBodyCell>{game.draw ? 'Yes' : ''}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
			</Table>
	</div>
</div>
