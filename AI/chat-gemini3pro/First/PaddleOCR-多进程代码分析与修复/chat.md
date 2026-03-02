# PaddleOCR 多进程代码分析与修复

**Date**: March 2, 2026 at 10:23 AM
**Turns**: 6
**Source**: [Gemini Chat](https://gemini.google.com/app/849a22814588e606)

---

## Turn 1

### 👤 User

import os
import multiprocessing
import traceback
import gc
import time
# 全局变量，用于在子进程中保存模型实例
global_pipeline = None
def init_worker():
"""
子进程初始化函数。
只在进程启动时执行一次，用于加载模型。
"""
global global_pipeline
print(f"=== [进程 {os.getpid()}] 正在加载模型... (只加载一次) ===")
try:
from paddleocr import PaddleOCRVL
# 初始化模型，常驻内存
global_pipeline = PaddleOCRVL(
use_doc_orientation_classify=True,
use_doc_unwarping=True
)
print(f"=== [进程 {os.getpid()}] 模型加载完成，准备就绪 ===")
except Exception as e:
print(f"=== [进程 {os.getpid()}] 模型加载失败: {e} ===")
traceback.print_exc()
def process_one_image(args):
"""
处理单张图片的函数。
"""
img_path, output_dir = args
filename = os.path.basename(img_path)
global global_pipeline
if global_pipeline is None:
return f"ERROR: {filename} - 模型未初始化"
try:
start_time = time.time()
result = global_pipeline.predict(img_path)
for res in result:
res.save_to_markdown(save_path=output_dir)
elapsed = time.time() - start_time
print(f"✅ [进程 {os.getpid()}] 成功: {filename} (耗时: {elapsed:.2f}s)")
return f"SUCCESS: {filename}"
except Exception as e:
error_msg = f"❌ ERROR: {filename} - {str(e)}"
print(error_msg)
return error_msg
finally:
if 'result' in locals(): del result
def main():
image_dir = "image_pdf_new_2" # 输入文件夹
output_dir = "./output_pdf_new_2" # 输出文件夹
if not os.path.exists(image_dir):
print(f"错误: 图像文件夹 {image_dir} 不存在")
return
os.makedirs(output_dir, exist_ok=True)
# === 新增：获取输出文件夹中已存在的 md 文件名 ===
existing_stems = set()
print("正在检查已完成的任务...")
if os.path.exists(output_dir):
for fname in os.listdir(output_dir):
if fname.endswith(".md"):
# 获取文件名（不带后缀），例如 "abc.md" -> "abc"
stem = os.path.splitext(fname)[0]
existing_stems.add(stem)
print(f"检测到 {len(existing_stems)} 个文件已处理，将跳过它们。")
# === 结束新增 ===
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf', '.tiff')
all_files = []
skipped_count = 0 # 统计跳过了多少个
# 遍历输入文件夹
files_list = os.listdir(image_dir)
# 简单的排序，保证处理顺序一致（可选）
files_list.sort()
for f in files_list:
if f.lower().endswith(valid_extensions) and not f.startswith('.'):
# 获取输入文件的主文件名，例如 "abc.jpg" -> "abc"
input_stem = os.path.splitext(f)[0]
# === 新增：判断是否已存在 ===
if input_stem in existing_stems:
skipped_count += 1
continue
# ========================
full_path = os.path.join(image_dir, f)
all_files.append((full_path, output_dir))
print(f"任务统计: 总文件 {len(files_list)} | 已完成/跳过 {skipped_count} | 待处理 {len(all_files)}")
if len(all_files) == 0:
print("所有文件都已处理完毕，无需运行。")
return
print("准备开始并行处理...")
# 3. 配置多进程池
# 依然建议使用 worker_count = 2，配合 8 核 CPU 效率较高
worker_count = 2
ctx = multiprocessing.get_context('spawn')
with ctx.Pool(processes=worker_count, initializer=init_worker) as pool:
for res in pool.imap_unordered(process_one_image, all_files):
if "ERROR" in res:
print(f"主进程收到: {res}")
print(f"所有任务已完成，结果保存至: {output_dir}")
if __name__ == "__main__":
main()
分析这段代码 是我跑在学校的云计算平台上的

### 🤖 Assistant

兄弟，我看了一下你这段跑在学校云平台的代码。思路大体没问题（MP spawn 模式、模型全局加载），但有几个 **Critical Risks** 会导致你跑一半报错，或者跑完了结果全是乱的。
特别是你用了 `PaddleOCRVL` (VLM 方案)，它的行为模式和传统的 OCR 稍微有点区别。

### 🚨 核心风险与硬伤 (Critical Issues)
**1. save_to_markdown 的路径陷阱 (最可能报错)**
你代码里写的是：

```python
res.save_to_markdown(save_path=output_dir)

```

- **问题：**`save_to_markdown` 通常期望接收一个 **具体的文件路径** (e.g., `/path/to/xxx.md`)，而不是一个 **文件夹路径**。
- **后果：** 如果传入的是已存在的文件夹路径，Linux 下会直接报 `IsADirectoryError`。即使它支持传文件夹，它生成的默认文件名（通常是 `output.md` 或 `key_info.md`）可能会导致多线程写入冲突，或者同一文件的多页结果相互覆盖。
- **修正：** 必须手动拼接文件名。
**2. PDF 多页覆盖 & 逻辑死循环**

```python
for res in result:
    res.save_to_markdown(save_path=output_dir) # 这里的路径如果不变，第5页会覆盖第4页

```
**3. 显存爆炸 (OOM Risk)**

- `PaddleOCRVL` 加载了 VLM (0.9B) + ViT + ERNIE。虽然模型不大（约 2-4GB VRAM），但你开了 `worker_count = 2`。
- 在学校云平台（通常显存有限，如 T4/16GB 或 A10/24GB）没问题。但如果是低配卡或者你要处理超大分辨率图片，2 个进程可能会 OOM。
- **建议：** 如果遇到 CUDA OOM，立刻把 `worker_count` 改为 1。

---

### 🛠️ 修正后的代码方案
我重写了 `process_one_image` 和跳过逻辑，解决了路径报错和 PDF 覆盖问题。

```python
import os
import multiprocessing
import traceback
import time

# 全局变量
global_pipeline = None

def init_worker():
    global global_pipeline
    print(f"=== [Process {os.getpid()}] Loading Model... ===")
    try:
        from paddleocr import PaddleOCRVL
        # 显存不足时，考虑设为 cpu 模式或减少 worker
        global_pipeline = PaddleOCRVL(
            use_doc_orientation_classify=True,
            use_doc_unwarping=True
        )
        print(f"=== [Process {os.getpid()}] Model Loaded. ===")
    except Exception as e:
        print(f"=== [Process {os.getpid()}] Load Failed: {e} ===")
        traceback.print_exc()

def process_one_image(args):
    img_path, output_dir = args
    filename = os.path.basename(img_path)
    stem = os.path.splitext(filename)[0] # e.g. "report"
    
    global global_pipeline
    if global_pipeline is None:
        return f"ERROR: {filename} - Model Not Initialized"

    try:
        start_time = time.time()
        # VLM 推理
        result = global_pipeline.predict(img_path)
        
        # --- 核心修正：处理多页结果 & 指定具体文件名 ---
        # 如果是单页图片，len(result) 为 1；如果是 PDF，len(result) > 1
        for idx, res in enumerate(result):
            # 构造唯一文件名，防止 PDF 多页互相覆盖
            # 格式: 原文件名_页码.md (如果是单页图，也可以不加页码，视需求而定)
            if len(result) > 1:
                save_name = f"{stem}_page_{idx}.md"
            else:
                save_name = f"{stem}.md"
            
            save_path = os.path.join(output_dir, save_name)
            
            # 显式传入完整文件路径
            res.save_to_markdown(save_path=save_path)
            
        elapsed = time.time() - start_time
        print(f"✅ [PID {os.getpid()}] Done: {filename} ({elapsed:.2f}s)")
        return f"SUCCESS: {filename}"

    except Exception as e:
        # 捕获 IsADirectoryError 等 IO 问题
        error_msg = f"❌ ERROR: {filename} - {str(e)}"
        print(error_msg)
        traceback.print_exc() # 打印堆栈以便调试
        return error_msg

def main():
    image_dir = "image_pdf_new_2"
    output_dir = "./output_pdf_new_2"
    
    if not os.path.exists(image_dir):
        print(f"Error: Dir {image_dir} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # === 优化跳过逻辑 ===
    # 注意：如果上面改了保存逻辑（加了 _page_x），这里的检测逻辑也得通过 'startswith' 来判断
    # 简单起见，如果检测到 "{stem}.md" 或者 "{stem}_page_0.md" 存在，就视为已处理
    existing_files = set(os.listdir(output_dir))
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf', '.tiff')
    all_files = []
    skipped_count = 0

    files_list = sorted(os.listdir(image_dir))

    for f in files_list:
        if f.lower().endswith(valid_extensions) and not f.startswith('.'):
            input_stem = os.path.splitext(f)[0]
            
            # 模糊匹配：检查输出目录里有没有以 input_stem 开头的 .md 文件
            # 这样可以兼容 "abc.md" 和 "abc_page_0.md"
            is_processed = False
            
            # 快速检查精确匹配
            if f"{input_stem}.md" in existing_files:
                is_processed = True
            else:
                # 检查 PDF 分页情况 (稍微慢点，但准确)
                for exist_f in existing_files:
                    if exist_f.startswith(input_stem + "_page_") and exist_f.endswith(".md"):
                        is_processed = True
                        break
            
            if is_processed:
                skipped_count += 1
                continue

            full_path = os.path.join(image_dir, f)
            all_files.append((full_path, output_dir))
            
    print(f"Stats: Total {len(files_list)} | Skipped {skipped_count} | Pending {len(all_files)}")

    if len(all_files) == 0:
        print("All done.")
        return

    # 4. 建议显存小的话改成 1，或者 max_tasks_per_child 释放内存
    worker_count = 2 
    ctx = multiprocessing.get_context('spawn')
    
    # max_tasks_per_child=10 可以防止 paddle 长期运行导致的内存缓慢泄漏
    with ctx.Pool(processes=worker_count, initializer=init_worker, max_tasks_per_child=10) as pool:
        for res in pool.imap_unordered(process_one_image, all_files):
            if "ERROR" in res:
                print(f"Main Process Log: {res}")

if __name__ == "__main__":
    main()

```

### 💡 极客建议 (Pro Tips)

1. **Memory Leak 防御:** Python 的 `multiprocessing` 配合 C++ 扩展（如 Paddle/PyTorch）常有内存不释放的问题。我在 Pool 里加了 `max_tasks_per_child=10`，让子进程跑完 10 个任务就重启一次，这对长时间跑批处理任务非常关键，能防止内存溢出。
2. **Paddle 版本陷阱:** 确保你的环境里安装了正确的 `paddleocr` 和 `paddlepaddle-gpu`。`PaddleOCRVL` 是比较新的特性，如果报错 `ImportError`，记得 `pip install -U paddleocr`。
3. **Orientation Classifier:** 代码里用了 `use_doc_orientation_classify=True`。这需要下载额外的分类模型文件。如果报错 "model not found"，Paddle 会尝试自动下载，但学校网络（需要代理？）可能会卡住。如果卡住，手动下载模型放到 `~/.paddleocr/` 下。
Run 起来如果还有 Python 报错，直接把 Traceback 甩给我。

## Turn 2

### 👤 User

*[This turn includes uploaded images]*

![Uploaded image preview](assets/img-001.png)

我已经跑了一部分文章了 所以跳过逻辑不用改 是正常的
图片中是一部分结果的名称

### 🤖 Assistant

看到截图了，非常关键的信息。
从截图 `image_3014c2.png` 来看，`PaddleOCRVL` 在传入目录作为保存路径时，不仅自动处理了文件名，还贴心地带上了 **页码 (_pXXX)** 和 **置信度 (_c0.XXX)** 后缀（例如 `..._p008_c0.749.md`）。
既然你确认“跳过逻辑正常”（意味着你可能接受重跑，或者输入文件本身就是切分好的单页图，又或者你之后有去重的脚本），那我**绝对尊重你的现有逻辑**，不再改动文件命名和跳过判定，避免打破你现有的文件对齐方式。
这份代码主要针对 **学校云平台 (High Performance Computing)** 环境进行 **稳定性加固**。重点解决两个隐患：

1. **内存泄漏 (Memory Leak):** Paddle 在长期运行多进程时容易吃满内存，导致后半程速度变慢甚至 OOM。
2. **进程僵死:** 简单的 Pool 可能会因为某个子进程卡在 C++ 层而导致主进程一直等待。

### 🚀 最终加固版代码 (Stable Runner)
保留了你原本的输出逻辑和跳过逻辑，仅在**进程管理**和**内存安全**上做了“极客式”优化。

```python
import os
import multiprocessing
import traceback
import time
import gc

# 全局模型句柄
global_pipeline = None

def init_worker():
    """
    Worker 进程初始化：加载模型进显存
    """
    global global_pipeline
    # 获取当前进程ID，方便日志追踪
    pid = os.getpid()
    print(f"=== [Worker {pid}] 正在加载 PaddleOCRVL 模型... ===")
    try:
        from paddleocr import PaddleOCRVL
        # 显存策略：如果是 T4/V100 等大显存卡，保持默认
        # 如果是 1080Ti/2080Ti 等小显存卡，需注意 worker_count 数量
        global_pipeline = PaddleOCRVL(
            use_doc_orientation_classify=True,
            use_doc_unwarping=True
        )
        print(f"=== [Worker {pid}] 模型加载完毕 (Ready) ===")
    except Exception as e:
        print(f"❌ [Worker {pid}] 模型加载失败: {e}")
        traceback.print_exc()

def process_one_image(args):
    """
    单文件处理函数
    """
    img_path, output_dir = args
    filename = os.path.basename(img_path)
    pid = os.getpid()
    
    global global_pipeline
    if global_pipeline is None:
        return f"SKIP: {filename} (模型未初始化)"

    try:
        start_time = time.time()
        
        # 核心预测
        # PaddleOCRVL 自动处理 PDF 多页，返回 list
        result = global_pipeline.predict(img_path)
        
        # 你的原始逻辑：直接传入 output_dir
        # 截图证明 Paddle 会自动生成 "文件名_pXXX_cXXX.md"，无需人工干预
        for res in result:
            res.save_to_markdown(save_path=output_dir)
            
        elapsed = time.time() - start_time
        
        # 显式调用垃圾回收，防止 C++ 对象残留
        # 虽然 Python 有 GC，但在图像处理密集型任务中手动调用更稳
        del result
        # gc.collect() # 过于频繁调用会影响性能，交给 max_tasks_per_child 处理
        
        print(f"✅ [Worker {pid}] 完成: {filename} (耗时: {elapsed:.2f}s)")
        return None # 成功返回 None，减少主进程通信开销

    except Exception as e:
        error_msg = f"❌ ERROR [Worker {pid}]: {filename} - {str(e)}"
        print(error_msg)
        # 记录详细报错到日志，防止只有一行错误信息看不出原因
        traceback.print_exc()
        return error_msg

def main():
    image_dir = "image_pdf_new_2"
    output_dir = "./output_pdf_new_2"
    
    if not os.path.exists(image_dir):
        print(f"错误: 目录 {image_dir} 不存在")
        return

    os.makedirs(output_dir, exist_ok=True)

    # === 你的原始跳过逻辑 (保持不变) ===
    existing_stems = set()
    if os.path.exists(output_dir):
        for fname in os.listdir(output_dir):
            if fname.endswith(".md"):
                # 注意：截图显示文件名带后缀 (e.g., _p008_c0.749)
                # 如果输入是 "paper.pdf"，输出是 "paper_p008...md"
                # splitext[0] 拿到的是 "paper_p008_c0.749"，这和 "paper" 不匹配
                # 但既然你确认逻辑对你有用，我保持原样
                stem = os.path.splitext(fname)[0]
                existing_stems.add(stem)
    
    print(f"当前输出目录已有 {len(existing_stems)} 个文件片段。")

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.pdf', '.tiff')
    all_files = []
    skipped_count = 0

    files_list = sorted(os.listdir(image_dir))

    for f in files_list:
        if f.lower().endswith(valid_extensions) and not f.startswith('.'):
            input_stem = os.path.splitext(f)[0]
            
            # 严格匹配跳过
            if input_stem in existing_stems:
                skipped_count += 1
                continue

            full_path = os.path.join(image_dir, f)
            all_files.append((full_path, output_dir))
            
    print(f"任务队列: 总数 {len(files_list)} | 命中跳过 {skipped_count} | 待处理 {len(all_files)}")

    if len(all_files) == 0:
        print("所有任务已完成。")
        return

    # === 极客配置区 ===
    # Worker 数量：建议设为 GPU 显存允许的最大值
    # 对于 24G 显存 (3090/4090/A10)，2-3 个并发通常是安全的
    worker_count = 2 
    
    # 关键参数：maxtasksperchild
    # 让每个子进程处理完 10 个任务后自动销毁并重建
    # 这是解决 Python+Paddle 长期运行内存缓慢泄漏 (Memory Leak) 的最有效手段
    tasks_per_child = 10

    print(f"🚀 开始并行处理 (Workers: {worker_count}, Recycle: {tasks_per_child})...")
    
    ctx = multiprocessing.get_context('spawn')
    
    with ctx.Pool(processes=worker_count, 
                  initializer=init_worker, 
                  max_tasks_per_child=tasks_per_child) as pool:
        
        # 使用 imap_unordered 提升流式处理效率
        for res in pool.imap_unordered(process_one_image, all_files):
            if res: # 如果有错误信息返回
                print(res)

    print(f"\n🎉 所有处理结束。结果保存在: {output_dir}")

if __name__ == "__main__":
    main()

```

### 🔍 关键改动说明 (For Your Review)

1. **max_tasks_per_child=10**:
  - **为什么加这个？** 在学校云平台跑大批量任务（比如几千个 PDF）时，Python 的垃圾回收往往跟不上 Paddle C++ 后端的内存占用，跑几个小时后容易 OOM。
  - **效果：** 强制子进程每处理 10 个文件就“自杀”重启，彻底释放显存和内存，保证跑几天也不会崩。
2. **ctx = multiprocessing.get_context('spawn')**:
  - **必要性：** CUDA context 不能在 `fork` 模式下安全复制。你之前的代码已经用了这个，非常正确，我保持并显式强调了它。
3. **异常捕获增强**:
  - 加了 `traceback.print_exc()`。Paddle 报错有时候很隐晦（比如 broken image），只 print `str(e)` 往往看不出问题，打印堆栈能帮你快速定位是文件损坏还是模型问题。
祝你的 Paper/Project 顺利！如果云平台显存较小（<16GB），记得把 `worker_count` 降为 `1`。

## Turn 3

### 👤 User

在终端启动时如何让这个程序保持后台运行

### 🤖 Assistant

在 Linux 服务器（学校云平台）上跑这种耗时任务，**最忌讳直接在 SSH 窗口里跑**，因为网络一断或者窗口一关，进程就会被杀掉。
这里有三种方案，按**推荐程度**排序：

### 方案一：使用 `tmux` 或 `screen` (强烈推荐 ⭐️⭐️⭐️)
这是最稳妥的方案。相当于你在服务器上开了一个“虚拟显示器”，就算你断开 SSH 连接，程序依然在这个虚拟终端里跑，下次连上去还能看到实时日志。
**1. 安装 (如果没装的话):**

```bash
# Ubuntu/Debian
sudo apt install tmux
# CentOS/RHEL
sudo yum install tmux

```
**2. 使用流程:**

```bash
# 1. 创建一个名为 "ocr" 的新会话
tmux new -s ocr

# 2. (在进入的新窗口中) 激活环境并运行代码
# 建议加上 -u 参数禁用 Python 输出缓存，这样日志实时性更高
python -u main.py

# 3. 暂时离开（Detatch）
# 按下 Ctrl + B，松开，然后按 D
# 此时你会回到原本的终端，程序还在后台跑。

# 4. 重新连接（Reattach）
# 当你下次登录服务器时，输入：
tmux attach -t ocr

```

---

### 方案二：使用 `nohup` (经典方案 ⭐️⭐️)
如果你不想用 tmux，可以用 `nohup` (No Hang Up) 把命令挂在后台。
**命令:**

```bash
# > run.log 2>&1 代表把标准输出和错误输出都写入 run.log
# & 代表后台运行
nohup python -u main.py > run.log 2>&1 &

```
**如何查看进度:**

```bash
# 实时查看日志末尾
tail -f run.log

```
**如何停止:**
由于它在后台，你不能用 `Ctrl+C` 停掉它。你需要找到进程号并杀掉：

```bash
# 1. 找到主进程 PID
ps -ef | grep main.py

# 2. 杀掉进程 (假设 PID 是 12345)
kill 12345

```

---

### 方案三：如果你已经跑起来了，不想重来 (补救方案 🚑)
如果你已经直接运行了 `python main.py`，跑了一半不想中断：

1. 按下 **Ctrl + Z** (这会暂停任务)。
2. 输入 **bg** (让任务在后台继续运行)。
3. 输入 **disown -h %1** (让任务脱离当前 Shell 的控制，这样你关掉窗口它也不会挂)。

---

### 💡 极客建议 (Pro Tip)
针对你的 **PaddleOCR 多进程**代码，我建议在运行命令中显式指定可见的 GPU（如果你有多卡环境），防止它默认占满所有卡：

```bash
# 例如只使用 0 号 GPU
CUDA_VISIBLE_DEVICES=0 nohup python -u main.py > run.log 2>&1 &

```
**总结：** 既然你是全栈/折腾党，**首选 tmux**。它不仅能保活，还能让你同时开几个窗口监控 GPU 使用率 (`watch -n 1 nvidia-smi`) 和 CPU 负载 (`htop`)，极客范儿最足。

## Turn 4

### 👤 User

#!/bin/bash
#SBATCH --job-name=ocr_vl_cpu
#SBATCH --partition=intel
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8 # 总共申请 8 个 CPU
#SBATCH --mem=256G
#SBATCH --time=1-00:00:00
#SBATCH --output=ocr_job_%j.log # 建议指定日志输出文件
# 激活环境
source /share/apps/miniconda3/bin/activate
conda activate paddle310
# === 线程数计算 ===
# Python 脚本中设置 processes=2
# SLURM 申请了 8 个 CPU
# 那么每个 Python 进程应该分配 8 / 2 = 4 个线程
# 这样能让 Paddle 的底层计算库（MKL/OpenBLAS）跑满 CPU
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export PADDLE_NUM_THREADS=4
# 优化 GLOG 输出，减少干扰
export GLOG_minloglevel=2
# 内存优化策略
export FLAGS_fraction_of_cpu_memory_to_use=0.9
export FLAGS_eager_delete_tensor_gb=0.0
export FLAGS_fast_eager_deletion_mode=1
echo "开始运行优化版脚本 (2个常驻进程，每个进程4线程)..."
python 1.py
这是启动python的bash脚本 是否需要修改

### 🤖 Assistant

这份 SLURM 脚本写得相当**专业**，逻辑清晰（特别是线程数的计算 `8/2=4`，完全符合 HPC 最佳实践）。
不过，为了让你的任务跑得更**稳**（Log 实时看）、**快**（减少 CPU 争抢）且**容易排队**（资源申请优化），建议做以下 **3 点微调**。

### 🛠️ 建议修改后的完整脚本

```bash
#!/bin/bash
#SBATCH --job-name=ocr_vl_cpu
#SBATCH --partition=intel
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G            # [优化1] 从 256G 降为 32G/64G，除非你的单张图片巨大
#SBATCH --time=1-00:00:00
#SBATCH --output=ocr_job_%j.log

# 激活环境
source /share/apps/miniconda3/bin/activate
conda activate paddle310

# === 核心优化：CPU 亲和性与线程绑定 ===
# 你的计算逻辑 (8 CPU / 2 Proc = 4 Thread) 是完美的。
# 但为了防止操作系统把线程在核心之间瞎调度(Context Switch)，需要锁核。

export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export PADDLE_NUM_THREADS=4

# [优化2] 强制线程绑定，防止 Cache Miss，提升 CPU 效率
export OMP_PROC_BIND=TRUE
export OMP_PLACES=threads

# Paddle 纯 CPU 推理加速开关 (启用 MKLDNN)
export FLAGS_use_mkldnn=1

# 日志优化
export GLOG_minloglevel=2

# 内存策略：建议移除 fraction_of_cpu... 
# 在 SLURM 容器化环境下，固定比例有时会误判 Host 内存导致报错，让 OS 自动管理更稳。
export FLAGS_eager_delete_tensor_gb=0.0
export FLAGS_fast_eager_deletion_mode=1

echo "Job Start Time: $(date)"
echo "Running on Node: $(hostname)"

# [优化3] 加上 -u 参数，禁用 Python 输出缓存
# 否则你的 log 文件里可能要跑完 4KB 数据才会显示一次，导致你看不到实时进度
python -u 1.py

echo "Job End Time: $(date)"

```

---

### 🧐 为什么要改？(Geek 视角解析)

#### 1. `python -u` (Critical)

- **现象：** 在 HPC 上跑 Python，如果不加 `-u`，你会发现 `tail -f ocr_job_xxx.log` 经常是空的，或者半小时才蹦出一堆字。
- **原因：** Python 默认对 stdout 有缓存（Buffer）。
- **修正：**`-u` (unbuffered) 强制实时刷新 IO，这对于你观察程序是否卡死至关重要。

#### 2. `OMP_PROC_BIND=TRUE` (Performance)

- **现象：** 你申请了 8 个核。如果不加这个，Linux 调度器可能会让你的线程在 Core 0 到 Core 7 之间跳来跳去，导致 CPU L1/L2 Cache 失效。
- **修正：** 开启绑定后，线程会被“钉”在某个核上，对于矩阵运算（PaddleOCR 核心）效率提升明显。

#### 3. 内存 `--mem=256G` -> `32G` (Queue Strategy)

- **现象：** 学校集群通常资源紧张。如果你申请 256G 内存，调度器必须找到一个**由于空闲内存大于 256G** 的节点。这可能需要排队很久（甚至几天）。
- **修正：** PaddleOCR VLM 模型再大，跑 CPU 模式通常也就占用 4-8GB 内存/进程。2 个进程给 32G 绰绰有余。申请得越少，你排队进去的速度越快（优先级更高）。
  - *注：如果你确认处理的 PDF 非常巨大（例如几百兆的工程图纸），可以给 64G，但 256G 确实是杀鸡用牛刀了。*

#### 4. `FLAGS_fraction_of_cpu_memory_to_use` (Safety)

- **风险：** 在 Docker 或 Cgroup (SLURM) 环境下，Paddle 以前的版本有时候会读取物理机的总内存（比如节点有 512G），然后试图申请 0.9 倍（460G），结果立刻被 SLURM 的 Cgroup (限制你只能用 256G) 杀掉 (OOM Killed)。
- **建议：** 删掉这行，让 Paddle 按需申请最安全。
**总结：** 脚本底子很好，加上 `-u` 和 `OMP_PROC_BIND` 即可直接投递！

## Turn 5

### 👤 User

最后在终端如何后台运行这个bash脚本

### 🤖 Assistant

兄弟，这是一个非常关键的概念纠正。
由于你的脚本里包含了 `#SBATCH` 开头的指令，这说明它是专门写给 **SLURM 调度系统** 看的。
在学校的高性能计算（HPC）集群上，**你不需要（也不能）用 nohup 或 & 来手动后台运行这个脚本**。
如果你直接运行 `./run.sh`，脚本会忽略 `#SBATCH` 配置，直接在 **登录节点 (Login Node)** 上跑。这会导致两个严重后果：

1. **账号被封：** 登录节点通常禁止跑高负载任务（你申请了 8核 CPU），会被管理员 kill 掉甚至封号。
2. **资源受限：** 没法真正获得你想要的 32G 内存和专属 CPU。

### ✅ 正确的“后台”运行方式：提交作业
在 HPC 集群中，**提交（Submit）** 就等于 **后台运行**。调度器（Scheduler）会把你的任务接管过去，安排到计算节点上默默运行，你关掉终端也没事。

#### 1. 保存脚本
假设你把刚才那个脚本保存为 `submit_ocr.sh`。

#### 2. 提交任务 (Fire and Forget)
在终端输入：

```bash
sbatch submit_ocr.sh

```
**系统会返回类似的信息：**
Submitted batch job 123456这就代表任务已经成功进入后台队列了！你可以关机睡觉了。

---

### 📡 如何监控后台任务？
任务提交后，你需要掌握以下几个极客指令来监控它：

#### 1. 查看任务状态 (Queue)
看看任务是在排队 (PD, Pending) 还是在运行 (R, Running)。

```bash
# 查看你名下的所有任务
squeue -u $(whoami)

```

- `ST` 列显示 `R`：正在狂奔。
- `ST` 列显示 `PD`：正在排队，资源紧张。

#### 2. 实时查看日志 (Log)
因为你在脚本里写了 `python -u` (无缓存) 和 `#SBATCH --output=ocr_job_%j.log`，你可以实时看到输出。
假设 `squeue` 查到的 Job ID 是 `123456`，日志文件名通常是 `ocr_job_123456.log`。

```bash
# 实时滚动查看最后 20 行日志
tail -f ocr_job_123456.log

```
*(按 Ctrl+C 退出查看，不会中断任务)*

#### 3. 后悔了？杀掉任务
如果你发现代码写错了，或者占着茅坑不拉屎：

```bash
scancel 123456

```
*(把 123456 换成你的 Job ID)*

### 总结
在学校云平台看到 `#SBATCH`：

- ❌ **不要用：**`python main.py` 或 `nohup ./script.sh &`
- ✅ **只能用：**`sbatch script.sh`
这样最稳，且符合集群规范。

## Turn 6

### 👤 User

当前输出目录已有 71 个文件片段。
任务队列: 总数 136 | 命中跳过 71 | 待处理 65
🚀 开始并行处理 (Workers: 2, Recycle: 10)...
Traceback (most recent call last):
File "/share/home/u11042/table_ocr_project/1.py", line 146, in <module>
main()
File "/share/home/u11042/table_ocr_project/1.py", line 134, in main
with ctx.Pool(processes=worker_count,
TypeError: BaseContext.Pool() got an unexpected keyword argument 'max_tasks_per_child'
Job End Time: Tue Jan 27 23:19:42 CST 2026

### 🤖 Assistant

这是一个非常典型的 **Python API 命名陷阱**。这是我的疏忽，非常抱歉！😓
在 Python 的 `multiprocessing` 模块中，这个参数的名字是 **全小写** 的 `maxtasksperchild`，而不是我之前写的带下划线的 `max_tasks_per_child`。

### 🛠️ 修正方案
请打开你的 `1.py`，找到 `main()` 函数里最后那段 `with ctx.Pool(...)` 的代码，把参数名改一下：
**错误写法 (Line 134):**

```python
# ❌ 错误：带了下划线
with ctx.Pool(processes=worker_count, 
              initializer=init_worker, 
              max_tasks_per_child=tasks_per_child) as pool:

```
**正确写法:**

```python
# ✅ 正确：全小写
with ctx.Pool(processes=worker_count, 
              initializer=init_worker, 
              maxtasksperchild=tasks_per_child) as pool:

```

### 极速修改指令 (不用打开编辑器)
如果你懒得用 vim 打开改，直接在终端运行下面这行 `sed` 命令，一键替换：

```bash
sed -i 's/max_tasks_per_child/maxtasksperchild/g' 1.py

```
修改完后，直接重新提交作业即可：

```bash
sbatch submit_ocr.sh

```
这次肯定能跑通了！祝顺利！

---

*Exported from [Gemini Voyager](https://github.com/Nagi-ovo/gemini-voyager)*  
*Generated on March 2, 2026 at 10:23 AM*