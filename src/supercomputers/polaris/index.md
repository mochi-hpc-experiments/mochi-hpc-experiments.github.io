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

## Benchmark Results

```js
// Load bandwidth data from CSV file
const bandwidthData = await FileAttachment("bandwidth.csv").csv({typed: true});
// Load GPU bandwidth data from CSV file
const bandwidthDataGPU = await FileAttachment("gpu-bandwidth.csv").csv({typed: true});
// Load latency data from CSV file
const latencyData = await FileAttachment("latency.csv").csv({typed: true});
```

The following results are collected from running the
[mochi-tests](https://github.com/mochi-hpc-experiments/mochi-tests) everyday on Polaris.
These tests consist of the following.

* [Latency tests](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/margo-p2p-latency.c): report the round-trip time for a no-op RPC between two processes located on different nodes;
* [Bandwidth tests](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/margo-p2p-bw.c): report the performance of RDMA operations between two processes located on different nodes;
* [GPU bandwidth tests](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/gpu-margo-p2p-bw.cu): report the performance of RDMA operations between GPU or CPU memory of two processes located on different nodes.

The following sections present these results in two forms: most recent daily run, and evolution over time.
In the latter, dropdown menus are available to vary the parameters of the runs.

## Bandwidth Performance


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
