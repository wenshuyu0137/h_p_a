// Tab.js
import React from "react";
import "../styles/tab.css"; // 引入用户信息相关样式

function Tab({ activeTab, setActiveTab }) {
  return (
    <div className="tab-container">
      <button onClick={() => setActiveTab("subAgents")}>下级代理</button>
      <button onClick={() => setActiveTab("tab2")}>其他选项卡1</button>
      <button onClick={() => setActiveTab("tab3")}>其他选项卡2</button>
      {/* 更多选项卡按钮 */}
    </div>
  );
}

export default Tab;
