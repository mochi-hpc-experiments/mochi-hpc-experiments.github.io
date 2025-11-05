# Mochi HPC Experiments

Welcome to the Mochi HPC Benchmark Performance Dashboard. This site presents performance data from benchmarks running on multiple supercomputing systems.

## Available Supercomputers

Select a supercomputer below to view its benchmark performance data.


```js
// Load the list of supercomputers from data loader
const supercomputers = await FileAttachment("data/supercomputers.json").json();
```

```js
html`<div class="grid grid-cols-1" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
  ${supercomputers.map(sc => html`
    <a href="/supercomputers/${sc.slug}/" style="text-decoration: none; color: inherit;">
      <div class="card" style="border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), url(${sc.image}); background-size: cover; background-position: center; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;">
        <h2 style="margin: 0; font-size: 2rem;">${sc.name}</h2>
      </div>
    </a>
  `)}
</div>

<style>
  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
</style>`
```

## About

This dashboard tracks performance metrics from Mochi HPC benchmarks across different supercomputing platforms. Each system has its own dedicated page with detailed performance visualizations and analysis.

---

*Last updated: ${new Date().toLocaleDateString()}*
