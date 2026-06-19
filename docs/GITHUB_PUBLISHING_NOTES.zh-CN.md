# GitHub 发布与网络排障经验

这份笔记整理了把 `oc-codex-pet-maker` 发布到 GitHub 时踩过的坑。它主要面向以后维护这个项目，或者把类似 Codex 宠物项目开源的人。

## 1. 先控制仓库体积

AI 生成图片、调试图、预览 GIF 和中间产物很容易让 Git 仓库变大。第一次推送前建议先确认哪些内容真的需要公开。

推荐纳入 Git：

- `README.md` 和 `README.zh-CN.md`
- `skill/`
- `scripts/`
- `templates/`
- `docs/`
- 少量精选示例图
- 最终可验证的示例宠物包

不推荐纳入 Git：

- 大量失败实验
- 临时 debug 图
- 反复生成的中间切图
- 过大的视频或动态图
- 含有 API key、token、账号信息的文件

可以用这些命令检查仓库状态：

```bash
git status --short
git log --oneline -3
```

如果 `.git` 已经因为误提交大文件变得很大，要先清理历史，再推送。否则即使后来把文件删掉，Git 历史里仍然可能保留大对象。

## 2. 使用清晰的远端仓库名

这个项目最后使用的仓库名是：

```text
oc-codex-pet-maker
```

比 `codex-pet-maker` 更不容易撞名，也更明确表达用途：帮助用户把自己的 OC 做成 Codex pet。

远端地址格式：

```bash
git remote add origin https://github.com/<your-name>/oc-codex-pet-maker.git
```

## 3. README 要先面向用户

开源仓库的 README 不应该一上来就讲某个具体角色的细节。更好的顺序是：

1. 这个项目是做什么的。
2. 用户怎么安装 Skill。
3. 用户怎么开始创建自己的宠物。
4. Codex 宠物有哪些状态。
5. 如何切图、合成、验证。
6. 再用 Lanxi 作为完整示例。

中文用户较多时，建议同时提供：

```text
README.md
README.zh-CN.md
```

并在两个文件顶部互相链接：

```markdown
[English](README.md) | [中文](README.zh-CN.md)
```

GitHub README 本身不会像单页网站一样原地切换语言，但这种顶部语言切换是最常见、最稳定的形式。

## 4. gh 登录成功不代表 push 一定稳定

可以用 GitHub CLI 检查登录状态：

```bash
gh auth status
```

看到已登录、token 有 `repo` 权限，说明认证一般没有问题。但 `git push` 仍然可能因为网络、VPN 或代理连接被重置。

我们遇到过的错误：

```text
fatal: unable to access 'https://github.com/...': Recv failure: Connection reset by peer
```

这个错误通常更像网络传输问题，而不是仓库权限问题。

## 5. 网络不稳定时的稳定 push 参数

如果普通 `git push` 失败，可以尝试降低 Git HTTP 传输复杂度：

```bash
git -c http.version=HTTP/1.1 \
  -c core.compression=0 \
  -c pack.threads=1 \
  -c http.postBuffer=524288000 \
  -c http.lowSpeedLimit=0 \
  -c http.lowSpeedTime=999999 \
  push
```

这些参数的作用大致是：

- `http.version=HTTP/1.1`：避免某些代理或 VPN 对 HTTP/2 支持不稳定。
- `core.compression=0`：减少压缩开销，避免大包处理时更容易断开。
- `pack.threads=1`：降低并发打包复杂度。
- `http.postBuffer=524288000`：提高 HTTP 发送缓冲区。
- `http.lowSpeedLimit=0` 和 `http.lowSpeedTime=999999`：放宽低速网络超时限制。

如果这个命令成功，之后可以检查：

```bash
git status --short --branch
git ls-remote --heads origin main
```

当本地不再显示 `ahead`，并且远端 `main` 指向最新 commit，就说明已经同步成功。

## 6. VPN 和代理需要单独判断

如果你开了 VPN，GitHub 网页能打开，不代表 Git 命令一定稳定。Git 可能走系统代理、Git 自己的代理配置，或完全不同的网络路径。

可以检查 Git 代理配置：

```bash
git config --global --get http.proxy
git config --global --get https.proxy
```

如果代理端口不稳定，可能会出现网页正常、push 失败的情况。此时可以：

- 暂时关闭 VPN 再试。
- 切换 VPN 节点。
- 使用上面的稳定 push 参数。
- 减小仓库体积后再推送。

## 7. 发布前检查清单

推送前建议检查：

- `git status --short --branch` 是否只包含你准备提交的修改。
- README 是否从用户角度说明了用法。
- 中文 README 是否和英文 README 同步。
- `.gitignore` 是否排除了 debug、中间产物和敏感文件。
- 是否没有把 API key 写进仓库。
- 示例资源是否足够小且有代表性。
- `scripts/validate_pet_package.py` 是否能验证示例包。

## 8. 当前项目的发布策略

这个项目采用“GitHub 项目 + Codex Skill”的形式：

- GitHub 仓库保存代码、文档、模板、示例和经验。
- `skill/SKILL.md` 作为 Codex Skill 入口。
- 用户安装 Skill 后，可以让 Codex 调用仓库里的流程和脚本。

这种方式比只写一份 Skill 更适合本项目，因为宠物制作不只是提示词，还包含切图、验证、打包、README、示例资源和长期维护经验。
