// custom javascript
function dsBarChart() {
var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.time.format("%H:%M").parse;

var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(d3.time.format("%H:%M"));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("#barChart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

d3.json('/data', function(error,data) {
   if (error) throw error;


  data.forEach(function(d) {
    d.ts = parseDate(d.ts);
    d.timecount = +d.timecount;
  });
  
  x.domain(data.map(function(d) { return d.ts; }));
  y.domain([0, d3.max(data, function(d) { return d.timecount; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("timecount ($)");

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.ts); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.timecount); })
      .attr("height", function(d) { return height - y(d.timecount); });

});
}
dsBarChart();

function dsLineChart(){
	var margin = {top: 20, right: 20, bottom: 70, left: 40},
    width = 600 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

//alter the time parser
//var parseDate = d3.time.format("%a %b %d %H:%M:%S +0000 %Y").parse;
var parseDate = d3.time.format("%H:%M").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.ts); })
    .y(function(d) { return y(d.timecount); });

var svg = d3.select("#lineChart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json('/data', function(error,data) {
   if (error) throw error;


  data.forEach(function(d) {
    d.ts = parseDate(d.ts);
    d.timecount = +d.timecount;
  });

  x.domain(d3.extent(data, function(d) { return d.ts; }));
  y.domain(d3.extent(data, function(d) { return d.timecount; }));

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Tweets");

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
});
}
dsLineChart();
