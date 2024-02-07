<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";

    let data = [];

    onMount(async () => {
        data = await d3.csv("data.csv");
    });
</script>

{#if data.length > 0}
    <table>
        <thead>
            <tr>
                {#each Object.keys(data[0]) as header}
                    <th>{header}</th>
                {/each}
            </tr>
        </thead>
        <tbody>
            {#each data as row}
                <tr>
                    {#each Object.values(row) as value}
                        <td>{value}</td>
                    {/each}
                </tr>
            {/each}
        </tbody>
    </table>
{:else}
    <p>Loading...</p>
{/if}
