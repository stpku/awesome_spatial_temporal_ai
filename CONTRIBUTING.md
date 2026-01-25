# 贡献指南

感谢您对本项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 1. 添加新项目
在 `awesomelist/github_projects.json` 中添加新的开源项目：

```json
{
  "name": "项目名称",
  "url": "GitHub 地址",
  "description": "项目描述（英文）",
  "stars": Star 数量,
  "last_updated": "YYYY-MM-DD",
  "tech_stack": ["技术栈"]
}
```

### 2. 添加最新研究项目
在 `awesomelist/latest_projects.json` 中添加前沿研究项目：

```json
{
  "name": "项目名称",
  "url": "项目官网或 GitHub",
  "description": "项目描述",
  "category": "分类",
  "tech_stack": ["技术栈"],
  "highlights": ["主要特点"]
}
```

### 3. 添加会议信息
在 `awesomelist/conferences.json` 中添加学术会议：

```json
{
  "name": "会议缩写",
  "full_name": "会议全称",
  "url": "官网地址",
  "date": "举办时间",
  "deadline": "投稿截止日期",
  "focus": ["研究领域"],
  "categories": ["分类标签"]
}
```

### 4. 添加期刊
在 `awesomelist/journals.json` 中添加学术期刊。

### 5. 添加媒体渠道
在 `awesomelist/media_channels.json` 中添加公众号或 Newsletter。

## 提交流程

1. Fork 本项目
2. 创建分支 (`git checkout -b feature/add-new-project`)
3. 提交更改 (`git commit -m 'Add new project: xxx'`)
4. 推送到分支 (`git push origin feature/add-new-project`)
5. 创建 Pull Request

## 数据格式要求

- 所有日期格式：`YYYY-MM-DD`
- URL 必须有效且可访问
- 描述信息应简洁明了
- 技术栈使用标准标签

## 更新频率

建议每季度更新一次数据，保持信息时效性。

## 联系方式

如有问题，请提交 Issue 或联系维护者。
