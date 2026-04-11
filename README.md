# Practice

## 設計並開發以「真實可動用餘額」為核心的智慧理財 App，整合分袋預算、信用卡圈存、預存金攤提與現金流風險預警。

## 建立 rule-based 財務引擎計算可支配額度、預算消耗速度與信用卡未來負擔，將傳統記帳工具轉為即時決策系統。

## 規劃交易資料結構、使用者行為指標、異常消費偵測與預算預測模組，支援後續統計分析與機器學習擴充。

## 實作 dashboard 與視覺化圖表，呈現袋別預算、預存金進度與現金流風險狀態。

cd backend
uvicorn app.api.main:app --reload

from app.db import Base, engine
from app.models.user import User
from app.schemas.user import UserCreate