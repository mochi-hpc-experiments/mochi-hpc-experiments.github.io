# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dashboard for presenting Mochi HPC benchmark performance data from multiple supercomputers, built with Observable Framework. Observable Framework is a static site generator that combines markdown files with reactive JavaScript code blocks for data visualization.

## Development Commands

**Start development server:**
```bash
npm run dev
```
Starts local server at http://localhost:3000 with live reload.

**Build static site:**
```bash
npm run build
```
Outputs to `dist/` directory.

**Deploy to Observable:**
```bash
npm run deploy
```

**Clean build artifacts:**
```bash
npm run clean
```

## Architecture

### Observable Framework Conventions

**Reactive code blocks:** JavaScript code blocks in markdown files are executed reactively. Variables defined in one block are available in subsequent blocks on the same page.

**Page routing:** Files in `src/` automatically become pages:
- `src/index.md` → `/`
- `src/supercomputers/example-system-1.md` → `/supercomputers/example-system-1`

**Data loaders:** Place in `src/data/` directory. These run at build time (not in browser):
- Must output to stdout (e.g., `process.stdout.write(JSON.stringify(data))`)
- Can be `.js`, `.ts`, `.py`, `.sh`, or any executable
- Access in markdown via `FileAttachment("data/filename.json")`
- Examples: `src/data/metrics.json.js` outputs JSON, `src/data/results.csv.py` outputs CSV

### Project Structure

- `src/index.md` - Main landing page listing all supercomputers
- `src/supercomputers/*.md` - Individual system pages with visualizations
- `src/data/` - Data loaders that fetch/process benchmark data at build time
- `observablehq.config.js` - Framework configuration (title, header, footer, theme)
- `dist/` - Build output (not tracked in git)

### Visualization Approach

**Observable Plot** is the primary visualization library. Use it for charts:
```javascript
Plot.plot({
  marks: [
    Plot.line(data, {x: "date", y: "value"}),
    Plot.dot(data, {x: "date", y: "value"})
  ]
})
```

**Inputs** library for interactive controls:
```javascript
Inputs.table(data)
Inputs.select(options)
```

**HTML interpolation** using tagged template literals:
```javascript
html`<div>${content}</div>`
```

## Adding a New Supercomputer

1. Create `src/supercomputers/<system-slug>.md`
2. Add entry to `supercomputers` array in `src/index.md`
3. Add visualizations using Observable Plot
4. Create data loaders in `src/data/` if fetching external benchmark results

## Configuration

Edit `observablehq.config.js` to modify:
- Site title and header text
- Theme (`"default"`, `"light"`, `"dark"`, etc.)
- Navigation pages
- Table of contents and search functionality
