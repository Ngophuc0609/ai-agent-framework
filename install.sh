#!/bin/bash
set -e

REPO_DIR=$(pwd)
BIN_DIR="$REPO_DIR/bin"
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

echo "Tiến hành cài đặt tự động ai-agent-sync..."

add_to_path() {
    local rc_file=$1
    if [ -f "$rc_file" ]; then
        if ! grep -q "$BIN_DIR" "$rc_file"; then
            echo -e "\n# AI Agent Framework PATH" >> "$rc_file"
            echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$rc_file"
            echo "✅ Đã thêm PATH vào $rc_file"
        else
            echo "⚡ PATH đã tồn tại sẵn trong $rc_file, bỏ qua."
        fi
    fi
}

add_to_path "$BASHRC"
add_to_path "$ZSHRC"

echo "🎉 Cài đặt hoàn tất!"
echo "👉 Vui lòng chạy lệnh sau để áp dụng ngay, hoặc khởi động lại Terminal:"
echo "source ~/.bashrc"
