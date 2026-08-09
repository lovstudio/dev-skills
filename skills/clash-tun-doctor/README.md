# lovstudio-clash-tun-doctor

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

基于最终运行态、实时连接和日志证据，诊断并修复 Clash Verge Rev TUN 导致的应用联网故障。

Independent source repository, also distributed through [lovstudio dev-skills](https://github.com/lovstudio/dev-skills) — by [lovstudio.ai](https://lovstudio.ai)

## 适用场景

- 开启 TUN 后微信图片发不出去。
- 微信朋友圈图片加载很慢或完全不显示。
- 应用被错误规则送进失效代理，持续 Loading。
- 订阅中已经关闭 IPv6，但最终运行配置仍启用 IPv6。
- Mihomo 日志出现 `no route to host` 或 `context deadline exceeded`。

## Install

```bash
npx skills add lovstudio/clash-tun-doctor-skill
```

The aggregate bundle remains available:

```bash
npx skills add lovstudio/dev-skills
```

或使用 Claude Code 插件市场：

```text
/plugin marketplace add lovstudio/dev-skills
/plugin install dev-tools@lovstudio-dev
```

依赖：macOS、Clash Verge Rev、Python 3.8+。诊断 CLI 只使用 Python 标准库。

## Usage

```bash
SKILL_DIR="${LOVSTUDIO_SKILLS_INSTALL_DIR:?Set LOVSTUDIO_SKILLS_INSTALL_DIR}/lovstudio-clash-tun-doctor"

# 只读诊断
python3 "$SKILL_DIR/scripts/clash_tun_doctor.py" diagnose --app wechat

# 预演修复
python3 "$SKILL_DIR/scripts/clash_tun_doctor.py" fix-wechat

# 备份、修复、重启并验证
python3 "$SKILL_DIR/scripts/clash_tun_doctor.py" fix-wechat --apply

# 回滚最近一次修复
python3 "$SKILL_DIR/scripts/clash_tun_doctor.py" rollback --apply
```

## 安全模型

- 永远先诊断，后修改。
- 修改命令默认 dry-run，必须显式传入 `--apply`。
- 每次修改创建时间戳备份和文件映射清单。
- 不修改订阅 URL，不输出代理密钥或控制器 Secret。
- 修复后检查最终配置和 Mihomo 运行态，而不是只检查源配置。

## Options

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--data-dir` | 自动发现 | Clash Verge Rev 数据目录。 |
| `--socket` | 自动发现 | Mihomo 控制器 Unix Socket。 |
| `--app` | `wechat` | 诊断时使用的应用过滤器。 |
| `--apply` | false | 明确授权修改或回滚。 |
| `--no-restart` | false | 修改后不重启 Clash Verge。 |
| `--json` | false | 输出 JSON 诊断结果。 |

## License

MIT
