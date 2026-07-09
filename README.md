# AI Agent Framework

Đây là bộ framework chung để điều phối cấu hình AI Agent, skill và workflow (hỗ trợ Antigravity, Cursor, Cline, Claude Code, GitHub Copilot, v.v.). Thư mục gốc chứa các script tiện ích để khởi tạo công cụ và đồng bộ cấu hình agent.

## Hướng dẫn cài đặt lệnh `ai-agent-sync` toàn cục (Global)

Để sử dụng các lệnh `ai-agent-sync` và `ai-agent-adapter-sync` ở bất kỳ thư mục nào trên máy (mà không cần gõ tiền tố `bin/`), bạn cần đưa thư mục `bin` của kho lưu trữ này vào biến môi trường hệ thống. 

Dưới đây là các cách thiết lập:

### Cách 1: Cài đặt global command bằng chính `ai-agent-sync`
Tại thư mục gốc của repository framework:

```bash
bin/ai-agent-sync --install-global
```

Lệnh này tạo symlink cho cả `ai-agent-sync` và `ai-agent-adapter-sync` vào `~/.local/bin`. Sau đó bạn có thể đứng ở bất kỳ repo nào và chạy:

```bash
ai-agent-sync --generate-adapters --no-tools
ai-agent-sync cline
ai-agent-sync cursor
```

Nếu `~/.local/bin` chưa nằm trong `PATH`, thêm dòng này vào `~/.bashrc` hoặc `~/.zshrc`:

```bash
export PATH="$PATH:$HOME/.local/bin"
```

### Cách 2: Cài đặt tự động bằng script 1-click
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

### Cách 3: Thêm vào biến môi trường PATH thủ công
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

### Cách 4: Tạo Symlink vào `~/.local/bin` thủ công (Không cần quyền root)
Nếu bạn không muốn sửa PATH nhưng thư mục `~/.local/bin` đã có sẵn trong PATH:

```bash
mkdir -p ~/.local/bin
ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-sync ~/.local/bin/ai-agent-sync
ln -s /home/pc1503/Desktop/Workspace/work/ai-agent-framework/bin/ai-agent-adapter-sync ~/.local/bin/ai-agent-adapter-sync
```

### Cách 5: Tạo Symlink hệ thống (Cần quyền sudo)
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

## Quy trình skill pack migration .NET 1:1 parity

Khi dùng các skill `.NET Framework -> .NET 8+`, mặc định phải chạy theo parity, không phải modernization:

```text
Baseline bản cũ
-> Sinh Unit Test / Contract Test từ baseline cũ
-> Tạo base project bản mới
-> Tạo test scaffold cho bản mới
-> Convert từng endpoint/màn hình/nghiệp vụ 1:1
-> Regression bản mới với baseline cũ
-> Ghi deferred issues, không sửa bug legacy trong phase parity
```

Các skill chính:

- `dotnet-parity-migration`: điều phối toàn bộ phase.
- `dotnet-baseline-capture`: tạo inventory, Golden Master, `legacy-baseline.json`, và test spec từ legacy.
- `dotnet-compatibility-port`: port tối thiểu từng slice sau khi baseline và test spec đã sẵn sàng.
- `dotnet-contract-regression`: so bản .NET 8+ với baseline cũ, không so với output tự sinh từ bản mới.

Deliverables nên nằm trong `migration-docs/` hoặc run namespace:

```text
00_MIGRATION_SCOPE.md
01_LEGACY_INVENTORY.md
02_LEGACY_BASELINE.md
03_UNIT_TEST_SPEC_FROM_LEGACY_BASELINE.md
04_COMPATIBILITY_DESIGN.md
05_NEW_PROJECT_BASELINE.md
06_NEW_PROJECT_TEST_SCAFFOLD.md
07_ENDPOINT_VIEW_MIGRATION_TRACKER.md
08_CONTRACT_REGRESSION_REPORT.md
09_VIEW_UI_REGRESSION_REPORT.md
10_MIGRATION_RISK_REGISTER.md
11_ACCEPTANCE_CHECKLIST.md
15_DEFERRED_ISSUES_REPORT.md
legacy-baseline.json
```

Nếu thiếu baseline/runtime evidence thì agent phải đánh dấu `BLOCKED`, không tự tạo mock response, không tự đoán DTO/field, không tự sửa bug legacy. Một slice chỉ được coi là xong khi regression pass với baseline cũ và trạng thái là `PASS`.
