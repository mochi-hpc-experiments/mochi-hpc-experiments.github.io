# Polaris

[← Back to all systems](/)

```js
const machineImage = await FileAttachment("machine.jpg").url();
```

```js
html`<img src="${machineImage}" alt="Polaris" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 2rem;">`
```

## System Overview

Polaris is Argonne's 34 petaflops supercomputer, featuring
560 compute nodes, each equipped with 1 AMD EPYC "Milan" processor,
4 NVIDIA A100 GPUs, Unified Memory Architecture, 2 fabric endpoints,
and 2 NVMe SSDs. These nodes are connected using HPE Slingshot 11 in
a Dragonfly topology with adaptive routing.

## Performance Metrics

```js
// Load performance data from CSV file
const performanceData = await FileAttachment("data.csv").csv({typed: true});
```

### Throughput Over Time

```js
Plot.plot({
  marks: [
    Plot.rectY(performanceData, {x: "date", y: "throughput", fill: "steelblue", interval: "day"})
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
    Plot.rectY(performanceData, {x: "date", y: "latency", fill: "coral", interval: "day"})
  ],
  x: {type: "utc", label: "Date"},
  y: {label: "Latency (ms)"},
  width: 800,
  height: 400
})
```

## Benchmark Details

- **System**: Polaris
- **Latest Run**: ${new Date().toLocaleDateString()}
- **Status**: Active

## Data

View the raw performance data:

```js
Inputs.table(performanceData)
```
