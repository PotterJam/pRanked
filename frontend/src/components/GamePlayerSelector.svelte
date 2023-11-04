<script lang="ts">
	import { slide } from 'svelte/transition';

    export let player1Label: string;
    export let player2Label: string;
    export let submitGame: (player1: string, player2: string) => number;

	let selectedPlayer1 = '';
	let selectedPlayer2 = '';
</script>

<div class="flex flex-col w-auto justify-end">
	<div class="text-center" transition:slide>
		<label class="inline-block w-20 text-lg font-bold" for="{player1Label}">{player1Label}</label>
		<select class="" id="{player1Label}" name="{player1Label}" bind:value={selectedPlayer1}>
			<option value="volvo">Volvo</option>
		</select>
	</div>
	{#if selectedPlayer1 != ''}
		<div class="text-center" transition:slide>
			<label class="inline-block w-20 text-lg font-bold" for="{player2Label}">{player2Label}</label>
			<select class="" id="{player2Label}" name="{player2Label}" bind:value={selectedPlayer2}>
				<option value="saab">Saaaaab</option>
			</select>
		</div>
	{/if}
	{#if selectedPlayer2 != ''}
		<div class="text-center" transition:slide>
			<button class="btn ml-auto bg-green-300 w-42 h-14 m-5 mt-3" on:click={submitGame(selectedPlayer1, selectedPlayer2)}>Submit</button>
		</div>
	{/if}
</div>

<style lang="postcss">
	select {
		@apply w-64 min-w-max m-2;
	}
</style>