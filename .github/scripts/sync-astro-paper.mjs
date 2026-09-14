import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

export async function syncBlog(source, site) {
  const counts = { posts: 0, images: 0, structures: 0 };
  async function copyTree(from, to, kind, accept, excluded = []) {
    let entries;
    try { entries = await readdir(from, { withFileTypes: true }); }
    catch (error) { if (error.code === "ENOENT" && kind !== "posts") return; throw error; }
    for (const entry of entries) {
      if (excluded.includes(entry.name)) continue;
      if (entry.isSymbolicLink()) throw new Error(`Symlink is not a sync input: ${path.join(from, entry.name)}`);
      const input = path.join(from, entry.name), output = path.join(to, entry.name);
      if (entry.isDirectory()) { await copyTree(input, output, kind, accept); continue; }
      if (!entry.isFile() || !accept(entry.name)) continue;
      const content = await readFile(input);
      let previous;
      try { previous = await readFile(output); } catch (error) { if (error.code !== "ENOENT") throw error; }
      if (previous?.equals(content)) continue;
      await mkdir(path.dirname(output), { recursive: true });
      await writeFile(output, content);
      counts[kind]++;
    }
  }
  await copyTree(source, path.join(site, "src/data/blog"), "posts", name => name.endsWith(".md"), ["mc", "blog-assets"]);
  await copyTree(path.join(source, "blog-assets"), path.join(site, "public/blog-assets"), "images", () => true);
  await copyTree(path.join(source, "mc"), path.join(site, "src/data/mc/structures"), "structures", name => name.toLowerCase().endsWith(".nbt"));
  return counts;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const [source, site] = process.argv.slice(2);
  if (!source || !site) throw new Error("Usage: node sync-astro-paper.mjs <Blog/Note> <Astro-Paper>");
  console.log(await syncBlog(path.resolve(source), path.resolve(site)));
}
