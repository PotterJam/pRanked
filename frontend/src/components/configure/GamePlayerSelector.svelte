<script lang="ts">
	import { fade, slide, scale } from 'svelte/transition';
	import check from '$lib/assets/check-lg.svg';
	import resetArrow from '$lib/assets/arrow-counterclockwise.svg';
	import Spinny from '../spinny.svelte';
	import type { Player } from '$lib/domain/player/player';
	import { getGameResultFromResponse, type Game } from '$lib/domain/games/games';
	import httpClient from '$lib/httpClient';

	export let players: Player[] = [];
	export let playerNames: string[] = [];
	export let games: Game[] = [];

	let onSubmit = false;
	let complete = false;

	let submitGame = async (winner: string, loser: string, draw: boolean) => {
		const winningPlayer = players.find(x => x.username === winner);
		const losingPlayer = players.find(x => x.username === loser);

		if (!winningPlayer || !losingPlayer) {
			throw new Error('Could not find players that you selected');
		}

		onSubmit = true;
		const submitGameResp = await httpClient.post('/games/submit', {
			winner_id: winningPlayer.playerId,
			loser_id: losingPlayer.playerId,
			draw: draw
		}, {
			headers: {
				'Content-Type': 'application/json'
			}
		});

		const newGameResult = getGameResultFromResponse(submitGameResp.data);

		const newGame: Game = {
			gameId: newGameResult.gameId,
			draw: draw,
			winnerId: winningPlayer.playerId,
			winnerUsername: winningPlayer.username,
			winnerRating: newGameResult.oldWinnerRating,
			loserId: losingPlayer.playerId,
			loserUsername: losingPlayer.username,
			loserRating: newGameResult.oldLoserRating,
		};

		games = [...games, newGame];

		complete = true;
	};

	let selectedPlayer1 = '';
	let selectedPlayer2 = '';
	let draw = false;

	const topWon = () => {
		submitGame(selectedPlayer1, selectedPlayer2, draw);
	};

	const bottomWon = () => {
		submitGame(selectedPlayer2, selectedPlayer1, draw);
	};

	const wasDraw = () => {
		draw = true;
		submitGame(selectedPlayer1, selectedPlayer2, draw);
	};

	const again = () => {
		complete = false;
		onSubmit = false;
		selectedPlayer1 = '';
		selectedPlayer2 = '';
		draw = false;
	};

	let headerText = 'Record a game';

	$: if (selectedPlayer1 != '' && selectedPlayer2 != '' && !onSubmit) {
		headerText = "Who's won?";
	} else {
		headerText = 'Record a game';
	}
</script>

<div class="text-center pt-14 px-2 text-3xl font-bold pb-3">{headerText}</div>
<div class="flex flex-col w-auto justify-end p-1">
	{#if complete}
		<div class="p-10 flex pb-7" in:scale>
			<img src={check} class="m-auto h-26 w-12" alt="Check mark" />
		</div>
		<button in:slide={{ delay: 700 }} class="btn text-xl bg-stone-100 w-32 h-12 mb-0 mx-3 mt-2" on:click={again}> Again? </button>
	{:else if onSubmit}
		<div class="p-10 flex" in:fade={{ delay: 700 }}><Spinny /></div>
	{:else if selectedPlayer1 == '' || selectedPlayer2 == ''}
		<select in:slide bind:value={selectedPlayer1}>
			<option value="" disabled selected hidden>Choose player 1...</option>
			{#each playerNames as playerName}
				<option value={playerName}>{playerName}</option>
			{/each}
		</select>
		<select in:slide bind:value={selectedPlayer2}>
			<option value="" disabled selected hidden>Choose player 2...</option>
			{#each playerNames.filter(name => name != selectedPlayer1) as playerName}
				<option value={playerName}>{playerName}</option>
			{/each}
		</select>
	{:else}
		<button class="btn bg-cyan-50 text-xl w-60 h-12 m-2" on:click={topWon}>{selectedPlayer1}</button>
		<button class="btn bg-cyan-50 text-xl w-60 h-12 m-2 mt-2" on:click={bottomWon}>{selectedPlayer2}</button>

		<div class="mb-5 text-center flex flex-col justify-center">
			<div class="flex items-center justify-center">
				<div class="flex-1" />
				<button class="flex-1 btn text-xl bg-stone-100 w-32 h-12 mb-0 mx-3 mt-2" on:click={wasDraw}> Draw</button>
				<button class="flex-1 self-end" on:click={again}>
					<img class="float-right h-7 w-7 mr-2 mb-1" src={resetArrow} alt="Reset icon" />
				</button>
			</div>
		</div>
	{/if}
</div>

<style lang="postcss">
	select {
		@apply w-64 min-w-max m-2;
	}
</style>
