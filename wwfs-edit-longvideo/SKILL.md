---
name: wwfs-edit-longvideo
description: Wallace Wang Financial Services (WWFS) 的 YouTube 长视频 AI 精剪助手。负责把 Wallace 录好的 20 分钟级别 YouTube 中文原片,通过 "SRT 转写 → 剪前音量峰值归一化 → Claude 精剪决策 → pyJianYingDraft 生成剪映草稿" 的 pipeline,自动化删掉口误/重复/废话/跑题,产出一个可直接在中文剪映(Windows 版)里打开微调的精剪草稿。当 Wallace 请求 "帮我剪视频"、"精剪 YouTube"、"把这个视频剪了"、"删掉口误和废话"、"用 AI 剪辑"、"生成剪映草稿"、"自动剪辑"、"长视频精剪"、"导出 SRT 之后呢"、"我的口播稿 + 视频怎么剪",或提到 pyJianYingDraft、剪映草稿、draft_content.json、Whisper、SRT 字幕、Jianying、CapCut、音量拉满、音量太小、normalize audio 等关键词时,务必使用此 skill。也适用于 Wallace 给了 SRT 文件或口播稿、想跑一遍精剪流程、剪辑脚本报错调试、剪映草稿打不开排查、版本兼容问题等场景。本 skill 会主动确认剪映版本、视频路径、草稿目录、SRT 来源,先把视频音量安全拉到接近最大,采用**两阶段精剪流程**(Pass 1: 按字幕序号列 NG 给 Wallace 肉眼 review → Pass 2: 拍板后才生成 keep_segments JSON),严格输出可直接喂给 Python 脚本的 JSON,并提醒 Wallace 先用短视频测试再跑长视频。也适用于 Wallace 只想做"NG 识别 review"、"对照口播稿找重录"、"列出该删的口误"这类中间步骤,不一定要走完整 pipeline。
---

# WWFS YouTube Video Editing Skill

负责把 Wallace 的 YouTube 长视频(默认 20 分钟左右、中文口播)通过 AI pipeline 精剪成可直接在**中文剪映 Windows 版**打开的草稿。

## 目标用户场景

Wallace 录完一期 YouTube 视频,原片有口误、重复、卡顿、跑题。希望通过 Claude + Python 自动化:
- 输入:原始视频 + SRT 字幕 (+ 可选:口播稿)
- 输出:剪映草稿箱里一个已经精剪好的项目,Wallace 打开后只需要加 BGM/字幕特效/片头片尾,然后导出

## 整体 Pipeline

```
原始视频 (.mp4)
   ↓
获取 SRT (剪映自带字幕识别 / Whisper / 飞书妙记 任选一)
   ↓
剪前音量峰值归一化 (把原片音频安全拉到接近最大)
   ↓
Pass 1: Claude NG Review (按字幕序号列出该删的句子, Wallace 肉眼 review)
   ↓
Pass 2: Claude 生成 keep_segments JSON (Wallace 拍板后)
   ↓
Python (pyJianYingDraft) 读 JSON 生成草稿
   ↓
打开剪映 → 草稿箱已有精剪版本 → 手动加 BGM/字幕/片头片尾 → 导出
```

## 标准操作流程 (SOP)

### Step 0: 先和 Wallace 确认这些信息

不要默认任何参数,先用 `ask_user_input_v0` 或直接问清楚:

1. **SRT 来源**:剪映自带识别 / Whisper / 已有逐字稿
2. **剪映版本**:专业版还是普通版?版本号?(`pyJianYingDraft` 对版本敏感,推荐专业版 5.9 左右)
3. **视频路径**:原始 .mp4 文件的完整 Windows 路径
4. **草稿目录**:让 Wallace 按 `Win+R` 输入 `%USERPROFILE%\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft` 验证一下是否存在,不存在就找另一个常见路径 `%USERPROFILE%\AppData\Local\JianyingPro Drafts`
5. **是否第一次跑**:第一次必须用 1-2 分钟的测试片先验证,不能直接上 20 分钟原片

### Step 1: 获取 SRT

**最省事路径(推荐 Wallace 用这个):**
剪映内置「识别字幕」→ 导出 SRT。完全不用装 Whisper。

