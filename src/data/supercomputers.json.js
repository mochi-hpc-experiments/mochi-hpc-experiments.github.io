import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import yaml from "js-yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const supercomputersDir = path.join(__dirname, "..", "supercomputers");

// Read all subdirectories in the supercomputers folder
const directories = fs.readdirSync(supercomputersDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

// Read info.yaml from each directory
const supercomputers = directories.map(slug => {
  const infoPath = path.join(supercomputersDir, slug, "info.yaml");

  if (!fs.existsSync(infoPath)) {
    console.error(`Warning: ${slug}/info.yaml not found`);
    return null;
  }

  const infoContent = fs.readFileSync(infoPath, "utf8");
  const info = yaml.load(infoContent);

  // Read image and convert to base64 data URL
  const imagePath = path.join(supercomputersDir, slug, "machine.jpg");
  let imageDataUrl = "";
  if (fs.existsSync(imagePath)) {
    const imageBuffer = fs.readFileSync(imagePath);
    const imageBase64 = imageBuffer.toString("base64");
    imageDataUrl = `data:image/jpeg;base64,${imageBase64}`;
  }

  return {
    slug,
    name: info.name,
    description: info.description,
    image: imageDataUrl
  };
}).filter(sc => sc !== null);

// Output as JSON
process.stdout.write(JSON.stringify(supercomputers, null, 2));
