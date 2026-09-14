# Obsidian-huizhi

个人笔记仓库

---

| 目录              | 说明           |
| --------------- | ------------ |
| `Blog/`         | 博客文章         |
| `Code-snippet/` | 代码片段         |
| `Essay/`        | 随笔、日/周记      |
| `Project/`      | 项目资料、方案和阶段记录 |
| `Study-Notes/`  | 学习笔记、知识整理    |

---

Last updated : 2026-05-24

## 博客同步

修改 `Blog/Note/` 或手动运行 Sync AstroPaper Blog 后，Actions 按内容增量复制：

- Markdown → Astro-Paper 的 `src/data/blog/`（排除 `mc/`、`blog-assets/`）。
- `Blog/Note/blog-assets/` → `public/blog-assets/`。
- `Blog/Note/mc/` 中的 NBT → `src/data/mc/structures/`，保留子目录。

同步不删除目标端文件，不覆盖 `src/data/mc/resources/`，不提交构建产物。删除或重命名源文件后，如需删除旧文章或旧结构，应在博客仓库单独处理。博客构建成功后才提交推送。

验证同步脚本：`node --test .github/scripts/sync-astro-paper.test.mjs`（Node.js 24）。
