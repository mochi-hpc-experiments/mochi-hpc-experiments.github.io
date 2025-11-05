# Mochi HPC Experiments Dashboard

This project uses [Observable Framework](https://observablehq.com/framework/) to present performance information from benchmarks running on multiple supercomputers.

## Project Structure

```
.
├── src/
│   ├── index.md                    # Main page with supercomputer list
│   ├── supercomputers/             # Individual supercomputer pages
│   │   ├── example-system-1.md
│   │   └── example-system-2.md
│   └── data/                       # Data loaders for benchmark data
├── observablehq.config.js          # Framework configuration
└── package.json                    # Dependencies and scripts
```

## Getting Started

### Install Dependencies

```bash
npm install
```

### Development

Start the local development server:

```bash
npm run dev
```

This will start a local server at `http://localhost:3000` where you can preview your site.

### Build

Build the static site:

```bash
npm run build
```

The built site will be in the `dist/` directory.

## Adding a New Supercomputer

To add a new supercomputer:

1. Create a new markdown file in `src/supercomputers/` (e.g., `my-system.md`)
2. Add the system to the list in `src/index.md`
3. Add performance data visualization using Observable Plot
4. Optionally create data loaders in `src/data/` for loading benchmark results

## Data Loading

Observable Framework supports data loaders that can fetch and process data at build time. Place data loaders in the `src/data/` directory. They can be:

- JavaScript/TypeScript files (`.js`, `.ts`)
- Python scripts (`.py`)
- Shell scripts (`.sh`)
- Any executable that outputs JSON, CSV, or other supported formats

Example data loader (`src/data/system-metrics.json.js`):

```javascript
import fs from "fs";

// Fetch or generate your data
const data = await fetchBenchmarkData();

// Output as JSON
process.stdout.write(JSON.stringify(data));
```

## Deployment

For GitHub Pages deployment:

```bash
npm run build
```

Then commit and push the `dist/` directory, or configure GitHub Actions to build and deploy automatically.

## Learn More

- [Observable Framework Documentation](https://observablehq.com/framework/)
- [Observable Plot](https://observablehq.com/plot/)
- [Observable Inputs](https://observablehq.com/@observablehq/inputs)