**备选路径:**
- Whisper 本地:`pip install openai-whisper` + `winget install ffmpeg`,跑 `whisper video.mp4 --language Chinese --model medium --output_format srt`
- 飞书妙记 / 通义听悟:网页上传导出 SRT
- WhisperX 强制对齐:如果 Wallace 有精确口播稿,用这个把稿子和视频对齐拿到精确时间戳

### Step 1.5: 剪辑前先把视频音量调到最大

在任何剪辑、切段、生成剪映草稿之前,先对原视频做一次**安全峰值归一化**:

- 目标:把整条视频的最大音量峰值抬到约 `-1 dB`,听起来尽量大,同时保留 1 dB headroom 防止爆音。
- 不要用剪映里手动拖音量当主流程;先生成一个标准化后的源文件,后续所有剪辑都使用这个新文件。
- 优先运行本 skill 的 `scripts/normalize_audio.py`:

```bash
python scripts/normalize_audio.py "原视频路径.mp4" --output "原视频路径.normalized.mp4"
```

脚本会用 ffmpeg 的 `volumedetect` 读取 `max_volume`,自动计算增益,并只重编码音频、复制视频流。成功后,把后续 `VIDEO_PATH`/`source_video` 改成 `.normalized.mp4`。如果脚本提示视频已经接近目标峰值,仍然可以继续用原片;但默认建议用输出的 normalized 文件,保证每次 pipeline 行为一致。

### Step 2: 让 Claude 精剪(本 skill 的核心)—— 两阶段流程

⚠️ **重要**:不要一步到位让 Claude 直接吐 `keep_segments` JSON。Wallace 看不到 JSON 里到底剪了什么,等剪映打开发现剪错了再回来调代价太大。

正确流程是**两个 pass**:

- **Pass 1 — NG Review**:Claude 按 SRT 字幕序号列出**所有该删的句子**,人话写出来,Wallace 肉眼 review、标歧义点
- **Pass 2 — JSON 生成**:Wallace 拍板之后,Claude 才把"保留段落"转成 `keep_segments` JSON 喂给 Python

---

#### Pass 1: NG Review(人话对照表)

**前提**:必须**同时拿到 SRT + 口播稿**才能跑这一 pass。只有 SRT 没法判断哪句是 keeper(口误重录后 Wallace 自己也常忘),只有口播稿没时间戳。

Prompt 模板:

```
你是 Wallace 的 YouTube 视频剪辑师。下面是一期视频的 SRT 转写 + Wallace 的精确口播稿。

你的任务:对比 SRT 和口播稿,找出 SRT 里**所有该删的 NG 句子**——
也就是口误、卡壳、重启、重录、说错单词、说反逻辑、连续重复同一句的那些。

输出要求:
1. **按口播稿的 block 结构分组**(HOOK / PAIN POINT / BLOCK 1 / BLOCK 2…/ CTA),每组下面列该 block 里的 NG
2. 每条 NG 用这个格式:
   - **字幕序号**:原文(简短引用) → 被哪几条字幕重录 / 说明什么问题
   例:**29–30**:"however here's the thing that didn't really tell you / that account that exactly" → 被 31–33 重录
3. 遇到**两个版本都说得通、不确定哪条是 keeper** 的歧义点,单独列在最后一节 ⚠️ 标记,让 Wallace 自己听原视频拍板
4. 常见 NG 模式必须全抓出来:
   - "so so / and and / I'm not I'm not" 这种结巴重启
   - 整段重录(说一遍后停下来从头再说一遍)
   - 单词说错后立刻纠正("consecutively → conservatively"、"bond money → borrowed money")
   - 数字/术语说反("15 percent" 说成 "fifth percent"、"can short sell" 漏掉 "short")
   - 半句卡住没说完就重启的(以 "and the / so the / but" 结尾)
5. **不要**输出 JSON,这一步就是给人看的 markdown 对照表

【口播稿】
(粘贴完整口播稿)

【SRT 内容】
(粘贴完整 SRT)
```

把 Claude 的输出直接发给 Wallace,等他 review。常见反馈:
- "这条不算 NG,我故意停顿强调的" → 标记为保留
- "歧义点 1 听了原片,留 118–119" → 记录决定
- "你漏了 XXX 段也是重录" → 补充进列表

迭代到 Wallace 说"OK 就这么剪"为止。

---

#### Pass 2: 生成 keep_segments JSON

Wallace 拍板后,用这个 prompt 把 Pass 1 的删除决定**反过来**转成保留段:

