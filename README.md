# 🇰🇷 Korean Data MCP

> Real-time Korean web data for AI assistants — powered by [Apify](https://apify.com) actors.

[![PyPI](https://img.shields.io/pypi/v/korean-data-mcp)](https://pypi.org/project/korean-data-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-blue)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives Claude, Cursor, and other AI tools direct access to live Korean web data — including Naver reviews, Melon music charts, Daangn/Bunjang marketplace listings, Korean news, and Musinsa fashion rankings.

[![korean-data-mcp MCP server](https://glama.ai/mcp/servers/leadbrain/korean-data-mcp/badges/card.svg)](https://glama.ai/mcp/servers/leadbrain/korean-data-mcp)

---

## 🛠 Available Tools

| Tool | Description |
|------|-------------|
| `get_naver_place_reviews` | Fetch reviews for any Naver Place (restaurant, cafe, shop, etc.) |
| `get_melon_chart` | Real-time / daily / weekly Korean music chart (실시간 차트) |
| `search_daangn` | Search Daangn Market (당근마켓) C2C listings |
| `search_bunjang` | Search Bunjang (번개장터) marketplace |
| `search_naver_news` | Search Naver News articles by keyword |
| `search_naver_places` | Search Naver Map places by keyword + location |
| `get_musinsa_ranking` | Musinsa fashion ranking by category |

---

## 🚀 Quick Start

### 1. Get an Apify API Token

Sign up at [apify.com](https://apify.com) (free tier: $5/month credit included).  
Copy your token from [console.apify.com/account/integrations](https://console.apify.com/account/integrations).

### 2. Install

```bash
pip install korean-data-mcp
```

Or with `uv` (recommended):

```bash
uv add korean-data-mcp
```

### 3. Set Environment Variable

```bash
export APIFY_TOKEN="your_apify_token_here"
```

### 4. Run the MCP Server

```bash
korean-data-mcp
```

---

## ⚙️ Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "korean-data": {
      "command": "korean-data-mcp",
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

Or with `uvx` (no install needed):

```json
{
  "mcpServers": {
    "korean-data": {
      "command": "uvx",
      "args": ["korean-data-mcp"],
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

---

## 💬 Usage Examples

Once connected to Claude Desktop or another MCP client:

```
"What are the top 10 songs on Melon chart right now?"

"Find cafes near Hongdae on Naver Map and show their reviews."

"Search Daangn for iPhone 15 Pro listings in Seoul."

"What are the trending news stories on Naver today about 인공지능?"

"Show me the Musinsa top 50 outer clothing items."
```

---

## 🔧 Cursor / VS Code Configuration

Add to `.cursor/mcp.json` or `.vscode/mcp.json`:

```json
{
  "servers": {
    "korean-data": {
      "type": "stdio",
      "command": "korean-data-mcp",
      "env": {
        "APIFY_TOKEN": "your_apify_token_here"
      }
    }
  }
}
```

---

## 📊 Data Sources

All data is fetched live via [Apify](https://apify.com/oxygenated_quagmire) actors:

| Actor | Apify Store |
|-------|-------------|
| Naver Place Reviews | [oxygenated_quagmire/naver-place-reviews](https://apify.com/oxygenated_quagmire/naver-place-reviews) |
| Melon Chart | [oxygenated_quagmire/melon-chart-scraper](https://apify.com/oxygenated_quagmire/melon-chart-scraper) |
| Daangn Market | [oxygenated_quagmire/daangn-market-scraper](https://apify.com/oxygenated_quagmire/daangn-market-scraper) |
| Bunjang Market | [oxygenated_quagmire/bunjang-market-scraper](https://apify.com/oxygenated_quagmire/bunjang-market-scraper) |
| Naver News | [oxygenated_quagmire/naver-news-scraper](https://apify.com/oxygenated_quagmire/naver-news-scraper) |
| Naver Place Search | [oxygenated_quagmire/naver-place-search](https://apify.com/oxygenated_quagmire/naver-place-search) |
| Musinsa Ranking | [oxygenated_quagmire/musinsa-ranking-scraper](https://apify.com/oxygenated_quagmire/musinsa-ranking-scraper) |

---

## 💰 Pricing

- **Apify Free Tier**: $5/month credit — enough for ~1,000–5,000 tool calls
- Actor runs are billed per 1,000 items returned ($0.50/1K items)
- No additional cost for this MCP server itself

---

## 🏗 Development

```bash
git clone https://github.com/leadbrain/korean-data-mcp
cd korean-data-mcp
pip install -e ".[dev]"
export APIFY_TOKEN="your_token"
python -m korean_data_mcp.server
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🤝 Contributing

Issues and PRs welcome at [github.com/leadbrain/korean-data-mcp](https://github.com/leadbrain/korean-data-mcp)

---

*Built on [FastMCP](https://github.com/PrefectHQ/fastmcp) · Data from [Apify](https://apify.com)*

<!-- mcp-name: io.github.leadbrain/korean-data -->