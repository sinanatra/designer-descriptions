<script>
    import { onMount, afterUpdate } from "svelte";
    import * as d3 from "d3";

    export let data;
    export let umap;
    let merged = [];
    let margin = { top: 20, right: 20, bottom: 20, left: 20 };
    let width = 2000;
    let height = 700;

    function updateUmap() {
        merged = data.map((obj) => {
            const p = umap.find((d) => d.path === obj.img_path);
            return {
                ...obj,
                points: p ? p.point : "",
            };
        });

        const container = d3.select(".umap");
        // const zoomBehavior = d3
        //     .zoom()
        //     .scaleExtent([0.2, 40])
        //     .on("zoom", zoomed);

        // container.call(zoomBehavior);

        container.select(".chart").remove();

        const svg = container
            .append("svg")
            .attr("class", "chart")
            .style("width", "100%")
            .style("height", "650px");

        const layer = svg.append("g");

        const x = d3
            .scaleLinear()
            .domain(d3.extent(merged, (d) => d.points[0]))
            .nice()
            .range([margin.left, width - margin.right]);

        const y = d3
            .scaleLinear()
            .domain(d3.extent(merged, (d) => d.points[1]))
            .nice()
            .range([height - margin.bottom, margin.top]);

        const projection = merged.map((d, i) => ({
            url: d.url,
            text: d.text,
            img: d.favicon_url,
            x: x(d.points[0]),
            y: y(d.points[1]),
        }));

        const image = layer
            .selectAll("image")
            .data(projection)
            .enter()
            .append("a")
            .attr("xlink:href", (d) => d.url)
            .attr("target", "_blank")
            .append("image")
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href", (d) => d.img)
            .attr("x", (d) => d.x)
            .attr("y", (d) => d.y);

        // function zoomed(event) {
        //     const { transform } = event;
        //     image.attr("transform", transform);
        // }
    }

    onMount(() => {
        updateUmap();
    });

    afterUpdate(() => {
        updateUmap();
    });
</script>

<div class="umap"></div>