```
基于刚才确认过的 NG 列表,现在生成喂给 pyJianYingDraft 的 JSON。

规则:
- 把所有**不在 NG 列表里**的字幕段合并成连续的 keep_segments
- 相邻字幕(前一条 end == 后一条 start,或差 <0.5 秒)合并成一段,避免几百个碎片
- 每段的 text 字段写一句话摘要,方便 Wallace 在剪映里识别

⚠️ 严格只输出 JSON,不要任何解释文字、不要 markdown 代码块包裹:
{
  "keep_segments": [
    {"start": "00:00:00,000", "end": "00:00:28,833", "text": "Hook + 自我介绍"},
    {"start": "00:00:30,000", "end": "00:02:15,400", "text": "Pain Point 银行默认配置"}
  ],
  "total_kept_seconds": 数字,
  "estimated_final_duration_minutes": 数字,
  "ng_segments_removed_count": 数字
}
```

保存为 `plan.json`(UTF-8 无 BOM),进 Step 3。

### Step 3: 跑 Python 脚本生成草稿

让 Wallace 装依赖:
```bash
pip install pyJianYingDraft
```

然后用本 skill 内置的 `scripts/cut.py`(见同目录 scripts/ 文件夹)。Wallace 只需要改顶部三行配置:
- `VIDEO_PATH` — **音量归一化后的**视频完整路径,也就是 Step 1.5 生成的 `.normalized.mp4`;只有在音量已经合适或 ffmpeg 不可用时才用原视频路径
- `PLAN_JSON` — Claude 输出的 JSON 路径
- `DRAFT_FOLDER` — 剪映草稿目录

运行 `python cut.py`,完成后剪映草稿箱会出现 `AI精剪_MMDD_HHMM` 的新项目。

### Step 3.5: 气口压缩 + 重复残留扫描(v3 新增,必做)

2026-06 的 TFSA 一期验证过:只按句子选 keep 段会留下大量气口(呼吸停顿)和少量重录残留。生成草稿前后必须跑这两步,参考实现都在本 skill 的 `scripts/`(注意:这些脚本顶部的素材路径/CLIPS 列表是按单期视频硬编码的,新视频要改配置区):

**A. 气口压缩(解决"视频很拖、能听到喘气")——Wallace 拍板的节奏标准(2026-06-12)**

Wallace 的规则:**每句话说完,近零分贝的尾巴全删;下一句开口前的吸气声必须消失**。

1. `detect_silence.py` — ffmpeg 对每个素材跑 `silencedetect=noise=-32dB:d=0.30`(加 `-vn` 跳过 4K 视频解码,很快),存 `silences.json`(只用于段首尾修边)
2. 构建脚本(`build_v3.py`)在拼接时:
   - **内部停顿以 Whisper 词间隙为准**:gap > **0.30s** 一律压缩,切点 = 前词尾 **+0.14s**(只留词的自然衰减)/ 后词头 **-0.05s**
   - **吸气声的去法**:吸气总是紧贴下一句的起音,不需要识别它——恢复点贴到词头前 0.05s,吸气自然落在被删区间里。⚠️ **切点定死在词边界,绝不能用静音区间放宽恢复点**——静音检测把吸气当"有声音",会把恢复点放到吸气前面,吸气就漏回来了(v3 的气口残留就是这么来的)
   - **段首尾按静音边界收紧**(开头留 0.05s、结尾留 0.14s),且被词边界硬钳制
   - ⚠️ **不能只信 ffmpeg 静音检测找停顿**——呼吸声响度常在 -32dB 以上,纯音频驱动会漏掉一大半气口(实测 26/53 处漏掉)
