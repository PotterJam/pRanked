
<script>
    import leaderboard from '$lib/assets/leaderboard.svg'
    import graph from '$lib/assets/graph.svg'
    import cog from '$lib/assets/cog.svg'
</script>

<div class="flex flex-row justify-center h-20 w-auto">
    <a href="/" class="flex justify-center navbut mr-5 sm:mr-10">
        <button on:click={() => {}}>
            <img src={leaderboard} class="h-12 w-12" alt="Leaderboard icon" />
        </button>
    </a>
    <a href="/graphs" class="flex justify-center navbut mr-5 sm:mr-10">
        <button on:click={() => {}}>
            <img src={graph} class="h-12 w-12" alt="Graph icon" />
        </button>
    </a>
    <a href="/configure" class="flex justify-center navbut">
        <button on:click={() => {}}>
            <img src={cog} class="h-12 w-12" alt="Settings icon" />
        </button>
    </a>
</div>


<style lang="postcss">
    .navbut {
        @apply bg-navbut w-60 rounded-b border-l border-r border-b-4 border-black
    }
</style>
