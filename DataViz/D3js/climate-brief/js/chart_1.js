function showChart1() {

    //Clean the chart area before draw a new chart
    const container = document.getElementById('chart');
    container.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "Greenhouse Emissions Evolution in  20 Years";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "With the Line Chart we seek to compare the total\
    greenhouse gases emission among OECD countries over a span of 30 years. We observe that the comparison is hard \
    because of the magnitude difference between countries, actually for this chart United States was left out \
    because the outstanding difference with the rest of the countries. Alternatives to overcome this could be to \
    change the scale to a logarithmic one, or create a subgroup of countries to analyze. The good thing is our \
    hypothesis seems to be right, countries in the Europe Union, with more progressive environmental policies \
    have decreased the overall greenhouse gases emissions.";

    //Making visible the texts chart 1
    const box = document.getElementById('texts');
    box.style.display = 'block';

    const height = 1200,
    width = 600,
    margin = ({ top: 20, right: 50, bottom: 40, left: 60 });

    const svg = d3.select("#chart")
        .append("svg")
        .attr("viewBox", [0, 0, width, height]);

    d3.csv("data/totalGHG.csv").then(data => {
        let countries = new Set(); 
        
        for (let d of data) {
            d.Year = +d.Year;
            d.Value = +d.Value;
            countries.add(d.Country); // push unique values to Set
        }
        
        let x = d3.scaleLinear()
            .domain(d3.extent(data, d => d.Year))
            .range([margin.left, width - margin.right]);
        
        let y = d3.scaleLinear()
            .domain(d3.extent(data, d => d.Value)).nice() // using extent because values are less than 0
            .range([height - margin.bottom, margin.top]);
        
        // Y Axis first
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .attr("class", "y-axis")
            .call(d3.axisLeft(y)
            .tickSize(-innerWidth)
            //.tickFormat(d => d + "%")
            );
        
        // X Axis second because we want it to be placed on top
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.top})`)
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

            //console.log(countryData)
            //console.log(country)
        
            let g = svg.append("g")
            .attr("class", "country")
            .on('mouseover', function () {
                // set/remove highlight class
                // highlight class defined in html
                d3.selectAll(".highlight").classed("highlight", false);
                d3.select(this).classed("highlight", true);
            });
        
            // USA selected in blue on load of page
            if (country === "United States") {
            g.classed("highlight", true);
            }
        
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
    }