3. **句中/句尾两档规则(Wallace 2026-06-12 终版)**:一句话内部 0.2-0.5s 的小停顿是说话韵律,**不能**和句间死气口用同一规则。用字幕标点判断句子边界——词尾带 `.?!` = 句尾(>0.30s 狠剪,留 0.14+0.05);逗号/无标点 = 句中(**>0.70s 才剪**,留 0.15+0.08);停顿 >1s 时即使无标点也按句尾兜底
4. **能量包络兜底层(必加)**:词时间戳会撒谎(假长词占着死区),静音检测也会撒谎(呼吸声)——最后一道修剪直接用 RMS 包络(10ms 窗,-44dB 阈值):每段结尾从最后一个有声帧往后只留 0.12s;段内真零分贝区按句中/句尾两档切。实测一轮清掉 67 处段尾尾巴 + 26.6s 死气
5. `gap_check.py` + 构建时自动验证:任何片段内部不得有 ≥0.7s 的零分贝区
6. QC 回转写如果出现残词/吞字,说明切到起音了,放宽对应处
7. **相邻无间隙的重复词(如 "cash, cash")不要剪**——两词之间没有缝,切点必伤其一,会制造更难听的伪影;这种本来就像强调("many, many years"),保留。同理,QC 扫描里两个 token 时间戳重叠(0.2s 装俩词)= 转写伪影不是真口吃,先复核再下刀
8. **人声/呼吸判定的终极方案(三代演进,直接用第三代)**:
   - ❌ 一代:纯分贝阈值(-44dB)——切掉弱辅音词尾("returns" 的 s)
   - ❌ 二代:分贝+过零率帧分类(擦音 ZCR≥38 / 浊音尾 ZCR≤20)——救回 s,但 "gamble" 的 "-le" 尾(ZCR 21-36)和呼吸(ZCR 21-37)同区间,帧特征不可分
   - ✅ 三代:**区域生长**——人声帧(>-30dB 或 quiet sibilant)向右连续生长(>-42dB 不断就一直算人声,把词尾全程带上);呼吸和人声之间总隔着真静音,永远并不进人声区;修剪余量窗口里出现**呼吸团**(>-40dB **且 ZCR≥21**;ZCR<21 是词尾浊音衰减如 "gamble" 的 -l,必须放行)就在它前面收刀。包络数据 = 每 10ms 一帧的 (dB, 过零数),5 个 4K 素材全算一遍约 1 分钟,缓存 envelopes2.pkl。⚠️ 不要再加"词尾自动延伸"层——它两次把被删 retake 开头词("so")的起音抓回来,区域生长已覆盖其用途
9. **构建时必须跑 clipped-word 验证器**:列出所有落在词内的 piece 边界,逐条核对是有意切点(假长词内的 NG 落刀)还是误伤(注意 Whisper 词尾普遍偏晚 ~0.2s,段尾 tail 标记多为假警报,真相以能量+QC 转写为准)
10. **哨兵词验收**:QC 转写后核对句尾词是否完整("gamble" 被切会转写成 "get")——挑 10 个左右句尾词 grep 计数,一个都不能少
11. **切点审计(`boundary_audit_qc.py`,必跑)**:所有"开头/结尾不对"类问题只可能发生在切点(段中间是原片连续播放)。对每个 piece 交界用 **QC 转写**(不是原始转写,会被脏时间戳骗)打印切口前后各 5 词,自动标记悬空连接词(and/so/but/or 结尾且无句号)。判定规则(2026-06-13 被 Wallace 纠正过):**切口前的连接词 + 切口处源片大跨度跳跃(>2s,说明删过内容)= 高危,默认删**——它多半是被删重录的开头词漏在了上一段尾巴上;只有源片连续(纯停顿压缩切口)时才是"连接词属下一句"的假警报。⚠️ QC 转写在跳切处时间戳会错乱(词间出现 2 秒假空洞),疑似空洞用 `probe_wav.py` 实测能量包络定真伪
11b. **剪映字幕空档检测(Wallace 发明,第 7 道,发布前必做)**:Wallace 发布前本来就要在剪映里对终稿跑"识别字幕"——此时字幕轨上**有声音却没字幕块的空档 = 嫌疑残渣**(识别引擎拼不出词的孤词碎片/含声呼吸),在时间线上肉眼可见。让 Wallace 右上角导出 SRT → `srt_gap_check.py <srt>` 自动列出所有 ≥0.4s 的字幕空档并映射回源片 → 逐个判断。TFSA 一期此法抓出 5 处 Whisper 全漏的问题(全在 verbatim 漏听盲区):"so the diff" 假起头、"highest volatility" 整句重录、"So just flip it" 重复、"Five blocks" 错误结尾 take、"very," 半词碎片。⚠️ 空档也可能只是正常停顿(不是残渣),剪映 cue 时间还会被挤压错位——**它只出嫌疑清单,不直接当刀位**
11c. **下刀前的最终仲裁纪律(2026-06-13 血泪)**:QC 转写会脑补惯用虚词("more so in the past" 的 "so" 纯属幻觉,差点为它切伤 "more.")。**任何 DROP 坐标必须先 `verbatim_zone.py <clip> <t0> <t1>` 对源片逐字仲裁**,确认目标词真实存在、起止时间准确,再写坐标。嫌疑来源(QC 扫描/SRT 空档/审计标记)只负责"指哪里",verbatim + 能量探针负责"是什么、切哪里"
12. 收敛标准(实测 15 轮):口吃扫描清零(同一处连续两轮出现才判真,单轮=转写伪影)+ 哨兵词无缺 + 片内死区 ≤0.7s + 切点审计无真悬空词 + 句尾实测缝隙 ~0.2-0.3s。**每次构建必跑全套 6 道检测**(口吃×2、哨兵词、死区、词边界、切点审计)——问题池从第一版就固定,检测器弱于人耳就会"每版都有问题",检测器齐了第一版就该是终版质量

