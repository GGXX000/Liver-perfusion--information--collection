#!/bin/bash

# --- Config ---
PACKAGE_NAME="project_deploy_$(date +%Y%m%d)"
DIST_DIR="./$PACKAGE_NAME"
ZIP_NAME="${PACKAGE_NAME}.zip"

echo "🚀 Starting Windows package creation..."

# 1. Clean up
rm -rf "$DIST_DIR"
rm -f "$ZIP_NAME"
mkdir -p "$DIST_DIR"

# 2. Build Frontend
echo "📦 Building frontend..."
cd frontend-admin && npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi
cd ..

echo "🚚 Moving static files to backend..."
rm -rf backend/app/static
cp -r frontend-admin/dist backend/app/static

# 3. Copy files to dist
echo "📂 Collecting files..."
mkdir -p "$DIST_DIR/backend"
cp -r backend/app "$DIST_DIR/backend/"
cp backend/requirements.txt "$DIST_DIR/backend/"

mkdir -p "$DIST_DIR/data"
if [ -f "data/hospital_demo.db" ]; then
    cp "data/hospital_demo.db" "$DIST_DIR/data/"
fi

cp start.bat "$DIST_DIR/"

# 4. Create ZIP
echo "🗜️  Creating ZIP..."
zip -r "$ZIP_NAME" "$DIST_DIR"

# 5. Clean up
rm -rf "$DIST_DIR"

echo "------------------------------------------"
echo "✅ Done!"
echo "📦 ZIP file: $ZIP_NAME"
echo "------------------------------------------"
