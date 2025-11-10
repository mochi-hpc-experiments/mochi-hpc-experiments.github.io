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

## Bandwidth Performance

```js
// Load bandwidth data from CSV file
const bandwidthData = await FileAttachment("bandwidth.csv").csv({typed: true});
```

```js
// Create input widgets for filtering
const operationInput = Inputs.select(["PULL", "PUSH"], {label: "Operation", value: "PULL"});
const operation = Generators.input(operationInput);
```

```js
const concurrencyInput = Inputs.select([1, 8], {label: "Concurrency", value: 1});
const concurrency = Generators.input(concurrencyInput);
```

```js
const busySpinInput = Inputs.select([true, false], {label: "Busy Spin", value: false});
const busy_spin = Generators.input(busySpinInput);
```

```js
const xferSizeInput = Inputs.select([1048576, 8388608, 1000000], {label: "Transfer Size (bytes)", value: 1048576});
const xfer_size = Generators.input(xferSizeInput);
```

```js
// Filter data based on selected inputs
const filteredBandwidthData = bandwidthData.filter(d =>
  d.op === operation &&
  d.concurrency === concurrency &&
  d.busy_spin === busy_spin &&
  d.xfer_size === xfer_size
);
```

### Bandwidth Over Time

```js
Plot.plot({
  marks: [
    Plot.rectY(filteredBandwidthData, {x: "date", y: d => d["MiB/s"] / 1024, fill: "green", interval: "day"})
  ],
  x: {type: "utc", label: "Date"},
  y: {label: "Throughput (GiB/s)"},
  width: 800,
  height: 400
})
```

```js
// Display the input widgets
html`<div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
  ${operationInput}
  ${concurrencyInput}
  ${busySpinInput}
  ${xferSizeInput}
</div>`
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
