### 简介
基于 Marimo 的数据处理小应用（Python 3.12，依赖由 `uv` 管理）。

### 运行方式（Docker Compose 推荐）
1) 准备环境变量（可选）：
   - 新建 `.env` 文件（与 `docker-compose.yml` 同目录），写入：

```
PORT=12718
TOKEN_PASSWORD=please-change-me
```

2) 构建与启动：

```
docker compose build
docker compose up -d
```

3) 访问：
   - 浏览器打开 `http://localhost:12718`
   - 登录口令为环境变量 `TOKEN_PASSWORD` 的值

4) 停止与清理：

```
docker compose down
```

### 直接使用 Docker（可选）

```
docker build -t entity-list:latest .
docker run -d \
  --name entity-list \
  -p 12718:12718 \
  -e PORT=12718 \
  -e TOKEN_PASSWORD=please-change-me \
  entity-list:latest
```

### 说明
- 依赖定义见 `pyproject.toml`，锁定文件为 `uv.lock`，镜像构建时使用 `uv sync --frozen` 安装依赖。
- 服务默认监听容器内端口 `12718`，可通过映射到宿主机实现访问。
- 启动命令：`uv run marimo run main.py --host 0.0.0.0 --port $PORT --token-password=$TOKEN_PASSWORD`。
- 如需修改镜像内源配置或无需镜像加速，可调整 `pyproject.toml` 中 `[[tool.uv.index]]`。


