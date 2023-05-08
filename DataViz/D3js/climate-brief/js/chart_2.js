function showChart2() {
    // document.getElementById("test").innerHTML = "";
    // document.getElementById("test").innerHTML = "Chart 3 goes here";

    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "Composition of Greenhouse Emissions by Year";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "With the Stacked Bars we want to compare the \
    composition of the total greenhouse gases emissions for a given country, in this case we used Germany.\
     The greenhouse gases can be classified en six different subtypes";

    //Making visible the texts
    const box = document.getElementById('texts');
    box.style.display = 'block';
    
    const height = 400,
    width = 600,
    margin = ({ top: 50, right: 20, bottom: 40, left: 50 });

    const svg = d3.select("#chart")
        .append("svg")
        .attr("viewBox", [0, 0, width, height]);

    d3.csv("data/DEU_GHG_types.csv").then( data => {

        let x = d3.scaleBand(data.map(d => (d.Year)),[margin.left, width - margin.right])
            .padding([0.2]);
    
        let y = d3.scaleLinear([0,1250000],[height - margin.bottom, margin.top]);
    
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x))
            .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)");
    
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y).tickSize(-width + margin.left + margin.right));
        
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
            .attr("x", d => x(d.data.Year))
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