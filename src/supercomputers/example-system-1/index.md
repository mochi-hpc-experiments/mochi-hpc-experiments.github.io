# Example System 1

[← Back to all systems](/)

```js
const machineImage = await FileAttachment("machine.jpg").url();
```

```js
html`<img src="${machineImage}" alt="Example System 1" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 2rem;">`
```

## System Overview

This page displays benchmark performance data for Example System 1.

## Performance Metrics

```js
// Load performance data from CSV file
const performanceData = await FileAttachment("data.csv").csv({typed: true});
```

### Throughput Over Time

```js
Plot.plot({
  marks: [
    Plot.barY(performanceData, {x: "date", y: "throughput", fill: "steelblue"})
  ],
  x: {label: "Date"},
  y: {label: "Throughput (MB/s)"},
  width: 800,
  height: 400
})
```

### Latency Over Time

```js
Plot.plot({
  marks: [
    Plot.barY(performanceData, {x: "date", y: "latency", fill: "coral"})
  ],
  x: {label: "Date"},
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
