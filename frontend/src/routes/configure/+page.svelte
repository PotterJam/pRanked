<script lang="ts">

	import GameSubmitter from '../../components/configure/GameSubmitter.svelte';
	import AddPlayer from '../../components/configure/AddPlayer.svelte';
	import { Button, Checkbox, Input, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';

	import type { Game } from '$lib/domain/games/games';
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';

	import { authenticated } from '$lib/auth';
	import httpClient from '$lib/httpClient';

	let adminPassword = '';
	const authenticateAdmin = async () => {
		const result = await httpClient.post('/api/authenticate/', null, { headers: { 'admin_password': adminPassword }});
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

	<div class="m-3 mt-10 overflow-x w-full sm:w-fit">
		<Table>
			<TableHead>
				<TableHeadCell>Date</TableHeadCell>
				<TableHeadCell>Winner</TableHeadCell>
				<TableHeadCell>Loser</TableHeadCell>
				<TableHeadCell>Draw</TableHeadCell>
			</TableHead>
			<TableBody>
				{#each games.sort(( a, b ) => b.gameId - a.gameId) as game}
					<TableBodyRow>
						<TableBodyCell>{game.datePlayed.toLocaleDateString('en-GB')}</TableBodyCell>
						<TableBodyCell>{game.winnerUsername} {Math.floor(game.winnerRating)} (<span class="text-green-600">{formatRatingChange(game.winnerRatingChange)}</span>)</TableBodyCell>
						<TableBodyCell>{game.loserUsername} {Math.floor(game.loserRating)} (<span class="text-red-600">{formatRatingChange(game.loserRatingChange)}</span>)</TableBodyCell>
						<TableHeadCell>
							<Checkbox disabled checked={game.draw}/>
						</TableHeadCell>
					</TableBodyRow>
				{/each}
			</TableBody>
			</Table>
	</div>
</div>
