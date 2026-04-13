# FlowPockets

FlowPockets 是一個以「真實可動用餘額（spendable balance）」為核心的智慧理財後端專案。  
它不是傳統只記錄收支分類的記帳工具，而是將記帳延伸為現金流決策系統，整合：

- 分袋式預算（Pockets）
- 信用卡已使用額度追蹤
- 預存金 / 年度基金（Reserve Funds）
- 可動用餘額計算
- Dashboard 分析 API


---

## 1. Core Features

### Users
- Create user
- List users

### Accounts
- Create bank / cash / credit card account
- List accounts
- Get single account

### Transactions
- Create transactions:
  - income
  - expense
  - card_spend
  - card_payment
- List transactions
- Filter by:
  - user_id
  - account_id
  - pocket_id
  - type

### Pockets
- Create pocket
- List pockets
- Get pocket
- Update pocket
- Archive pocket

### Reserve Funds
- Create fund
- List funds
- Get fund
- Update fund
- Archive fund

### Dashboard
- Home summary
- Pocket detail
- Account detail
- Fund detail

---

## 2. Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

---

cd backend
uvicorn app.api.main:app --reload

from app.db import Base, engine
from app.models.user import User
from app.schemas.user import UserCreate

