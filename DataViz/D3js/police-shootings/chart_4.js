function showChart4() {
    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "Not Only Racism Could Be an Issue";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "Analyzing the available data,\
    it is impossible to overlook an important fact: 21.3% of the people shot dead by the police\
    were diagnosed with a mental illness. This raises more questions than the existing data can\
    answer, but it is key to ask how the mental health of the general population is a trigger for\
    risky behaviors that lead to acts of violence and crime. But it is also worth asking, in view\
    of what has been observed in all the graphs shown, how is the mental health of those who exercise\
    the role of law enforcement in our society.";

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


    d3.csv('total_deaths_by_mental.csv').then((data) => {

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
            return [d.data.Mental, d.data.Deaths + '%'];
            })
            .join("tspan")
            .attr("x", 0)
            .attr("y", (d, i) => `${i * 1.0}em`)
            .attr("font-size", 18)
            .attr("font-weight", 800)
            .text(d => d);
        
        svg.append("text")
            .attr("font-weight", "bold")
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .text("2015")
            .style("font-size", 50);
        });
}