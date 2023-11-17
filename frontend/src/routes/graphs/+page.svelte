<script lang="ts">
    import type { GraphsLoadData } from '$lib/domain/routeLoadReturns';
    export let data: GraphsLoadData;

    import { onDestroy, onMount } from 'svelte';
    import Chart, { type ChartConfiguration } from 'chart.js/auto';
    import { Colors } from 'chart.js';
    import 'chartjs-adapter-date-fns';

    Chart.register(Colors);
    
    let portfolio: HTMLCanvasElement;
    let myChart: Chart<'line'>;

    const dataSets = data.ratingHistoryGraphData.map((ratingHistory) => ({
            label: ratingHistory.player_name,
            data: ratingHistory.rating_history.map(({ date_played, rating }) => ({ x: date_played, y: rating })),
            fill: false,
            tension: 0.1
        }));

    const config: ChartConfiguration<'line'> = {
        type: 'line',
        data: {
            // @ts-ignore: ChartJS types are wrong
            datasets: dataSets
        },
        options: {
            spanGaps: true,
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                // x: {
                //     type: 'time',
                //     time: {
                //         unit: 'week'
                //     }
                // },
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Rating changes over time'
                }
            }
        }
    };

    onMount(()=> {
        const ctx = portfolio.getContext('2d');

        // Initialize chart using default config set
        if (ctx) {
            myChart = new Chart(ctx, config);
        }
    });

    onDestroy(() => {
        myChart.destroy();
    });

</script>

<div class="mt-10 w-4/5 sm:w-3/4 mx-auto">
    <canvas bind:this={portfolio} width={600}/>
</div>
