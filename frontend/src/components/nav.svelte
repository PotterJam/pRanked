
<script>
    import leaderboard from '$lib/assets/leaderboard.svg'
    import graph from '$lib/assets/graph.svg'
    import cog from '$lib/assets/cog.svg'
</script>

<div class="flex flex-row justify-center h-20 w-auto">
    <button class="navbut mr-5 sm:mr-10"
    on:click={() => {}}>
        <img src={leaderboard} class="m-auto h-12 w-12" alt="Leaderboard icon" />
    </button>
    <button class="navbut mr-5 sm:mr-10"
    on:click={() => {}}>
        <img src={graph} class="m-auto h-12 w-12" alt="Graph icon" />
    </button>
    <button class="navbut"
            on:click={() => {}}>
        <img src={cog} class="m-auto h-12 w-12" alt="Settings icon" />
    </button>
</div>


<style lang="postcss">
    .navbut {
        @apply bg-navbut w-60 rounded-b border-l border-r border-b-4 border-black
    }
</style>
