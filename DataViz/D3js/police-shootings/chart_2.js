function showChart2() {
    // document.getElementById("test").innerHTML = "";
    // document.getElementById("test").innerHTML = "Chart 3 goes here";

    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "A More Detailed View to the Race Factor";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "Now, by using a stacked bars chart, we can have a better\
    understanding on the racial composition of the monthly deaths by shooting in the hands of the police. First thing\
    to notice is that White, Black, and Hispanic People are the more affected communities, which is in line with the\
    overall racial structure of the american society. But, how representative is this?";

    //Making invisible the month select box for chart 1
    const box = document.getElementById('texts');
    box.style.display = 'block';
    
    const height = 400,
    width = 600,
    margin = ({ top: 50, right: 20, bottom: 30, left: 20 });

    const svg = d3.select("#chart")
        .append("svg")
        .attr("viewBox", [0, 0, width, height]);

    d3.csv("total_death_by_month_race.csv").then( data => {

        let x = d3.scaleBand(data.map(d => (d.Month)),[margin.left, width - margin.right])
            .padding([0.2]);
    
        let y = d3.scaleLinear([0,160],[height - margin.bottom, margin.top]);
    
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x))
    
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y).tickSize(-width + margin.left + margin.right))
        
        //protein,carbs,fiber
        const subgroups = data.columns.slice(1);
    
        const color = d3.scaleOrdinal(subgroups,['#817F82','#AE8CA3','#A2ABB5', '#95D9DA', '#976391', '#48639C']);
        
        const stackedData = d3.stack()
            .keys(subgroups)(data);
        
        console.log(stackedData)
    
        svg.append("g")
            .selectAll("g")
            .data(stackedData)
            .join("g")
            .attr("fill", d => color(d.key))
            .selectAll("rect")
            .data(d => d)
            .join("rect")
            .attr("x", d => x(d.data.Month))
            .attr("y", d => y(d[1]))
            .attr("height", d => y(d[0]) - y(d[1]))
            .attr("width",x.bandwidth());
    
        let legendGroup = svg
            .selectAll(".legend-group")
            .data(subgroups)
            .join("g")
            .attr("class", "legend-group");
    
        legendGroup
            .append("circle")
            .attr("cx", (d, i) => (14 + (i * 90)))
            .attr("cy",17)
            .attr("r", 5)
            .attr("fill", (d, i) => color(i));
        
        legendGroup
            .append("text")
            .attr("x", (d, i) => (20 + (i * 90)))
            .attr("y",20)
            .text((d, i) => subgroups[i]);
        });
}