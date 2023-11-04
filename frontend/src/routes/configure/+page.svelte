<script lang="ts">
	import GamePlayerSelector from '../../components/GamePlayerSelector.svelte';

	let newPlayerName = '';
</script>

<div class="flex flex-col items-center justify-center h-auto w-auto pt-10 pb-20 px-2">
	<div class="text-center pt-7 pb-5 px-2 text-3xl font-bold">Add player</div>

	<!-- put the button and text area in line -->
	<div class="flex">
		<textarea bind:value={newPlayerName} />
		<button class="btn bg-white ml-2">Add</button>
	</div>

	<GamePlayerSelector />
</div>
