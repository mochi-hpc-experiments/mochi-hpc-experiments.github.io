# Mochi HPC Experiments

Welcome to the Mochi HPC Benchmark Performance Dashboard. This site presents performance data from benchmarks running on multiple supercomputing systems.

## Available Supercomputers

Select a supercomputer below to view its benchmark performance data:


```js
// Define the list of supercomputers
const supercomputers = [
  {
    name: "Example System 1",
    slug: "example-system-1",
    description: "Description of Example System 1",
    image: await FileAttachment("supercomputers/example-system-1/machine.jpg").url()
  }
];
```

```js
html`<div class="grid grid-cols-1" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
  ${supercomputers.map(sc => html`
    <div class="card" style="border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), url(${sc.image}); background-size: cover; background-position: center;">
      <h2 style="margin-top: 0;"><a href="/supercomputers/${sc.slug}/">${sc.name}</a></h2>
      <p>${sc.description}</p>
    </div>
  `)}
</div>`
```

## About

This dashboard tracks performance metrics from Mochi HPC benchmarks across different supercomputing platforms. Each system has its own dedicated page with detailed performance visualizations and analysis.

---

*Last updated: ${new Date().toLocaleDateString()}*
