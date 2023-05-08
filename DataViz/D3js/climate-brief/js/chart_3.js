function showChart3() {
    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "Evolution in the Composition of Greenhouse Emissions by Country";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "With the Stacked Area we want to see how the \
    six different gases that compound the greenhouse emissions have evolved over the last 30 years for \
    a given country, in this case Germany. The final goal is to have a dropdown menu to select the country and update the chart";

    //Making visible the texts1
    const box = document.getElementById('texts');
    box.style.display = 'block';

    var margin = {top: 60, right: 175, bottom: 50, left: 60},
    width = 660 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#chart")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    d3.csv("data/DEU_GHG_types.csv").then( data => {

        var keys = data.columns.slice(1)
        // color palette
        var color = d3.scaleOrdinal()
            .domain(keys)
            .range(d3.schemeSet2);
        //stack the data?
        var stackedData = d3.stack()
            .keys(keys)
            (data)
        // Add X axis
        var x = d3.scaleLinear()
        .domain(d3.extent(data, function(d) { return d.Year; }))
        .range([ 0, width ]);
        var xAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(5).tickFormat(data => data))

        // Add X axis label:
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height+40 )
            .text("Year");

        // Add Y axis label:
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", 0)
            .attr("y", -20 )
            .text("Thousands of Tonnes")
            .attr("text-anchor", "start")

        // Add Y axis
        var y = d3.scaleLinear()
        .domain([0, 1250000])
        .range([ height, 0 ]);
        svg.append("g")
        .call(d3.axisLeft(y).ticks(5))


         // Area generator
        var area = d3.area()
        .x(function(d) { return x(d.data.Year); })
        .y0(function(d) { return y(d[0]); })
        .y1(function(d) { return y(d[1]); })

        // Create the scatter variable: where both the circles and the brush take place
        var areaChart = svg.append('g')
        .attr("clip-path", "url(#clip)")
        .selectAll("mylayers")
        .data(stackedData)
        .enter()
        .append("path")
        .attr("class", function(d) { return "myArea " + d.key })
        .style("fill", function(d) { return color(d.key); })
        .attr("d", area)



        // Add one dot in the legend for each name.
        var size = 20
        svg.selectAll("myrect")
        .data(keys)
        .enter()
        .append("rect")
            .attr("x", 475)
            .attr("y", function(d,i){ return 10 + i*(size+5)}) // 100 is where the first dot appears. 25 is the distance between dots
            .attr("width", size)
            .attr("height", size)
            .style("fill", function(d){ return color(d)})

        // Add one dot in the legend for each name.
        svg.selectAll("mylabels")
        .data(keys)
        .enter()
        .append("text")
            .attr("x", 475 + size*1.2)
            .attr("y", function(d,i){ return 10 + i*(size+5) + (size/2)}) // 100 is where the first dot appears. 25 is the distance between dots
            .style("fill", function(d){ return color(d)})
            .text(function(d){ return d})
            .attr("text-anchor", "left")
            .style("alignment-baseline", "middle")
        });
}
