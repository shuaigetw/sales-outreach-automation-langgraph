---
name: sales-outreach-automation-langgraph
description: 基於 LangGraph 與多個 AI 模型的銷售自動化拓展系統，整合 Zoho CRM 抓取潛在客戶名單，並執行背景調查、自動產出客製化開發信與報告。
---

# Sales Outreach Automation (LangGraph)

這是一個強大的 AI 銷售外展自動化工具，能自動從 Zoho CRM 抓取 "NEW" 狀態的潛在客戶名單，進行 LinkedIn 與數位足跡分析，產出客製化的報告與開發信，並將結果自動更新回 Zoho CRM。

## 觸發方式

當使用者輸入以下指令或表達類似意圖時觸發此 Skill：
`/sales-langgraph-outreach`

## 執行前檢查清單 (Pre-flight Checklist)

**在執行腳本前，請務必幫使用者檢查 `.env` 環境變數：**

這套件位於 `.agents/skills/sales-outreach-automation-langgraph/` 目錄。
請確認該目錄下是否存在 `.env` 檔案。若沒有，請提醒使用者：
「在執行自動化前，請先複製 `.agents/skills/sales-outreach-automation-langgraph/.env.example` 為 `.env`，並填入您的 API Keys（包含 Zoho CRM、Google Gemini、LinkedIn、Serper API 等），才能順利執行喔！」

## 如何執行

如果 `.env` 已經準備好，請在 MyAgent 根目錄下使用 `uv` 執行主程式：

```bash
uv run python .agents/skills/sales-outreach-automation-langgraph/main.py
```

## 關於 Zoho CRM 整合

本工具預設使用 `ZohoLeadLoader`，會自動連線至您的 Zoho CRM。
- 它會尋找 Lead 狀態為 "NEW" 的潛在客戶。
- 分析完成後，它會自動將這些 Lead 的狀態更新為 "CONTACTED"，並將生成的報告連結附加上去。
