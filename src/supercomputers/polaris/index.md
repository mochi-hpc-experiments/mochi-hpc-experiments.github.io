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
  y: {label: "Latency (μs)", grid: true},
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
  y: {label: "Latency (μs)", grid: true},
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

```js
// Get unique dates from bandwidth data and sort chronologically
const bandwidthDates = [...new Set(bandwidthData.map(d => String(d.date)))]
  .sort((a, b) => new Date(a) - new Date(b));
const latestBandwidthDateInput = Inputs.select(bandwidthDates, {
  label: "Date",
  value: bandwidthDates[bandwidthDates.length - 1]
});
const selectedBandwidthDate = Generators.input(latestBandwidthDateInput);
```

```js
// Filter data for selected date
const bandwidthForDate = bandwidthData.filter(d => String(d.date) === selectedBandwidthDate);

// Create function to generate data for specific op and busy_spin
function getBandwidthData(op, busySpin) {
  const concurrencies = [1, 8];
  const xferSizes = {1048576: "1MiB", 8388608: "8MiB", 1000000: "1MB"};
  const data = [];

  for (const conc of concurrencies) {
    for (const [xferSize, xferLabel] of Object.entries(xferSizes)) {
      const entry = bandwidthForDate.find(d =>
        d.op === op &&
        d.concurrency === conc &&
        d.xfer_size === Number(xferSize) &&
        d.busy_spin === busySpin
      );
      data.push({
        category: `C${conc}-${xferLabel}`,
        throughput: entry ? entry["MiB/s"] / 1024 : 0
      });
    }
  }
  return data;
}

const bandwidthPullFalse = getBandwidthData("PULL", false);
const bandwidthPullTrue = getBandwidthData("PULL", true);
const bandwidthPushFalse = getBandwidthData("PUSH", false);
const bandwidthPushTrue = getBandwidthData("PUSH", true);
```

The following graphs show the bandwidth for different levels of transfer concurrency
(1 or 8 threads) and different transfer sizes (1 MB, 1 MiB, or 8 MiB). Legends
indicate the concurrency and transfer sizes (e.g. 1C-1MB represents 1 thread and 1 MB transfers).

```js
html`<div style="margin-bottom: 1rem;">
  ${latestBandwidthDateInput}
</div>`
```

```js
html`<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
  <div>
    <h4 style="text-align: center; margin-bottom: 0.5rem;">PULL, Busy Spin: false</h4>
    ${Plot.plot({
      marks: [
        Plot.barY(bandwidthPullFalse, {x: "category", y: "throughput", fill: "category"})
      ],
      x: {label: null},
      y: {label: "Throughput (GiB/s)", grid: true},
      color: {legend: true},
      width: 380,
      height: 300,
      marginLeft: 60,
      marginBottom: 60
    })}
  </div>
  <div>
    <h4 style="text-align: center; margin-bottom: 0.5rem;">PULL, Busy Spin: true</h4>
    ${Plot.plot({
      marks: [
        Plot.barY(bandwidthPullTrue, {x: "category", y: "throughput", fill: "category"})
      ],
      x: {label: null},
      y: {label: "Throughput (GiB/s)", grid: true},
      color: {legend: true},
      width: 380,
      height: 300,
      marginLeft: 60,
      marginBottom: 60
    })}
  </div>
  <div>
    <h4 style="text-align: center; margin-bottom: 0.5rem;">PUSH, Busy Spin: false</h4>
    ${Plot.plot({
      marks: [
        Plot.barY(bandwidthPushFalse, {x: "category", y: "throughput", fill: "category"})
      ],
      x: {label: null},
      y: {label: "Throughput (GiB/s)", grid: true},
      color: {legend: true},
      width: 380,
      height: 300,
      marginLeft: 60,
      marginBottom: 60
    })}
  </div>
  <div>
    <h4 style="text-align: center; margin-bottom: 0.5rem;">PUSH, Busy Spin: true</h4>
    ${Plot.plot({
      marks: [
        Plot.barY(bandwidthPushTrue, {x: "category", y: "throughput", fill: "category"})
      ],
      x: {label: null},
      y: {label: "Throughput (GiB/s)", grid: true},
      color: {legend: true},
      width: 380,
      height: 300,
      marginLeft: 60,
      marginBottom: 60
    })}
  </div>
</div>`
```

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
  y: {label: "Throughput (GiB/s)", grid: true},
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

## GPU Bandwidth Performance

