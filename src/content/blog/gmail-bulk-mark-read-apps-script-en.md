---
title: Bulk-Clearing Gmail Unread Emails with Google Apps Script
date: 2026-09-10
lang: en
category: Engineering
tags: [gmail, google-apps-script, automation, productivity]
description: Bypass Gmail's front-end UI limits and batch-mark thousands of unread emails via Apps Script, with rate-limit-safe pagination and progress logging.
translationKey: gmail-bulk-mark-read-apps-script
draft: false
---

When unread emails pile up to thousands or even tens of thousands, Gmail's front-end UI becomes unusable: select-all freezes, pages stutter, and operations get cut off midway. The core of this method is **bypassing Gmail's front-end UI entirely and calling the Gmail API directly on Google's backend via Google Apps Script**.

## Core Principle

The script follows a "paginated search → batch mark → sleep to avoid rate limits → loop" pattern. It executes server-side on Google's infrastructure, forces the read-state refresh, and tracks its own progress in logs.

## Full Steps

1. **Set up the environment**: open [script.google.com](https://script.google.com/) in your browser and create a new project from the top-left menu.

2. **Deploy the code**: clear the default code and paste in the following script, which includes progress logging:

```javascript
function markAllAsRead() {
  Logger.log("Started marking emails as read...");
  let totalProcessed = 0;

  // Search the first 100 unread threads each round
  let threads = GmailApp.search('is:unread', 0, 100);

  while (threads.length > 0) {
    GmailApp.markThreadsRead(threads); // mark batch as read
    totalProcessed += threads.length;
    Logger.log("Marked " + threads.length + " threads. Total so far: " + totalProcessed);

    Utilities.sleep(1000); // pause 1s to avoid API rate limits
    threads = GmailApp.search('is:unread', 0, 100); // fetch next batch
  }

  Logger.log("Done! Total threads marked as read: " + totalProcessed);
}
```

3. **Authorize and run**: hit **Save** (the floppy icon) in the toolbar, then **Run**. On the first run, a permission prompt appears — pick your Google account and grant access (if warned about an "unverified app", choose **Advanced** → **Go to project**).

4. **Watch the progress**: after running, an **Execution log** panel opens at the bottom of the editor, showing batches being processed in real time until the final summary line prints.

## Why This Method Holds Up

- **Immune to UI state**: whatever your inbox layout is (categories, priority inbox, etc.) doesn't affect the underlying API execution.
- **Rate-limit safe**: the `Utilities.sleep(1000)` call keeps requests from being rejected by Google's servers.
- **Stable at scale**: the `while` loop plus 100-thread batches can chew through thousands or tens of thousands of backlogged emails without freezing your browser or timing out the script.

> **Note**: the script marks **every** unread thread it finds as read. If you only want a subset, adjust the search query — e.g. `'is:unread older_than:1y'` to only touch mail older than a year, or add a label filter.
