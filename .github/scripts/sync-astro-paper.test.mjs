import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { syncBlog } from "./sync-astro-paper.mjs";

test("sync writes separate targets, preserves existing data and skips identical files", async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), "obsidian-sync-"));
  const source = path.join(root, "notes"), site = path.join(root, "site");
  const put = async (file, content) => { await mkdir(path.dirname(file), { recursive: true }); await writeFile(file, content); };
  try {
    await put(path.join(source, "post.md"), "文章");
    await put(path.join(source, "blog-assets/image.png"), "image");
    await put(path.join(source, "mc/nested/test.nbt"), Buffer.from([0,255,1]));
    await put(path.join(source, "mc/README.md"), "not a post");
    await put(path.join(site, "src/data/mc/resources/keep.json"), "resource");
    await put(path.join(site, "src/data/blog/keep.md"), "keep");
    assert.deepEqual(await syncBlog(source, site), { posts: 1, images: 1, structures: 1 });
    const target = path.join(site, "src/data/blog/post.md"), before = (await stat(target)).mtimeMs;
    assert.deepEqual(await syncBlog(source, site), { posts: 0, images: 0, structures: 0 });
    assert.equal((await stat(target)).mtimeMs, before);
    assert.deepEqual(await readFile(path.join(site,"src/data/mc/structures/nested/test.nbt")),Buffer.from([0,255,1]));
    assert.equal(await readFile(path.join(site,"src/data/mc/resources/keep.json"),"utf8"),"resource");
    assert.equal(await readFile(path.join(site,"src/data/blog/keep.md"),"utf8"),"keep");
    await assert.rejects(stat(path.join(site,"src/data/blog/mc/README.md")),{code:"ENOENT"});
    await put(path.join(source,"post.md"),"updated");
    assert.equal((await syncBlog(source,site)).posts,1);
    await rm(path.join(source,"post.md"));
    assert.equal((await syncBlog(source,site)).posts,0);
    assert.equal(await readFile(target,"utf8"),"updated");
  } finally { await rm(root,{recursive:true,force:true}); }
});

test("workflow commits NBT inputs without force-adding generated assets", async () => {
  const workflow = await readFile(new URL("../workflows/sync-astro-paper.yml", import.meta.url), "utf8");
  assert.match(workflow, /git add src\/data\/mc\/structures/);
  assert.doesNotMatch(workflow, /git add -f public\/pagefind/);
});
