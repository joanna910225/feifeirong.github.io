---
title: 用 Google Apps Script 批量清空 Gmail 未读邮件
date: 2026-09-10
lang: zh
category: Engineering
tags: [gmail, google-apps-script, automation, productivity]
description: 绕过 Gmail 前端 UI 的限制，用 Apps Script 在 Google 后端直接调用 Gmail API，稳定清空成千上万封未读邮件。
translationKey: gmail-bulk-mark-read-apps-script
draft: false
---

未读邮件积压到几千甚至上万封时，Gmail 的前端 UI 基本就没法用了：全选点不动、页面卡顿、操作还经常被截断。这个方法的核心是**绕过 Gmail 前端 UI 的限制，直接通过 Google Apps Script 在后端调用 Gmail API** 来批量处理邮件。

## 核心原理

脚本通过「分页搜索 → 批量标记 → 暂停防限流 → 循环」的逻辑，在 Google 服务器端直接执行操作，强制刷新邮件状态，并且自带进度追踪。

## 完整执行步骤

1. **创建环境**：浏览器访问 [script.google.com](https://script.google.com/)，点击左上角新建一个项目（New Project）。

2. **部署代码**：清空默认代码，将以下带有日志功能的脚本粘贴进去：

```javascript
function markAllAsRead() {
  Logger.log("开始标记邮件为已读...");
  let totalProcessed = 0;

  // 每次搜索前 100 封未读邮件
  let threads = GmailApp.search('is:unread', 0, 100);

  while (threads.length > 0) {
    GmailApp.markThreadsRead(threads); // 执行标记已读
    totalProcessed += threads.length;
    Logger.log("已标记 " + threads.length + " 个对话。总计已处理: " + totalProcessed);

    Utilities.sleep(1000); // 暂停 1 秒，防止触发 API 频率限制
    threads = GmailApp.search('is:unread', 0, 100); // 获取下一批
  }

  Logger.log("执行完毕！共标记已读的对话总数: " + totalProcessed);
}
```

3. **授权与运行**：点击工具栏的**保存**（软盘图标），然后点击**运行**（Run）。首次运行会弹出权限请求，按提示选择你的 Google 账号并允许授权（如果提示「未经验证的应用」，点击「高级」→「转至项目」即可）。

4. **查看进度**：运行后，编辑器底部会自动弹出**执行日志（Execution log）**窗口，可以实时看到代码一批批处理邮件的进度，直到最终打印出「执行完毕」的汇总数据。

## 为什么这个方法稳

- **不受 UI 状态干扰**：无论收件箱是何种布局（分类、优先收件箱等），都不影响 API 的底层执行。
- **规避限流（Rate Limiting）**：加入了 `Utilities.sleep(1000)`，避免请求过快被 Google 服务器拒绝。
- **稳定性高**：通过 `while` 循环和每次 100 封的批处理，能够稳定吃掉数千甚至数万封积压邮件，而不会导致浏览器卡死或脚本超时。

> **注意**：脚本会把搜索到的**所有**未读对话标记为已读。如果只想处理一部分，可以修改搜索条件，比如 `'is:unread older_than:1y'` 只处理一年前的未读，或加上标签过滤。
