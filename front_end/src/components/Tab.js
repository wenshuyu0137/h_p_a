// Tab.js
import React from "react";
import "../styles/tab.css"; // 引入用户信息相关样式

function Tab({ activeTab, setActiveTab }) {
  return (
    <div className="tab-container">
      <button onClick={() => setActiveTab("subAgents")}>下级代理</button>
      <button onClick={() => setActiveTab("transactionOut")}>卖出交易</button>
      <button onClick={() => setActiveTab("transactionIn")}>买入交易</button>
      <button onClick={() => setActiveTab("Redeem")}>兑换码</button>
      {/* 更多选项卡按钮 */}
    </div>
  );
}

export default Tab;
