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

## Benchmark Details

```js
// Load bandwidth data from CSV file
const bandwidthData = await FileAttachment("bandwidth.csv").csv({typed: true});
// Load GPU bandwidth data from CSV file
const bandwidthDataGPU = await FileAttachment("gpu-bandwidth.csv").csv({typed: true});
// Load latency data from CSV file
const latencyData = await FileAttachment("latency.csv").csv({typed: true});
```

```js
// Get the latest date from the data
const latestDate = latencyData.length > 0
  ? new Date(latencyData[latencyData.length - 1].date).toLocaleDateString()
  : "N/A";
```

- **Latest Run**: ${latestDate}

The following results are collected from running the
[mochi-tests](https://github.com/mochi-hpc-experiments/mochi-tests) every day on Polaris.
The following sections present bandwidth and latency results in two forms:
most recent daily run, and evolution over time.
In the latter, dropdown menus are available to vary the parameters of the runs.

## Latency Performance

Latency is measured using the
[margo-p2p-latency](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/margo-p2p-latency.c)
benchmark, which runs on two processes located on distinct nodes, and issues no-op RPCs to measure round-trip time.

### Latest Latency Results

```js
// Get unique dates from latency data and sort chronologically
const latencyDates = [...new Set(latencyData.map(d => String(d.date)))]
  .sort((a, b) => new Date(a) - new Date(b));
const latestLatencyDateInput = Inputs.select(latencyDates, {
  label: "Date",
  value: latencyDates[latencyDates.length - 1]
});
const selectedLatencyDate = Generators.input(latestLatencyDateInput);
```

```js
// Filter data for selected date (compare as strings)
const latencyForDate = latencyData.filter(d => String(d.date) === selectedLatencyDate);

// Prepare data for bar chart
const latencyFalse = latencyForDate.find(d => d.busy_spin === false);
const latencyTrue = latencyForDate.find(d => d.busy_spin === true);

const latencyBarData = [
  {
    category: "Busy Spin: false",
    latency: latencyFalse ? latencyFalse.med * 1e6 : 0
  },
  {
    category: "Busy Spin: true",
    latency: latencyTrue ? latencyTrue.med * 1e6 : 0
  }
];
```

```js
html`<div style="margin-bottom: 1rem;">
  ${latestLatencyDateInput}
</div>`
```

```js
Plot.plot({
  marks: [
    Plot.barY(latencyBarData, {x: "category", y: "latency", fill: "category"})
  ],
  x: {label: null, tickFormat: () => ""},
  y: {label: "Latency (μs)"},
  color: {legend: true},
  width: 600,
  height: 400,
  marginLeft: 60,
  marginBottom: 60
})
```

### Latency Over Time

```js
// Create input widget for busy_spin filtering
const latencyBusySpinInput = Inputs.select([true, false], {label: "Busy Spin", value: false});
const latency_busy_spin = Generators.input(latencyBusySpinInput);
```

```js
// Filter latency data based on busy_spin
const filteredLatencyData = latencyData.filter(d => d.busy_spin === latency_busy_spin);

// Calculate 30-day range ending at latest date
const latestLatencyDate = latencyData.length > 0
  ? new Date(Math.max(...latencyData.map(d => new Date(d.date))))
  : new Date();
const thirtyDaysAgo = new Date(latestLatencyDate);
thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
```

```js
Plot.plot({
  marks: [
    Plot.rectY(filteredLatencyData, {x: "date", y: d => d.med * 1e6, fill: "coral", interval: "day"})
  ],
  x: {type: "utc", label: "Date", domain: [thirtyDaysAgo, latestLatencyDate]},
  y: {label: "Latency (μs)"},
  width: 800,
  height: 400,
  marginLeft: 60,
  marginBottom: 40
})
```

```js
// Display the input widget
html`<div style="margin-top: 1rem;">
  ${latencyBusySpinInput}
</div>`
```

## Bandwidth Performance

Bandwidth is measured using the
[margo-p2p-bw](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/margo-p2p-bw.c)
benchmark, which runs on two processes located on distinct nodes, and transfers data using RDMA.

### Latest Bandwidth Results

TODO

### Bandwidth Over Time

```js
// Create input widgets for filtering
const operationInput = Inputs.select(["PULL", "PUSH"], {label: "Operation", value: "PULL"});
const operation = Generators.input(operationInput);
const concurrencyInput = Inputs.select([1, 8], {label: "Concurrency", value: 1});
const concurrency = Generators.input(concurrencyInput);
const busySpinInput = Inputs.select([true, false], {label: "Busy Spin", value: false});
const busy_spin = Generators.input(busySpinInput);
const xferSizeInput = Inputs.select([1048576, 8388608, 1000000],
                                    {label: "Transfer Size (bytes)", value: 1048576});
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

// Calculate 30-day range ending at latest date
const latestBandwidthDate = bandwidthData.length > 0
  ? new Date(Math.max(...bandwidthData.map(d => new Date(d.date))))
  : new Date();
const thirtyDaysAgoBandwidth = new Date(latestBandwidthDate);
thirtyDaysAgoBandwidth.setDate(thirtyDaysAgoBandwidth.getDate() - 30);
```

```js
Plot.plot({
  marks: [
    Plot.rectY(filteredBandwidthData, {x: "date", y: d => d["MiB/s"] / 1024, fill: "green", interval: "day"})
  ],
  x: {type: "utc", label: "Date", domain: [thirtyDaysAgoBandwidth, latestBandwidthDate]},
  y: {label: "Throughput (GiB/s)"},
  width: 800,
  height: 400,
  marginLeft: 60,
  marginBottom: 40
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

