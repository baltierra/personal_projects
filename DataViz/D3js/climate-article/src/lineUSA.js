const height_4 = 600,
width_4 = 900,
margin_4 = ({ top: 20, right: 85, bottom: 40, left: 70 });

const svg_4 = d3.select("#lineUSA")
    .append("svg")
    .attr("viewBox", [0, 0, width_4, height_4]);

d3.csv("./data/totalGHGUSA.csv").then(data => {
    let countries = new Set(); 
    
    for (let d of data) {
        d.Year = +d.Year;
        d.Value = +d.Value;
        countries.add(d.Country); // push unique values to Set
    }
    
    let x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.Year))
        .range([margin_4.left, width_4 - margin_4.right]);
    
    let y = d3.scaleLinear()
        .domain(d3.extent(data, d => d.Value))
        .range([height_4 - margin_4.bottom, margin_4.top]);
    
    // Y Axis first
    svg_4.append("g")
        .attr("transform", `translate(${margin_4.left},0)`)
        .attr("class", "y-axis")
        .call(d3.axisLeft(y)
        .tickSize(-innerWidth)
        );
    
    // X Axis second because we want it to be placed on top
    svg_4.append("g")
        .attr("transform", `translate(0,${height_4 - margin_4.top})`)
        .call(d3.axisBottom(x)
        .tickSizeOuter(0)
        .tickSizeInner(0)
        .tickFormat(d => d)
        );
    
    let line = d3.line()
        .x(d => x(d.Year))
        .y(d => y(d.Value))
        .curve(d3.curveNatural);
    

    // looping through set
    for (let country of countries) { 
        //.filter filters data in D3
        let countryData = data.filter(d => d.Country === country);
    
        let g = svg_4.append("g")
        .attr("class", "country")
        .on('mouseover', function () {
            // set/remove highlight class
            // highlight class defined in html
            d3.selectAll(".highlight").classed("highlight", false);
            d3.select(this).classed("highlight", true);
        });

        //Add a label for the Y axis
        svg_4.append("text")
        .attr("class", "y-label")
        .attr("text-anchor", "end")
        .attr("x", -margin_4.top / 2)
        .attr("dx", "-0.5em")
        .attr("y", 10)
        .attr("transform", "rotate(-90)")
        .text("GHG Emissions (thousands of tonnes)");

        //Add a label for the X axis
        svg_4.append("text")
            .attr("class", "x-label")
            .attr("text-anchor", "end")
            .attr("x", width_4 - margin_4.right)
            .attr("y", height_4)
            .attr("dx", "0.5em")
            .attr("dy", "0.0em") 
            .attr("font-weight", 700)
            .text("YEAR");
    
    
        g.append("path")
        .datum(countryData) // datum is a single result from data
        .attr("fill", "none")
        .attr("stroke", "#ccc")
        .attr("d", line)
    
        // find position of last piece to position end of line labels
        let lastEntry = countryData[countryData.length - 1];
    
        g.append("text")
        .text(country)
        .attr("x", x(lastEntry.Year))
        .attr("y", y(lastEntry.Value))
        .attr("dx", "5px") // shifting attribute in svg
        .attr("dominant-baseline", "middle")
        .attr("fill", "#999");
    }
    
    });