<script>
  import "../app.css";
	import Nav from "../components/nav.svelte";
</script>

<Nav></Nav>

<slot />

<style lang="postcss">
  :global(body) {
    @apply bg-darkcream pl-5 pr-5 pb-5;
  }
</style>
