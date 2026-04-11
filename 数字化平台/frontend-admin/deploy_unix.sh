#!/usr/bin/env zsh

echo "🚀 开始编译前端..."
npm run build

echo "🗑️  Cleaning old backend static files..."
# Note: assuming backend folder is at the same level as frontend-admin
rm -rf ../backend/app/static

echo "📦 Moving new static files..."
mv dist ../backend/app/static

echo "✅ 更新完成！现在刷新网页即可。"