**B. 重复残留扫描(解决"还是有重复的地方")**

1. `find_dups_v2.py <pieces文件>` — 对最终时间线扫 5 词逐字重复 n-gram
2. `find_retakes_fuzzy.py` — 90 秒窗口内模糊相似度 ≥0.55 的改写重述(抓换了措辞的重录)
3. 对每个命中**逐条人工判断**,常见误报(应保留):目录页 vs 章节标题("number one..." 出现两次)、刻意平行讲解(covered call vs put)、口头禅。真重录特征:同 clip 内相隔 <60s、措辞几乎一致、不是结构句
4. 确认要删的加进 `build_v3.py` 的 `DROP_RANGES`(clip 名, 源片秒起, 秒止)重建,不要去剪映里手删
5. 给 Wallace 出一份带最终时间线时间点的复查报告(参考 ai_cut 目录的 `v3_复查报告.md` 格式),标出 ⚠️ 建议重点听的位置

文字扫描抓不到**内容层面的重述**(同一观点换话再讲)——那要靠 Pass 1 对照口播稿,或 Wallace 听完报时间点反查。

**C. 回转写质检(Wallace 提出的方法,2026-06-11 实测必做)**

⚠️ **原始转写是不可信的**:faster-whisper 开 `vad_filter=True` 会吞掉轻声填充词("So... So..." 起头重启),还会把整句重录**合并成一个词**(信号:某个词的时长异常拉长,如 "a" 占 1.4 秒、"decade" 占 2 秒——里面藏着一遍假起头)。所以基于原始转写的文字扫描有盲区,成片必须用音频回转写来验收:

1. `render_qc_audio.py <pieces文件>` — ffmpeg 按 pieces 把成片**音频**拼出来(16kHz mono wav,只抽音频很快,不用导出视频)
2. `transcribe_qc.py <wav>` — faster-whisper 回转写,**必须 `vad_filter=False` + `condition_on_previous_text=False`**(让填充词和口吃如实出现),然后自动跑两个扫描:同词连续(so so / not not)+ ABAB 双词口吃(so if so if / like a like a)
3. 命中的口吃用 QC 词时间戳映射回源片(`map_stutters.py`),加进 `DROP_RANGES` 重建,再跑一轮回转写直到干净。⚠️ Whisper 每次转写有随机差异,每轮会暴露**不同的**漏网口吃,实测要迭代 2-3 轮才收敛(TFSA 一期:第一轮抓 8 处、第二轮又抓 3 处、第三轮干净)
4. 注意:`render_qc_audio.py` 的 qc_tmp 缓存按 piece 序号存,**pieces 变了必须先删 qc_tmp 和 qc.wav** 再重跑;"many, many years" 这类强调式重复是正常的,别剪

**D. 嫌疑词扫描 + 逐字模式(2026-06-12 新增,Wallace 听出三连 "so" 后倒查出来的方法)**

普通设置的 Whisper(连 QC 回转写也一样)会把连续假起头**规整化**:"So your TF— so your, so your TFSA..." 三次起头会被转成一个 "So" + 一个时长 2.7 秒的假 "TFSA",文字上完全看不出来,回转写扫描也会被骗。两个对策:

