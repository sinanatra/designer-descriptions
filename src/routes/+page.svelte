<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import Umap from "../components/Umap.svelte";
    let data = [];
    let umap = [];
    $: searchTerm = "";

    onMount(async () => {
        data = await d3.csv("data.csv");
        umap = await d3.json("umap.json");
        data.filter((d) => d.url.length > 0).sort((a, b) =>
            a.text.localeCompare(b.text),
        );
    });

    $: sorted = data.filter((item) =>
        item.text.toLowerCase().includes(searchTerm.toLowerCase()),
    );
</script>

{#if data.length > 0}
    {#if umap.length > 0}
        <Umap data={sorted} {umap} />
    {/if}
    <section class="container">
        <input bind:value={searchTerm} placeholder="Search..." />
        {#each sorted as { text, url, x, y }}
            <div class="point">
                <a href={url} target="_blank">
                    {text}
                </a>
            </div>
        {/each}
    </section>
{:else}
    <p>Loading...</p>
{/if}

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        background-color: black;
        color: white;
    }

    p {
        margin: 0;
    }

    .container {
        padding-top: 2rem;
        font-family: sans-serif;
        max-width: 768px;
        margin: 0 auto;
        font-size: 24px;
    }

    input {
        margin: 5px;
        padding: 2px;
        min-height: 30px;
        width: 100%;
        border-radius: 10px;
        border-style: none;
    }

    a {
        margin: 5px;
        padding: 2px;
        display: inline-flex;
        text-decoration: unset;
        /* background: linear-gradient(to right, blue, gainsboro, purple); */
        background-color: white;
        color: black;
        /* -webkit-background-clip: text; */
        /* background-clip: text;
        text-decoration: unset; */
        border-radius: 10px;
    }
</style>
