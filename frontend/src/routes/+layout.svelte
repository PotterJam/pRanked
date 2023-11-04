<script>
    import "../app.css";
</script>

<slot />

<style lang="postcss">
  :global(body) {
    @apply bg-darkcream pl-5 pr-5 pb-5;
  }

  :global(.btn) {
    @apply text-black font-medium py-2 px-4 rounded cursor-pointer border border-black;
  }

</style>
