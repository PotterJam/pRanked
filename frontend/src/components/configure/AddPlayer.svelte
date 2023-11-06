<script lang="ts">
    import { getPlayerFromReponse, type Player, type PlayerResponse } from '$lib/domain/player/player';

    import httpClient, { isAxiosError } from '$lib/httpClient';

    import redx from '$lib/assets/red-x.svg';
    import greenCheck from '$lib/assets/green-check.svg';
    import { Input, Button, P } from 'flowbite-svelte'

    export let playerNames: string[] = [];
    export let players: Player[] = [];
    
    let newPlayerNameInput = '';
    $: newPlayerName = newPlayerNameInput.trim();

    let addPlayerFailed = false;
    let addPlayerSuccess = false;
    let addPlayerDisabled = false;

    const addPlayer = async () => {
        const failed = () => {
            addPlayerFailed = true;
            addPlayerDisabled = true;
            setTimeout(() => {
                addPlayerFailed = false;
                addPlayerDisabled = false;
            }, 500);
        };

        // new player name should be all alphanumeric characters, with max one space in between, and have a length of at least 2
        const validNewPlayerNameRegex = /^[a-zA-Z0-9]+( [a-zA-Z0-9]+)?$/;
        const newPlayerNameValid = validNewPlayerNameRegex.test(newPlayerName)
            && newPlayerName.length > 1
            && !playerNames.includes(newPlayerName);

        if (newPlayerNameValid) {
            try {
                const res = await httpClient.put<PlayerResponse>('/players/' + newPlayerName);
                const newPlayer = getPlayerFromReponse(res.data);
                
                addPlayerDisabled = true;
                addPlayerSuccess = true;

                players = [...players, newPlayer];
        
                setTimeout(() => {
                    addPlayerSuccess = false;
                    addPlayerDisabled = false;
                    newPlayerName = '';
                }, 500);
            } catch (error) {
                if (isAxiosError<PlayerResponse>(error)) {
                    if (error.response?.status === 409) alert('Player already exists');
                    failed();
                }
            }
        } else {
            failed();
        }
    };
</script>

<div class="text-center pt-7 pb-5 px-2 text-3xl font-bold">Add player</div>
<div class="flex h-10">
    <Input disabled={addPlayerDisabled} placeholder="Player name..." rows="1" bind:value={newPlayerNameInput} />
    {#if !addPlayerFailed && !addPlayerFailed && !addPlayerDisabled}
        <Button color="light" on:click={addPlayer} class="ml-2">Add</Button>
    {:else}
    <div class="flex justify-center h-10 w-16 mx-4 ml-5">
        {#if addPlayerFailed}
            <img src={redx} class="h-10 w-10" alt="Cross icon" />
        {:else if addPlayerSuccess}
            <img src={greenCheck} class="h-10 w-10" alt="Check mark" />
        {/if}
    </div>
    {/if}
</div>