1. `suspect_scan.py` — 扫原始转写里**时长 >1.4 秒的词**(正常词不会这么长;拉长 = 里面吞了重录或长停顿),对每个嫌疑词 ±4 秒用**逐字模式**重转写:`vad_filter=False` + `initial_prompt="Umm, so, so, so... like, hmm, okay, uh, I mean..."`(填充词提示让 Whisper 如实写出口吃)。TFSA 一期 18 个嫌疑词里挖出 **12 处隐藏假起头/废话**,包括开头的三连 so
2. QC 回转写(`transcribe_qc.py`)也要带同样的 initial_prompt
3. 嫌疑词也可能只是时间戳脏(内容正常)或真实拖长音,逐字结果要人工判断;verbatim 模式偶尔整段漏听,用能量包络(`dead_zone_check.py` 思路,100ms RMS >-38dB)兜底确认该区域是否真有语音
4. 假起头的典型模式(供判断):同一短语连说 2-4 次,每次稍长(\"the hack number, / the hack number two, / the hack number two, holding...\"),keeper 几乎总是**最后一遍**;说错词自我纠正(account→amount)也算,删前一遍

**修边铁律**:静音检测(-32dB)会把轻声词(比如句首轻轻说的 "So")误判为静音,修边切点必须被词边界硬性钳制(首词前 ≥0.08s、尾词后 ≥0.12s),否则会切进词中间。

**剪映开着时草稿目录被 `.locked` 锁住**,`create_draft(allow_replace=True)` 会 PermissionError——换个新草稿名(加 b/c 后缀)绕开,顺便方便对比。

### Step 4: 打开剪映微调

Wallace 检查精剪结果,加 BGM、字幕特效、片头片尾,然后导出。本 skill 不负责这部分(剪映 UI 操作)。

## 关键坑提醒(必须主动告诉 Wallace)

0. **不要跳过 Pass 1**——直接让 Claude 一步生成 JSON,看不见每一句的去留,等剪映里发现剪错了再回来调代价巨大。**有口播稿就一定要走两阶段流程**。Pass 1 的对照表本身就是一份可以单独存档的"剪辑决策记录",出问题能回查。

1. **第一次跑必须用短视频测试**——拿 1-2 分钟的测试片走完整 pipeline,确认草稿能在剪映打开。直接上 20 分钟视频出错会浪费大量时间。

2. **剪映版本锁定**——`pyJianYingDraft` 对剪映版本敏感,推荐**剪映专业版 5.9 左右**。如果 Wallace 升级了剪映,可能需要等库适配,所以暂时**不要自动更新剪映**。

3. **草稿目录可能不一样**——不同剪映版本/语言会用不同目录,主要这两个:
   - `%USERPROFILE%\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft`(中文专业版常见)
   - `%USERPROFILE%\AppData\Local\JianyingPro Drafts`(老版本)
   先打开剪映新建一个空项目,然后去这两个路径看哪个里有新文件夹,就用哪个。

4. **Claude 输出必须是纯 JSON**——不能有 markdown 围栏、不能有解释文字,否则 `json.load()` 会挂。Prompt 里强调过了,但每次都要主动检查。

5. **20 分钟 SRT 大约 5000-8000 字**——Claude 单次能处理,但要确认 Wallace 用的 Claude 模型有足够 context。如果超长(>30 分钟视频),分段处理。

6. **时间戳精度**——SRT 时间戳精度到毫秒就够,Python 脚本里转成微秒喂给 pyJianYingDraft。

## 给 Wallace 的口语化解释

Wallace 不一定熟悉 Python 工具链。如果他问 "Whisper 是什么"、"pyJianYingDraft 怎么装"、"SRT 长什么样" 这种基础问题,用大白话解释,不要堆术语。优先推荐他用**剪映自带字幕识别**这条最省事的路径,而不是先去装 Whisper。

## 迭代和反馈

精剪质量取决于 Claude 的判断。如果 Wallace 反馈:
- "剪太狠了,把 XX 段也剪了" → 在 prompt 里追加"保留 XX 类内容"
- "没剪干净,还是有废话" → 让 Claude 输出"删除段落"列表对照,或者降低保留阈值
- "节奏不对" → 让 Claude 输出每段的衔接说明,或者改成"保留 + 转场点"双输出

每次跑完,主动问 Wallace 反馈,迭代 prompt。

## 不在本 skill 范围

- 剪映 UI 内的操作(加 BGM、字幕特效、调色)——这部分让 Wallace 手动
- 视频导出/上传 YouTube——不自动化
- Shorts 切片(从长视频切多个短视频)——这是另一种玩法,如果 Wallace 要做,单独写 skill 或扩展本 skill
