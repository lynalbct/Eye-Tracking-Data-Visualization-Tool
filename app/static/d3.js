// URL: https://observablehq.com/@lynalbct/connected-scatterplot
// Title: Connected Scatterplot
// Author: Lyn Albacete (@lynalbct)
// Version: 255
// Runtime version: 1

const m0 = {
  id: "8f7e57582892b726@255",
  variables: [
    {
      inputs: ["md"],
      value: (function(md){return(
md`# Connected Scatterplot

This is a recreation of Hannah Fairfield’s excellent [*Driving Shifts Into Reverse*](http://www.nytimes.com/imagepages/2010/05/02/business/02metrics.html) (2010). Read the annotations of the original! See also Fairfield’s [*Driving Safety, in Fits and Starts*](http://www.nytimes.com/interactive/2012/09/17/science/driving-safety-in-fits-and-starts.html) (2012), [Noah Veltman’s variation](https://bl.ocks.org/veltman/87596f5a256079b95eb9) of this graphic, and [a paper on connected scatterplots](http://steveharoz.com/research/connected_scatterplot/) by Haroz *et al.*

Data: Hannah Fairfield`
)})
    },
    {
      name: "viewof replay",
      inputs: ["html"],
      value: (function(html){return(
html`<button>Replay`
)})
    },
    {
      name: "replay",
      inputs: ["Generators","viewof replay"],
      value: (G, _) => G.input(_)
    },
    {
      name: "chart",
      inputs: ["replay","d3","DOM","width","height","length","line","data","xAxis","yAxis","x","y","halo"],
      value: (function(replay,d3,DOM,width,height,length,line,data,xAxis,yAxis,x,y,halo)
{
  replay;

  const svg = d3.select(DOM.svg(width, height));

  const l = length(line(data));
  
  svg.append("g")
      .call(xAxis);
  
  svg.append("g")
      .call(yAxis);
  
  svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 2.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-dasharray", `0,${l}`)
      .attr("d", line)
    .transition()
      .duration(5000)
      .ease(d3.easeLinear)
      .attr("stroke-dasharray", `${l},${l}`);
  
  svg.append("g")
      .attr("fill", "white")
      .attr("stroke", "black")
      .attr("stroke-width", 2)
    .selectAll("circle")
    .data(data)
    .join("circle")
      .attr("cx", d => x(d.x))
      .attr("cy", d => y(d.y))
      .attr("r", 3);
  
  const label = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
    .selectAll("g")
    .data(data)
    .join("g")
      .attr("transform", d => `translate(${x(d.x)},${y(d.y)})`)
      .attr("opacity", 0);
  
  label.append("text")
      .text(d => d.name)
      .each(function(d) {
        const t = d3.select(this);
        switch (d.orient) {
          case "top": t.attr("text-anchor", "middle").attr("dy", "-0.7em"); break;
          case "right": t.attr("dx", "0.5em").attr("dy", "0.32em").attr("text-anchor", "start"); break;
          case "bottom": t.attr("text-anchor", "middle").attr("dy", "1.4em"); break;
          case "left": t.attr("dx", "-0.5em").attr("dy", "0.32em").attr("text-anchor", "end"); break;
        }
      })
      .call(halo);
  
  label.transition()
      .delay((d, i) => length(line(data.slice(0, i + 1))) / l * (5000 - 125))
      .attr("opacity", 1);
  
  return svg.node();
}
)
    },
    {
      name: "height",
      value: (function(){return(
720
)})
    },
    {
      name: "margin",
      value: (function(){return(
{top: 20, right: 30, bottom: 30, left: 40}
)})
    },
    {
      name: "x",
      inputs: ["d3","data","margin","width"],
      value: (function(d3,data,margin,width){return(
d3.scaleLinear()
    .domain(d3.extent(data, d => d.x)).nice()
    .range([margin.left, width - margin.right])
)})
    },
    {
      name: "y",
      inputs: ["d3","data","height","margin"],
      value: (function(d3,data,height,margin){return(
d3.scaleLinear()
    .domain(d3.extent(data, d => d.y)).nice()
    .range([height - margin.bottom, margin.top])
)})
    },
    {
      name: "xAxis",
      inputs: ["height","margin","d3","x","width","data","halo"],
      value: (function(height,margin,d3,x,width,data,halo){return(
g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(width / 80))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line").clone()
        .attr("y2", -height)
        .attr("stroke-opacity", 0.1))
    .call(g => g.append("text")
        .attr("x", width - 4)
        .attr("y", -4)
        .attr("font-weight", "bold")
        .attr("text-anchor", "end")
        .attr("fill", "black")
        .text(data.x)
        .call(halo))
)})
    },
    {
      name: "yAxis",
      inputs: ["margin","d3","y","width","data","halo"],
      value: (function(margin,d3,y,width,data,halo){return(
g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(null, "$.2f"))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line").clone()
        .attr("x2", width)
        .attr("stroke-opacity", 0.1))
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 4)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .attr("fill", "black")
        .text(data.y)
        .call(halo))
)})
    },
    {
      name: "halo",
      value: (function(){return(
function halo(text) {
  text.select(function() { return this.parentNode.insertBefore(this.cloneNode(true), this); })
      .attr("fill", "none")
      .attr("stroke", "white")
      .attr("stroke-width", 4)
      .attr("stroke-linejoin", "round");
}
)})
    },
    {
      name: "length",
      inputs: ["d3"],
      value: (function(d3){return(
function length(path) {
  return d3.create("svg:path").attr("d", path).node().getTotalLength();
}
)})
    },
    {
      name: "line",
      inputs: ["d3","x","y"],
      value: (function(d3,x,y){return(
d3.line()
    .curve(d3.curveCatmullRom)
    .x(d => x(d.x))
    .y(d => y(d.y))
)})
    },
    {
      name: "data",
      inputs: ["d3"],
      value: (async function(d3)
{
  const data = await d3.csv("https://gist.githubusercontent.com/mbostock/bd35887eafa65347debee780753c43a9/raw/bf812ca674d62101e144dad8003107124bf8d1ea/driving.csv", ({side, year, miles, gas}) => ({orient: side, name: year, x: +miles, y: +gas}));
  data.x = "Miles per person per year";
  data.y = "Cost per gallon";
  return data;
}
)
    },
    {
      name: "d3",
      inputs: ["require"],
      value: (function(require){return(
require("d3@5")
)})
    }
  ]
};

const notebook = {
  id: "8f7e57582892b726@255",
  modules: [m0]
};

export default notebook;
