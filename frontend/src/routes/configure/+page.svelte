<script lang="ts">
	import type { ConfigureLoadData } from '$lib/domain/routeLoadReturns';

	import GamePlayerSelector from '../../components/configure/GamePlayerSelector.svelte';
	import AddPlayer from '../../components/configure/AddPlayer.svelte';

    export let data: ConfigureLoadData;
    let players = data.players;
    $: playerNames = new Set(players.map((p) => p.username));
</script>

<div class="flex flex-col items-center justify-center h-auto w-auto pt-10 pb-20 px-2">
	<AddPlayer playerNames={playerNames} bind:players={players}/>

	<GamePlayerSelector players={players}/>
</div>
