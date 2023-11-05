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

	<div class="m-5 mt-10">
		<Table>
			<TableHead>
				<TableHeadCell>Winner</TableHeadCell>
				<TableHeadCell>Rating</TableHeadCell>
				<TableHeadCell>Loser</TableHeadCell>
				<TableHeadCell>Rating</TableHeadCell>
				<TableHeadCell>Draw</TableHeadCell>
			</TableHead>
			<TableBody>
				{#each games as game}
					<TableBodyRow>
						<TableBodyCell>{game.winnerUsername}</TableBodyCell>
						<TableBodyCell>{Math.floor(game.winnerRating)}</TableBodyCell>
						<TableBodyCell>{game.loserUsername}</TableBodyCell>
						<TableBodyCell>{Math.floor(game.loserRating)}</TableBodyCell>
						<TableBodyCell>{game.draw ? 'Yes' : ''}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
			</Table>
	</div>
</div>
