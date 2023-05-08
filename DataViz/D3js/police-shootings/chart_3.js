function showChart3() {
    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "Black People is Over-Represented";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "When we look at the total of death people\
    by race, by using a ring chart, we can observe that the three races with more representation in this\
    statistics are White, Black, and Hispanic People. But when we compare that representation with the\
    overall racial diversity in the Unites States, we can observe that Black people is over-represented.\
    According to 2020 U.S. Census, 12.1% of the population identifies as Black or African American, but\
    this percentage increases to 24.8% when it comes to the people killed by the police, the actual double.\
    The Native American people is also over-represented to the double in this numbers, according to the\
    U.S. census data but the actual number stills considerable low in comparison with other races. Here\
    it is worth asking why this great difference in black people and how these numbers are still tied to\
    the remaining racism in American society. But that is not the only concern";

    //Making invisible the month select box for chart 1
    const box = document.getElementById('texts');
    box.style.display = 'block';

    const height = 400,
    width = 600;
    margin = ({ top: 20, right: 10, bottom: 20, left: 10 });

    const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("style", "max-width: 100%; height: auto; height: intrinsic;");


    d3.csv('total_deaths_by_race.csv').then((data) => {

        for (let d of data) {
            d.Deaths = +d.Deaths;
        }

        innerRadius = 80;
        outerRadius = 145;
        labelRadius = 160;

        
        const arcs = d3.pie().sort(null).value(d => d.Deaths)(data);
        const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
        const arcLabel = d3.arc().innerRadius(labelRadius).outerRadius(labelRadius);

        colors_chart = ['#817F82','#AE8CA3','#A2ABB5', '#95D9DA', '#976391', '#48639C'];

        svg.append("g")
            .attr("stroke", "white")
            .attr("stroke-width", 2)
            .attr("stroke-linejoin", "round")
            .selectAll("path")
            .data(arcs)
            .join("path")
            .attr("fill", (d, i) => colors_chart[i])
            .attr("d", arc);
        
        svg.append("g")
            //.attr("font-size", 20)
            .attr("text-anchor", "middle")
            .selectAll("text")
            .data(arcs)
            .join("text")
            .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
            .selectAll("tspan")
            .data(d => {
            return [d.data.Race, d.data.Deaths + '%'];
            })
            .join("tspan")
            .attr("x", 0)
            .attr("y", (d, i) => `${i * 1.0}em`)
            .attr("font-weight", 800)
            .attr("font-size", 12)
            .text(d => d);
        
        svg.append("text")
            .attr("font-weight", "bold")
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .text("2015")
            .style("font-size", 50);
        });
}