GPU bandwidth is measured using the
[gpu-margo-p2p-bw](https://github.com/mochi-hpc-experiments/mochi-tests/blob/main/perf-regression/gpu-margo-p2p-bw.cu)
benchmark, which runs on two processes located on distinct nodes, and transfers data using RDMA between CPU and/or GPU memory.

### Latest GPU Bandwidth Results


```js
// Get unique dates from GPU bandwidth data and sort chronologically
const gpuBandwidthDates = [...new Set(bandwidthDataGPU.map(d => String(d.date)))]
  .sort((a, b) => new Date(a) - new Date(b));
const latestGPUBandwidthDateInput = Inputs.select(gpuBandwidthDates, {
  label: "Date",
  value: gpuBandwidthDates[gpuBandwidthDates.length - 1]
});
const selectedGPUBandwidthDate = Generators.input(latestGPUBandwidthDateInput);
```

```js
// Filter data for selected date
const gpuBandwidthForDate = bandwidthDataGPU.filter(d => String(d.date) === selectedGPUBandwidthDate);

// Create data for all memory combinations and operations
const memCombinations = [
  {hostA: "GPU", hostB: "GPU"},
  {hostA: "GPU", hostB: "CPU"},
  {hostA: "CPU", hostB: "GPU"},
  {hostA: "CPU", hostB: "CPU"}
];

const ops = ["PULL", "PUSH"];
const gpuBandwidthBarData = [];

for (const mem of memCombinations) {
  for (const op of ops) {
    const entry = gpuBandwidthForDate.find(d =>
      d.op === op &&
      d.hostA_mem === mem.hostA &&
      d.hostB_mem === mem.hostB
    );
    // Arrow direction: → for PULL (A pulls from B), ← for PUSH (A pushes to B)
    const arrow = op === "PULL" ? "→" : "←";
    gpuBandwidthBarData.push({
      category: `${mem.hostA}${arrow}${mem.hostB}`,
      throughput: entry ? entry["MiB/s"] / 1024 : 0
    });
  }
}
```

The following graph shows the GPU bandwidth for different memory locations on each host.
HostA and HostB refer to the two processes on distinct nodes.
Host A is always the sender of an RPC to Host B. The latter issues the RDMA transfer (PUSH or PULL). Hence "GPU←CPU" means that Host B issues a PUSH from its CPU memory to Host A's GPU memory. "GPU→CPU" means that Host B issues a PULL from Host A's GPU memory to Host B's CPU memory.

```js
html`<div style="margin-bottom: 1rem;">
  ${latestGPUBandwidthDateInput}
</div>`
```

```js
Plot.plot({
  marks: [
    Plot.barY(gpuBandwidthBarData, {x: "category", y: "throughput", fill: "category"})
  ],
  x: {label: null, tickFormat: () => ""},
  y: {label: "Throughput (GiB/s)", grid: true},
  color: {legend: true},
  width: 800,
  height: 400,
  marginLeft: 60,
  marginBottom: 60
})
```

### GPU Bandwidth Over Time

```js
// Create input widgets for GPU bandwidth filtering
const gpuOperationInput = Inputs.select(["PULL", "PUSH"], {label: "Operation", value: "PULL"});
const gpuOperation = Generators.input(gpuOperationInput);
const hostAMemInput = Inputs.select(["CPU", "GPU"], {label: "Host A Memory", value: "GPU"});
const hostA_mem = Generators.input(hostAMemInput);
const hostBMemInput = Inputs.select(["CPU", "GPU"], {label: "Host B Memory", value: "GPU"});
const hostB_mem = Generators.input(hostBMemInput);
```

```js
// Filter GPU bandwidth data based on selected inputs
const filteredGPUBandwidthData = bandwidthDataGPU.filter(d =>
  d.op === gpuOperation &&
  d.hostA_mem === hostA_mem &&
  d.hostB_mem === hostB_mem
);

// Calculate 30-day range ending at latest date
const latestGPUBandwidthDate = bandwidthDataGPU.length > 0
  ? new Date(Math.max(...bandwidthDataGPU.map(d => new Date(d.date))))
  : new Date();
const thirtyDaysAgoGPUBandwidth = new Date(latestGPUBandwidthDate);
thirtyDaysAgoGPUBandwidth.setDate(thirtyDaysAgoGPUBandwidth.getDate() - 30);
```

```js
Plot.plot({
  marks: [
    Plot.rectY(filteredGPUBandwidthData, {x: "date", y: d => d["MiB/s"] / 1024, fill: "purple", interval: "day"})
  ],
  x: {type: "utc", label: "Date", domain: [thirtyDaysAgoGPUBandwidth, latestGPUBandwidthDate]},
  y: {label: "Throughput (GiB/s)", grid: true},
  width: 800,
  height: 400,
  marginLeft: 60,
  marginBottom: 40
})
```

```js
// Display the input widgets
html`<div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
  ${gpuOperationInput}
  ${hostAMemInput}
  ${hostBMemInput}
</div>`
```

## Spack Environment

```js
const spackYaml = await FileAttachment("spack.yaml").text();
```

The following is the Spack environment used for the latest run. This environment mostly comes from 
[the Mochi Platform Configurations](https://github.com/mochi-hpc-experiments/platform-configurations/tree/main/ANL/Polaris).

```js
html`<details>
  <summary style="cursor: pointer; padding: 0.5rem; background-color: #f5f5f5; border-radius: 4px; user-select: none;">
    Click to expand spack.yaml
  </summary>
  <pre style="margin-top: 0.5rem; padding: 1rem; background-color: #f5f5f5; border-radius: 4px; overflow-x: auto;"><code>${spackYaml}</code></pre>
</details>`
```

