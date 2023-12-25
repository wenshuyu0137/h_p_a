// SubAgentsTable.js
import React, { useState } from "react";
import "../styles/sub_agents_table.css"; // 确保样式文件已正确导入

function SubAgentsTable({ subAgents, refreshData, gpt_agent }) {
  const [showPopup, setShowPopup] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null); // 新增状态来存储选中的代理
  const [amount, setAmount] = useState(""); // 新增状态来存储输入框的金额
  // 处理生成兑换码按钮点击事件
  const handleTransactionClick = () => {
    setShowPopup(true);
  };

  // 处理弹窗中的确定和取消按钮
  const handleSubmit = () => {
    // 处理提交逻辑
    setShowPopup(false);
  };

  const handleCancel = () => {
    setShowPopup(false);
  };
  return (
    <>
      <button className="refresh-button" onClick={refreshData}>
        刷新
      </button>
      {showPopup && (
        <>
          <div
            className="transaction-popup-backdrop"
            onClick={handleCancel}
          ></div>
          <div className="transaction-create-popup">
            <label>
              金额: <input type="text" />
            </label>
            <div className="transaction-button-container">
              <button onClick={handleSubmit}>确定</button>
              <button onClick={handleCancel}>取消</button>
            </div>
          </div>
        </>
      )}
      <table>
        <thead>
          <tr>
            <th>代理名</th>
            <th className="action-cell">操作</th>
          </tr>
        </thead>
        <tbody>
          {subAgents.map((agent, index) => (
            <tr key={index}>
              <td>{agent[0]}</td>
              <td className="action-cell">
                <button
                  className="transaction-button"
                  onClick={handleTransactionClick}
                >
                  发起交易
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default SubAgentsTable;
