<script lang="ts">
	import GamePlayerSelector from './GamePlayerSelector.svelte';

	let showInitialMenu = true;
	let showDrawMenu = false;
	let showWinLossMenu = false;

	const toggleDrawMenu = () => {
		showInitialMenu = false;
		showDrawMenu = true;
		showWinLossMenu = false;
	};

	const toggleWinLossMenu = () => {
		showInitialMenu = false;
		showDrawMenu = false;
		showWinLossMenu = true;
	};

	const submitDraw = () => {
		return 1;
	};

	const submitWinLoss = () => {
		return 1;
	};
</script>

<div class="flex items-center justify-center h-screen w-auto">
	{#if showInitialMenu}
		<div class="text-center flex flex-col justify-center">
			<p class="text-3xl font-bold pb-3">Draw?</p>
			<div class="flex flex-row flex-wrap justify-center">
				<button class="btn bg-green-300 w-32 h-16 m-3 mb-0" on:click={toggleDrawMenu}>Yes</button>
				<button class="btn bg-red-300 w-32 h-16 m-3" on:click={toggleWinLossMenu}>No</button>
			</div>
		</div>
	{:else if showDrawMenu}
		<GamePlayerSelector player1Label="Player 1" player2Label="Player 2" submitGame={submitDraw} />
	{:else if showWinLossMenu}
		<GamePlayerSelector player1Label="Winner" player2Label="Loser" submitGame={submitWinLoss} />
	{/if}
</div>
