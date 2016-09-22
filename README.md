# octocat-webhooks
一个使用 github webhooks 自动部署网站的脚本

## 使用方法

1. 生成 secret_token: `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)'`
2. 在 `.bashrc` 中加入secret_token: `export GH_SECRET_TOKEN=your_secret_token` 并执行 `source ~/.bashrc` 确保环境变量被导入
3. 在你的 github 项目中开启 webhooks 并设置以下参数:
   - Payload URL: http://yoursite:8001/deploy
   - Content type: application/json
   - Secret: your_secret_token
4. 执行 webhooks.py 开启 webhooks 部署服务

