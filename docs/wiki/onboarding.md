# Onboarding - Finpath Newsroom

## Giới thiệu

Finpath Newsroom V3.6 là hệ thống viết bài tin chuyên sâu về cổ phiếu Việt Nam sử dụng Claude Code CLI và pipeline LLM agents.

## Yêu cầu

- Python 3.13+
- Node.js 18+ (cho web viewer)
- Claude Code CLI

## Cài đặt

```bash
# Clone và vào thư mục
cd /data/finpath/finpath-newsroom

# Cài đặt Python dependencies
uv sync

# Cài đặt web viewer dependencies
cd web && npm install && cd ..

# Copy secrets file
cp data/secrets.yaml.example data/secrets.yaml
# Edit data/secrets.yaml với API keys thật
```

## Cấu trúc chính

### 1. Skills (`.claude/skills/`)

12 skill V3.6 cho pipeline:

| Skill | Mô tả |
|-------|-------|
| `finpath-newsroom-orchestrator` | Điều phối toàn bộ pipeline |
| `finpath-newsroom-crawler` | Crawl tin từ 20 nguồn |
| `finpath-newsroom-editor` | Filter + route theo universe |
| `finpath-newsroom-story-editor` | Tổng biên tập, tạo brief |
| `finpath-newsroom-master-bank` | Viết bài Bank |
| `finpath-newsroom-master-ck` | Viết bài CK |
| `finpath-newsroom-master-bds` | Viết bài BĐS |
| `finpath-newsroom-master-oil-gas` | Viết bài Oil-Gas |
| `finpath-newsroom-skeptic` | Critique "Góc nhìn ngược" |
| `pipeline` | Quản lý + mở rộng pipeline |
| `guide` | Onboarding assistant |

### 2. Knowledge Base (`kb/`)

Markdown KB cho 4 sector:

- `kb/bank/` - 27 mã ngân hàng
- `kb/ck/` - 30 mã chứng khoán
- `kb/bds/` - 4 mã BĐS dân cư
- `kb/oil-gas/` - 10 mã dầu khí

### 3. Lib (`lib/`)

Python helpers:

- `finpath_api.py` - Gọi Finpath API
- `pipeline_db.py` - SQLite operations
- `quality_gates.py` - Validate bài viết

### 4. Web Viewer (`web/`)

React + Vite + Tailwind app để đọc bài.

## Chạy Pipeline

```bash
# Viết tin về một mã
# (trong Claude Code CLI)
/tin VCB

# Chạy web viewer
cd web && npm run dev
```

## Quy tắc quan trọng

1. **0% tiếng Anh** trong nội dung bài - dùng mapping cứng (xem CLAUDE.md)
2. **200-400 từ** hard cap
3. **Title phải có hook** - câu hỏi hoặc paradox
4. **Không khuyến nghị mua/bán** - chỉ phân loại NĐT phù hợp
5. **Verify trước khi action lớn** - đọc spec + get approval

## Tài liệu liên quan

- [Architecture](./architecture.md) - Cấu trúc hệ thống
- [Features Map](./features-map.md) - Danh sách chức năng
- [Skills Guide](./skills-guide.md) - Danh sách skills
- [CLAUDE.md](/data/finpath/finpath-newsroom/CLAUDE.md) - Project instructions
