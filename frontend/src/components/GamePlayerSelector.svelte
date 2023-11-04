<script lang="ts">
	import check from '$lib/assets/check-lg.svg'
	import Spinny from './spinny.svelte';

	import { fade, slide, scale } from 'svelte/transition';

	let onSubmit = false;
	let complete = false;

    let submitGame: (winner: string, loser: string, draw: boolean) => number = () => {
        onSubmit = true;
        setTimeout(() => {
            complete = true;
        }, 2000);
		return 1;
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

</script>

<div class="flex flex-col w-auto justify-end p-5">
	{#if complete}
	<div class="p-10 flex" in:scale><img src={check} class="m-auto h-12 w-12" alt="Check mark" /></div>
	<button in:slide={{delay: 700}} class="btn text-xl bg-stone-100 w-32 h-12 mb-0 mx-3 mt-2" on:click={again}>Again?</button>
	{:else if onSubmit}
		<div class="p-10 flex" in:fade><Spinny /></div>
	{:else if selectedPlayer1 == '' || selectedPlayer2 == ''}
	<select in:slide bind:value={selectedPlayer1}>
		<option value="" disabled selected hidden>Choose player 1...</option>
		<option value="volvo">Volvo</option>
	</select>
	<select in:slide bind:value={selectedPlayer2}>
		<option value="" disabled selected hidden>Choose player 2...</option>
		<option value="busa">Busa</option>
	</select>
	{:else}
		<div class="text-center text-2xl p-5 pt-3 font-medium">Who won?</div>
		<button in:slide class="btn bg-cyan-50 text-xl w-60 h-14 m-3" on:click={topWon}>{selectedPlayer1}</button>
		<button in:slide class="btn bg-cyan-50 text-xl w-60 h-14 m-3 mt-2" on:click={bottomWon}>{selectedPlayer2}</button>

		<div class="mb-5 text-center flex flex-col justify-center">
			<div class="flex flex-row flex-wrap justify-center">
				<button class="btn text-xl bg-stone-100 w-32 h-12 mb-0 mx-3 mt-2" on:click={wasDraw}>Draw</button>
			</div>
		</div>	
	{/if}
</div>

<style lang="postcss">
	select {
		@apply w-64 min-w-max m-2;
	}
</style>