# Example System 1

[← Back to all systems](/)

## System Overview

This page displays benchmark performance data for Example System 1.

## Performance Metrics

```js
// Load performance data
// Replace this with actual data loading from your data sources
const performanceData = [
  {date: "2024-01-01", throughput: 100, latency: 10},
  {date: "2024-02-01", throughput: 120, latency: 9},
  {date: "2024-03-01", throughput: 115, latency: 11},
];
```

### Throughput Over Time

```js
Plot.plot({
  marks: [
    Plot.line(performanceData, {x: "date", y: "throughput", stroke: "steelblue"}),
    Plot.dot(performanceData, {x: "date", y: "throughput", fill: "steelblue"})
  ],
  x: {type: "utc", label: "Date"},
  y: {label: "Throughput (MB/s)"},
  width: 800,
  height: 400
})
```

### Latency Over Time

```js
Plot.plot({
  marks: [
    Plot.line(performanceData, {x: "date", y: "latency", stroke: "coral"}),
    Plot.dot(performanceData, {x: "date", y: "latency", fill: "coral"})
  ],
  x: {type: "utc", label: "Date"},
  y: {label: "Latency (ms)"},
  width: 800,
  height: 400
})
```

## Benchmark Details

- **System**: Example System 1
- **Latest Run**: ${new Date().toLocaleDateString()}
- **Status**: Active

## Data

View the raw performance data:

```js
Inputs.table(performanceData)
```
