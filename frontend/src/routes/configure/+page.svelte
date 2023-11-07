<script lang="ts">

	import GameSubmitter from '../../components/configure/GameSubmitter.svelte';
	import AddPlayer from '../../components/configure/AddPlayer.svelte';
	import { Button, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

	import type { Game } from '$lib/domain/games/games';
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';

	import { authenticated } from '$lib/auth';
	import httpClient from '$lib/httpClient';

	let adminPassword = '';
	const authenticateAdmin = async () => {
		const result = await httpClient.post('/authenticate/', null, { headers: { 'admin_password': adminPassword }});
		$authenticated = result.data.authenticated;
	}

    export let data: ConfigureLoadData;
    let players = data.players;
    $: playerNames = players.map((p) => p.username);

	let games: Game[] = data.games;

	const formatRatingChange = (no: number) => no > 0 ? `+${Math.floor(no)}` : Math.floor(no);
</script>

<div class="flex flex-col items-center justify-center pt-10 pb-20 px-2">
	{#if !$authenticated}
		<div class="text-center pt-7 pb-5 px-2 text-3xl font-bold">Admin login</div>
		<div class="flex">
			<Input class="w-48" placeholder="Password..." rows="1" bind:value={adminPassword} />
			<Button class="ml-2" on:click={authenticateAdmin}> Login </Button>
		</div>
	{/if}
	
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
						<TableBodyCell>{game.winnerUsername} {Math.floor(game.winnerRating)} ({formatRatingChange(game.winnerRatingChange)})</TableBodyCell>
						<TableBodyCell>{game.loserUsername} {Math.floor(game.loserRating)} ({formatRatingChange(game.loserRatingChange)})</TableBodyCell>
						<TableBodyCell>{game.draw ? 'Yes' : ''}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
			</Table>
	</div>
</div>
