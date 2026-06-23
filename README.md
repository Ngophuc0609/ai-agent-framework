# AI Agent Framework

Đây là bộ framework chung để điều phối cấu hình AI Agent, skill và workflow (hỗ trợ Antigravity, Cursor, Cline, Claude Code, GitHub Copilot, v.v.). Thư mục gốc chứa các script tiện ích để khởi tạo công cụ và đồng bộ cấu hình agent.

## Hướng dẫn cài đặt lệnh `ai-agent-sync` toàn cục (Global)

Để sử dụng các lệnh `ai-agent-sync` và `ai-agent-adapter-sync` ở bất kỳ thư mục nào trên máy (mà không cần gõ tiền tố `bin/`), bạn cần đưa thư mục `bin` của kho lưu trữ này vào biến môi trường hệ thống. 

Dưới đây là các cách thiết lập:

### Cách 1: Cài đặt tự động bằng script 1-click (Nhanh nhất - Đa nền tảng)
Tại thư mục gốc của repository, bạn chỉ cần chạy lệnh tương ứng với hệ điều hành:

**Dành cho Ubuntu / Linux / macOS (hoặc WSL):**
```bash
./install.sh
source ~/.bashrc  # (Hoặc source ~/.zshrc)
```

**Dành cho Windows (PowerShell):**
```powershell
.\install.ps1
```
*(Lưu ý trên Windows: Sau khi cài đặt xong bằng PowerShell, hãy tắt và mở lại cửa sổ Terminal để biến môi trường PATH có tác dụng. Nếu PowerShell báo lỗi execution policy, hãy chạy bằng quyền Admin hoặc thêm cờ `-ExecutionPolicy Bypass`).*

### Cách 2: Thêm vào biến môi trường PATH thủ công
Cách này giúp shell của bạn luôn nhận diện các file thực thi trong thư mục `bin` của repo này.

1. Mở file cấu hình shell của bạn (thường là `~/.bashrc` cho Bash hoặc `~/.zshrc` cho Zsh):
   ```bash
   nano ~/.bashrc
   ```
2. Thêm dòng sau vào cuối file, nhớ thay thế đường dẫn tuyệt đối trỏ tới thư mục `bin` của repo này:
   ```bash
   export PATH="$PATH:/home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin"
   ```
3. Lưu lại và áp dụng thay đổi bằng lệnh:
   ```bash
   source ~/.bashrc  # (Hoặc source ~/.zshrc tuỳ loại shell bạn dùng)
   ```

### Cách 2: Tạo Symlink vào `~/.local/bin` (Không cần quyền root)
Nếu bạn không muốn sửa PATH nhưng thư mục `~/.local/bin` đã có sẵn trong PATH:

```bash
mkdir -p ~/.local/bin
ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-sync ~/.local/bin/ai-agent-sync
ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-adapter-sync ~/.local/bin/ai-agent-adapter-sync
```

### Cách 3: Tạo Symlink hệ thống (Cần quyền sudo)
Cách này tạo liên kết tới thư mục `/usr/local/bin` để dùng chung cho mọi user:

```bash
sudo ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-sync /usr/local/bin/ai-agent-sync
sudo ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-adapter-sync /usr/local/bin/ai-agent-adapter-sync
```

## Cách sử dụng sau khi cài đặt

Sau khi setup thành công, bạn có thể đứng ở bất kỳ thư mục dự án nào trên máy và gõ trực tiếp lệnh để cài đặt và khởi tạo các công cụ (như MCP Memory, CodeGraph):

```bash
# Khởi tạo công cụ
ai-agent-sync --install-tools --yes

# Đồng bộ rules và instructions cho các AI agents
ai-agent-sync --install-tools --yes --generate-adapters

# Hoặc đồng bộ cho agent cụ thể (VD: Antigravity, Cursor)
ai-agent-sync agy
ai-agent-sync cursor
```
