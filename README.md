# Awesome Spatio-Temporal AI (Data Mirror)

> **⚠️ 这是数据镜像仓库**
> 
> 完整项目（含代码、自动化工具、文档）请访问：
> - **GitHub**: https://github.com/stpku/awesome_spatial_temporal_ai
> - **NAS Git**: ssh://skyswind@192.168.1.10:22/volume1/gitrepo/awesome_spatial_temporal_ai.git

精选的时空智能（Spatio-Temporal AI）资源合集，涵盖空间智能、世界模型、开源项目、学术期刊、行业媒体等。

**最后更新**: 2026-01-30

---

## 数据文件

本仓库仅包含核心数据文件：

| 文件 | 内容 |
|------|------|
| `awesomelist/github_projects.json` | GitHub 开源项目（24个） |
| `awesomelist/latest_projects.json` | 最新空间智能/世界模型项目（14个） |
| `awesomelist/conferences.json` | 学术会议（11个） |
| `awesomelist/journals.json` | 学术期刊（9个） |
| `awesomelist/datasets.json` | 数据集（14个） |
| `awesomelist/media_channels.json` | 媒体渠道（10个） |
| `awesomelist/papers.json` | 学术论文（40篇） |

**总计**: 122 个资源条目

---

## 快速开始

### 浏览数据

```bash
# 查看 GitHub 项目
cat awesomelist/github_projects.json | python -m json.tool

# 查看最新项目
cat awesomelist/latest_projects.json | python -m json.tool
```

### 使用数据

```python
import json

# 加载项目数据
with open('awesomelist/github_projects.json') as f:
    data = json.load(f)
    for category in data['categories']:
        print(f"## {category['category']}")
        for project in category['projects']:
            print(f"- [{project['name']}]({project['url']}) - {project['description']}")
```

---

## 数据更新

本镜像仓库的数据定期从主仓库同步。如需最新数据或提交贡献，请访问：

🔗 **https://github.com/stpku/awesome_spatial_temporal_ai**

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 相关链接

- **主仓库**: https://github.com/stpku/awesome_spatial_temporal_ai
- **Gitee 镜像**: https://gitee.com/stpku/awesome_spatial_tempoal_ai
- **NAS 完整版**: ssh://skyswind@192.168.1.10:22/volume1/gitrepo/awesome_spatial_temporal_ai.git
