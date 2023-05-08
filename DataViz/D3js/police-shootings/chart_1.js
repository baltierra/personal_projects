function showChart1() {

    //Clean the chart area before draw a new chart
    const container = document.getElementById('chart');
    container.textContent = '';

    document.getElementById("title_chart").innerHTML = "";
    document.getElementById("title_chart").innerHTML = "General Total and Total by Race";
    document.getElementById("description_chart").innerHTML = "";
    document.getElementById("description_chart").innerHTML = "In this chart we can observe the monthly total\
    of people shot and killed by police officers during 2015. At the same time we can see how that total\
    disaggregate by race. First thing we can observe is that the total fluctuated between 100 and 160 people\
    per month exhibiting two spikes, in March and July, but those fluctuations are hard to explain with the\
    available data and they are hardly attributable to some seasonal effect. But what we can observe is that\
    the general curve seems to be similar in shape to the curve that describes White people. Another thing\
    we can observe, in terms of race, is that Asians and Native Americans are the races that keeps the lowest\
    record. But let's dive into the racial factor in the next chart.";

    //Making invisible the month select box for chart 1
    const box = document.getElementById('texts');
    box.style.display = 'block';

    const height = 400,
    width = 600,
    margin = ({ top: 20, right: 50, bottom: 40, left: 25 });

    const svg = d3.select("#chart")
        .append("svg")
        .attr("viewBox", [0, 0, width, height]);

    d3.csv("deaths_months_total.csv").then(data => {
        let timeParse = d3.timeParse("%Y-%m");
        let races = new Set(); 
        
        for (let d of data) {
            d.month = timeParse(d.month);
            d.amount = +d.amount;
            races.add(d.race); // push unique values to Set
        }
        
        let x = d3.scaleTime()
            .domain(d3.extent(data, d => d.month))
            .range([margin.left, width - margin.right]);
        
        let y = d3.scaleLinear()
            .domain(d3.extent(data, d => d.amount)).nice() // using extent because values are less than 0
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
            .tickFormat(d3.timeFormat("%b"))
            );
        
        let line = d3.line()
            .x(d => x(d.month))
            .y(d => y(d.amount))
            .curve(d3.curveNatural);
        

        // looping through set
        for (let race of races) { 
            //.filter filters data in D3
            let raceData = data.filter(d => d.race === race);

            console.log(raceData)
            //console.log(race)
        
            let g = svg.append("g")
            .attr("class", "race")
            .on('mouseover', function () {
                // set/remove highlight class
                // highlight class defined in html
                d3.selectAll(".highlight").classed("highlight", false);
                d3.select(this).classed("highlight", true);
            });
        
            // USA selected in blue on load of page
            if (race === "Total") {
            g.classed("highlight", true);
            }
        
            g.append("path")
            .datum(raceData) // datum is a single result from data
            .attr("fill", "none")
            .attr("stroke", "#ccc")
            .attr("d", line)
        
            // find position of last piece to position end of line labels
            let lastEntry = raceData[raceData.length - 1];
        
            g.append("text")
            .text(race)
            .attr("x", x(lastEntry.month))
            .attr("y", y(lastEntry.amount))
            .attr("dx", "5px") // shifting attribute in svg
            .attr("dominant-baseline", "middle")
            .attr("fill", "#999");
        }
        
        });
    }