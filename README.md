# 💼 Automated Expense Audit Dashboard

A simple and effective Streamlit app that helps finance and audit teams **flag unusual or high-risk business expenses** using automated rules and visual insights.

---

## 🎯 Project Goal

To streamline the expense auditing process by:
- Automatically flagging high-value, weekend, or unknown-vendor entries
- Detecting GST mismatches based on category
- Summarizing expense trends with visuals and filters

---

## 🧠 Features

✅ Upload Excel file of business expenses  
✅ Auto-flag risky entries based on rules  
✅ Apply filters by vendor, category, flagged status  
✅ View charts:
- 📊 Expense breakdown by category
- 📈 Top 5 vendors by spend  

✅ Download flagged transactions as a CSV  
✅ Web-based interface – no coding needed to use!

---

## 📌 Audit Rules Implemented

| Rule No. | Description                                 |
|----------|---------------------------------------------|
| 1        | Amount > ₹1,00,000                          |
| 2        | Vendor not in approved master list          |
| 3        | Transactions made on weekends               |
| 4        | GST rate mismatch based on expense category |

---

## 📂 Folder Structure

expense_audit_dashboard/
│
├── app.py # Streamlit app code
├── sample_expense_data.xlsx # Sample upload file
├── vendor_master_list.csv # Approved vendors list
├── flagged_output.csv # Output (auto-generated)
└── README.md # Project info


---

## 🛠 Tech Stack

- Python 🐍
- Pandas 📊
- Streamlit 🌐
- Plotly 📈 (for interactive charts)

---

## 🚀 How to Run Locally

1. Clone the repo:

```bash
git clone https://github.com/your-username/expense-audit-dashboard.git
cd expense-audit-dashboard
