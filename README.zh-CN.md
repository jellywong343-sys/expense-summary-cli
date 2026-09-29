# 鏀嚭姹囨€诲懡浠よ宸ュ叿

[English](README.md)

鎸夋湀浠藉拰鍒嗙被姹囨€绘湰鍦拌处鍗?CSV锛屾敮鎸佹棩鏈熴€佸垎绫荤瓫閫変互鍙?CSV/JSON 鎶ュ憡銆?
## 涓昏鍔熻兘

- 鍙厤缃棩鏈熴€侀噾棰濄€佸垎绫诲拰澶囨敞瀛楁鍚嶇О銆?- 浣跨敤 Decimal 绮剧‘璁＄畻鏈堝害鍜屽垎绫绘眹鎬汇€?- 鏀寔鍖呭惈杈圭晫鐨勬棩鏈熺瓫閫夊拰澶氫釜鍒嗙被绛涢€夈€?- 鏀寔璐у竵绗﹀彿銆佸崈浣嶅垎闅旂鍜屾嫭鍙疯礋鏁般€?- 鍙娇鐢?`--absolute` 灏嗛噾棰濊浆鎴愭鏁般€?- 瀹屽叏鏈湴杩愯锛屼笉杩炴帴閾惰鎴栭噾铻嶆湇鍔°€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/expense-summary-cli.git
cd expense-summary-cli
python -m pip install -e .
```

## 浣跨敤

```bash
expense-summary examples/expenses.csv
expense-summary expenses.csv --start 2026-01-01 --end 2026-01-31
expense-summary expenses.csv --category Food --category Transport
expense-summary expenses.csv --json report.json --csv summary.csv
```

璇峰厛纭閾惰璐﹀崟鐨勬璐熷彿瑙勫垯銆傚彧鏈夊綋璐熸暟娑堣垂闇€瑕佹寜姝ｆ暟鏀嚭璁＄畻鏃讹紝鎵嶄娇鐢?`--absolute`銆?
## 闅愮

鎵€鏈夊鐞嗛兘鍦ㄦ湰鍦板畬鎴愶紝绀轰緥鏁版嵁涓鸿櫄鏋勬暟鎹€備笉瑕佹妸鐪熷疄閲戣瀺璁板綍鎻愪氦鍒板叕寮€浠撳簱銆?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT

