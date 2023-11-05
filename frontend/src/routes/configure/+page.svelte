<script lang="ts">

	import GameSubmitter from '../../components/configure/GameSubmitter.svelte';
	import AddPlayer from '../../components/configure/AddPlayer.svelte';
	import type { Game } from '$lib/domain/games/games';
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';

    export let data: ConfigureLoadData;
    let players = data.players;
    $: playerNames = players.map((p) => p.username);

	let games: Game[] = data.games;
</script>

<div class="flex flex-col items-center justify-center h-auto w-auto pt-10 pb-20 px-2">
	<AddPlayer playerNames={playerNames} bind:players={players}/>

	<GameSubmitter players={players} bind:games={games}/>

	<div class="m-5 mt-10">
		{JSON.stringify(games)}
	</div>
</div>
