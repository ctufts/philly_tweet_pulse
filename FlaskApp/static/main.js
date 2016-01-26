

/////////////////////////////GENDER CHART/////////////////////////////
function dsGenderChart() {
  var margin = {top: 40, right: 60, bottom: 90, left: 40},
    width = 600 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

  var y = d3.scale.linear()
      .rangeRound([height, 0]);

  var color = d3.scale.ordinal()
      .range(["#7A99AC", "#E4002B"]);
      // .range(["#D62728", "#1F77B4"]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(d3.time.format("%m/%d/%y %H:%M"));

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format(".2s"));

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      var v = d.y1 - d.y0;
      return "<strong>Tweets:</strong> <span style='color:#c8c8c8'>" + v + "</span>";
    })

    // var svg = d3.select("#barChart").append("svg")
  var svg = d3.select("#genderChart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.call(tip);


  d3.csv('/static/gender_data.csv', function(error, data) {
    if (error) throw error;
    // console.log(data[0])
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "ts"; }));

    data.forEach(function(d) {
      var y0 = 0;
      d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
      d.total = d.ages[d.ages.length - 1].y1;
      d.ts    = parseDate(d.ts);
    });

    x.domain(data.map(function(d) { return d.ts; }));
    y.domain([0, d3.max(data, function(d) { return d.total; })]);

    xAxis.tickValues(x.domain().filter(function(d, i) { return !(i % 2); }))
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")  
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)" );

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(-5,0)")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y",6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .style("font-size", 12)
        .text("Tweets");

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px")
        .text("Hourly Tweet Frequency By Gender");

    var ts = svg.selectAll(".ts")
        .data(data)
      .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x(d.ts) + ",0)"; });

    ts.selectAll("rect")
        .data(function(d) { return d.ages; })
      .enter().append("rect")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    
    var legend = svg.selectAll(".legend")
        .data(color.domain().slice().reverse())
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + 26)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width + 22)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

});

}
dsGenderChart();

function dsAgeChart() {
  var margin = {top: 40, right: 60, bottom: 90, left: 40},
    width = 600 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

  var y = d3.scale.linear()
      .rangeRound([height, 0]);

  var color = d3.scale.ordinal()
      .range(["#edf8fb","#bfd3e6","#9ebcda",
        "#8c96c6","#8c6bb1","#88419d","#6e016b"]);
  //d3.scale.category20b();
      // .range(["#98abc5", "#ff8c00"]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .tickFormat(d3.time.format("%m/%d/%y %H:%M"));


  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format(".2s"));

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      var v = d.y1 - d.y0;
      return "<strong>Tweets:</strong> <span style='color:#c8c8c8;'>" + v + "</span>";
    })        
    // var svg = d3.select("#barChart").append("svg")
  var svg = d3.select("#ageChart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.call(tip);


  d3.csv('/static/age_data.csv', function(error, data) {
    if (error) throw error;
    console.log(data[0])
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "ts"; }));

    data.forEach(function(d) {
      var y0 = 0;
      d.ages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
      d.total = d.ages[d.ages.length - 1].y1;
      d.ts    = parseDate(d.ts);
    });

    // data.sort(function(a, b) { return b.total - a.total; });

    x.domain(data.map(function(d) { return d.ts; }));
    y.domain([0, d3.max(data, function(d) { return d.total; })]);

    // only show every other tick label
    xAxis.tickValues(x.domain().filter(function(d, i) { return !(i % 2); }))
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")  
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-65)" );

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(-5,0)")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .style("font-size", "12px")
        .text("Tweets");

    svg.append("text")
        .attr("x", (width / 2))             
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")  
        .style("font-size", "16px")
        .text("Hourly Tweet Frequency By Age");

    var ts = svg.selectAll(".ts")
        .data(data)
      .enter().append("g")
        .attr("class", "g")
        .attr("transform", function(d) { return "translate(" + x(d.ts) + ",0)"; });

    ts.selectAll("rect")
        .data(function(d) { return d.ages; })
      .enter().append("rect")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    
    var legend = svg.selectAll(".legend")
        .data(color.domain().slice().reverse())
      .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width + 26 )
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width + 22)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

});

}
dsAgeChart();

