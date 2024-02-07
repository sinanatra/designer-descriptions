<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { load } from "@tensorflow-models/universal-sentence-encoder";
    import { UMAP } from "umap-js";

    let data = [];
    let wordClusters = [];

    onMount(async () => {
        data = await d3.csv("data.csv");

        const model = await load();
        const embeddings = await model.embed(data.map((d) => d.text));
        const embeddingsArray = embeddings.arraySync();
        const textWithEmbeddings = data.map((d, i) => ({
            text: d.text,
            url: d.url,
            embedding: embeddingsArray[i],
        }));

        const umap = new UMAP();
        const umapData = umap.fit(
            textWithEmbeddings.map((item) => item.embedding),
        );

        // Normalize UMAP data to fit within the container
        const normalizedUmapData = umapData.map((pos) => [
            ((pos[0] - Math.min(...umapData.map((p) => p[0]))) /
                (Math.max(...umapData.map((p) => p[0])) -
                    Math.min(...umapData.map((p) => p[0])))) *
                100,
            ((pos[1] - Math.min(...umapData.map((p) => p[1]))) /
                (Math.max(...umapData.map((p) => p[1])) -
                    Math.min(...umapData.map((p) => p[1])))) *
                100,
        ]);

        wordClusters = textWithEmbeddings
            .map((item, index) => ({
                text: item.text,
                url: item.url,
                position: normalizedUmapData[index],
            }))
            .sort((a, b) => {
                if (a.position[1] !== b.position[1]) {
                    return a.position[1] - b.position[1]; // sort vertical
                }
                return a.position[0] - b.position[0]; // If vertical positions are the same, sort by horizontal position
            });

        console.log(wordClusters);
    });
</script>

<section class="umap-container">
    {#if wordClusters.length > 0}
        {#each wordClusters as { text, url, position }}
            <div
                class="umap-point"
                style="left: {position[0]}%; top: {position[1]}%;"
            >
                <a href={url} target="_blank">
                    {text}
                </a>
            </div>
        {/each}
    {:else}
        <p>Loading...</p>
    {/if}
</section>

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

    .umap-container {
        font-family: sans-serif;
        position: relative;
        width: 100vw;
        height: 100vh;
        padding: 10px;
        font-size: 14px;
    }

    .umap-point {
        position: relative;
    }

    a {
        background: linear-gradient(to right, blue, gainsboro, purple);
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        text-decoration: unset;
    }
</style>
