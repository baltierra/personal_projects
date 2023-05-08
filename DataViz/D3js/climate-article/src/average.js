const height = 600, width = 900, margin = ({ top: 15, right: 30, bottom: 85, left: 80 });

const svg = d3.select("#average")
  .append("svg")
  .attr("viewBox", [0, 0, width, height]);

d3.csv('./data/totalsAndAvg.csv').then(data => {
    for (let d of data) {
    d.Average = +d.Average;
    }

    let x = d3.scaleBand()
        .domain(data.map(d => d.Country))
        .range([margin.left, width - margin.right])
        .padding(1,1);

    let y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.Average)]).nice()
        .range([height - margin.bottom, margin.top]);

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .attr("class", "y-axis")
    .call(d3.axisLeft(y)
      .tickSizeOuter(0)
    //   .tickFormat(d => d + "%")
      .tickSize(-width + margin.right + margin.left)
    );

//   svg.append("g")
//     .attr("transform", `translate(0,${height - margin.bottom})`)
//     .call(d3.axisBottom(x));

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .selectAll("text")  
    .style("text-anchor", "end")
    .attr("dx", "-.85em")
    .attr("dy", ".15em")
    .attr("transform", "rotate(-45)");


  svg.append("text")
    .attr("class", "y-label")
    .attr("text-anchor", "end")
    .attr("x", -margin.top / 2)
    .attr("dx", "-0.5em")
    .attr("y", 10)
    .attr("transform", "rotate(-90)")
    .text("GHG Emissions (thousands of tonnes)");


  let line = d3.line()
    .x(d => x(d.Country))
    .y(d => y(d.Average))
    //.curve(d3.curveNatural); // more: https://observablehq.com/@d3/d3-line#cell-244



  svg.append("path")
    .datum(data)
    .attr("d", line)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
  
});