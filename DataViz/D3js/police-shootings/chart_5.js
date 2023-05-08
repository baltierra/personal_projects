function showChart5() {

    //Clean the chart area before draw a new chart
    const container_1 = document.getElementById('chart');
    container_1.textContent = '';
    const container_2 = document.getElementById('texts');
    container_2.textContent = '';

    //Making invisible the month select box for chart 1
    const box = document.getElementById('texts');
    box.style.display = 'block';

    const height = 400,
    width = 600,
    margin = ({ top: 20, right: 20, bottom: 40, left: 40 });

    const svg = d3.select("#chart")
        .append("svg")
        .attr("viewBox", [0, 0, width, height]);

    d3.csv('total_deaths_by_month.csv').then(data => {
        for (let d of data) {
            d.Deaths = +d.Deaths;
        }

        let x = d3.scaleBand()
                    .domain(data.map(d => d.Month))
                    .range([margin.left, width - margin.right])
                    .padding(0,1);
        
        let y = d3.scaleLinear()
                    .domain([0, d3.max(data, d => d.Deaths)]).nice()
                    .range([height - margin.bottom, margin.top]);
                    
        
        svg.append("g")
            .attr("transform", `translate(${margin.left},0)`)
            .attr("class", "y-axis") // adding a class to y-axis for scoping
            .call(d3.axisLeft(y)
            .tickSizeOuter(0)
            .tickFormat(d => d)
            .tickSize(-width + margin.right + margin.left) // modified to meet at end of axis
            );
    
        svg.append("g")
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x).tickSizeOuter(0));
    
        svg.append("text")
            .attr("class", "x-label")
            .attr("text-anchor", "end")
            .attr("x", width - margin.right)
            .attr("y", height)
            .attr("dx", "0.5em")
            .attr("dy", "-1.0em")
            .attr("font-weight", 800)
            .text("Month");
        
        svg.append("text")
            .attr("class", "y-label")
            .attr("text-anchor", "end")
            .attr("x", -margin.top/2)
            .attr("dx", "-0.5em")
            .attr("y", 7)
            .attr("transform", "rotate(-90)")
            .attr("font-weight", 800)
            .text("Total Deaths");
        
        let line = d3.line()
            .x(d => x(d.Month))
            .y(d => y(d.Deaths))
            .curve(d3.curveNatural); // more: https://observablehq.com/@d3/d3-line#cell-244
    
        svg.append("path")
            .datum(data)
            .attr("d", line)
            .attr("fill", "none")
            .attr("stroke", "steelblue");
    
        });}
