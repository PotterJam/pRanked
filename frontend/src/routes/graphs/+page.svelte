<script lang="ts">
    import type { GraphsLoadData } from '$lib/domain/routeLoadReturns';
    export let data: GraphsLoadData;

    import { onDestroy, onMount } from 'svelte';
    import Chart, { type ChartConfiguration } from 'chart.js/auto';
    import { Colors } from 'chart.js';

    Chart.register(Colors);
    
    let portfolio: HTMLCanvasElement;
    let myChart: Chart<'line'>;

    const graphData = {
          labels: ['Expenses', 'Savings', 'Investments'],
          datasets: [{
            label: 'My First Dataset',
            data: [1, 2, 3],
            fill: false,
            tension: 0.1
        },
        {
            label: 'My First Dataset',
            data: [2,3,1],
            fill: false,
            tension: 0.1
        }]
      };
      
    const config: ChartConfiguration<'line'> = {
        type: 'line',
        data: graphData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
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
