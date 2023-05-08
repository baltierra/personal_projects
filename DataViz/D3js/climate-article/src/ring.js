const height_1 = 600,
width_1 = 900,
margin_1 = ({ top: 20, right: 10, bottom: 20, left: 10 });

const svg_1 = d3.select("#ring")
.append("svg")
.attr("width", width_1)
.attr("height", height_1)
.attr("viewBox", [-width_1 / 2, -height_1 / 2, width_1, height_1])
.attr("style", "max-width: 100%; height: auto; height: intrinsic;");


d3.csv('./data/total_perc.csv').then((data) => {

    for (let d of data) {
        d.Total = +d.Total;
    }

    innerRadius = 80;
    outerRadius = 145;
    labelRadius = 160;

    
    const arcs = d3.pie().sort(null).value(d => d.Total)(data);
    const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
    const arcLabel = d3.arc().innerRadius(labelRadius).outerRadius(labelRadius);

    colors_chart = ['#817F82','#AE8CA3','#A2ABB5', '#95D9DA', '#976391', '#48639C'];

    svg_1.append("g")
        .attr("stroke", "white")
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .selectAll("path")
        .data(arcs)
        .join("path")
        .attr("fill", (d, i) => colors_chart[i])
        .attr("d", arc);
    
    svg_1.append("g")
        //.attr("font-size", 20)
        .attr("text-anchor", "middle")
        .selectAll("text")
        .data(arcs)
        .join("text")
        .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
        .selectAll("tspan")
        .data(d => {
        return [d.data.Country, d.data.Total + '%'];
        })
        .join("tspan")
        .attr("x", 0)
        .attr("y", (d, i) => `${i * 1.0}em`)
        .attr("font-size", 18)
        .attr("font-weight", 800)
        .text(d => d);
    
    svg_1.append("text")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .attr("dy", "-1em")
        .attr("alignment-baseline", "middle")
        .text("Total GHG")
        .style("font-size", 20);

    svg_1.append("text")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .attr("dy", "0em")
        .attr("alignment-baseline", "middle")
        .text("Emissions")
        .style("font-size", 20);

    svg_1.append("text")
        .attr("font-weight", "bold")
        .attr("text-anchor", "middle")
        .attr("dy", "1em")
        .attr("alignment-baseline", "middle")
        .text("Last 30 Years")
        .style("font-size", 20);
    });