<script lang="ts">
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';
	import httpClient, { isAxiosError } from '$lib/httpClient';

	import redx from '$lib/assets/red-x.svg';
	import greenCheck from '$lib/assets/green-check.svg';

	import GamePlayerSelector from '../../components/GamePlayerSelector.svelte';
	import { GetPlayerFromReponse, type PlayerResponse } from '$lib/domain/player/player';

	export let data: ConfigureLoadData;
	const players = data.players;
	$: playerNames = new Set(players.map((p) => p.username));

	let newPlayerName = '';

	let addPlayerFailed = false;
	let addPlayerSuccess = false;
	let addPlayerDisabled = false;

	const addPlayer = async () => {
		const failed = () => {
			addPlayerFailed = true;
			addPlayerDisabled = true;
			setTimeout(() => {
				addPlayerFailed = false;
				addPlayerDisabled = false;
			}, 1000);
		};

		if (newPlayerName.length > 1 && !playerNames.has(newPlayerName)) {
			try {
				const res = await httpClient.put<PlayerResponse>('/players/' + newPlayerName);
				const newPlayer = GetPlayerFromReponse(res.data);
				
				addPlayerDisabled = true;
				addPlayerSuccess = true;

				players.push(newPlayer);
		
				setTimeout(() => {
					addPlayerSuccess = false;
					addPlayerDisabled = false;
					newPlayerName = '';
				}, 1000);
			} catch (error) {
				if (isAxiosError<PlayerResponse>(error)) {
					if (error.response?.status === 409) alert('Player already exists');
					failed();
				}
			}
		} else {
			failed();
		}
	};
</script>

<div class="flex flex-col items-center justify-center h-auto w-auto pt-10 pb-20 px-2">
	<div class="text-center pt-7 pb-5 px-2 text-3xl font-bold">Add player</div>
	<div class="flex">
		<textarea disabled={addPlayerDisabled} bind:value={newPlayerName} />
		{#if !addPlayerFailed && !addPlayerFailed && !addPlayerDisabled}
			<button on:click={addPlayer} class="h-12 w-16 btn bg-white ml-2">Add</button>
		{:else}
			<div class="flex items-center justify-center h-12 w-18 mx-4">
				{#if addPlayerFailed}
					<img src={redx} class="h-10 w-10" alt="Cross icon" />
				{:else if addPlayerSuccess}
					<img src={greenCheck} class="h-10 w-10" alt="Check mark" />
				{/if}
			</div>
		{/if}
	</div>

	<GamePlayerSelector />
</div>
