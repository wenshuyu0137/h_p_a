// SubAgentsTable.js
import React, { useState } from "react";
import "../styles/sub_agents_table.css"; // 确保样式文件已正确导入

function SubAgentsTable({ subAgents, refreshData, gpt_agent }) {
  const [showPopup, setShowPopup] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null); // 新增状态来存储选中的代理
  const [amount, setAmount] = useState(""); // 新增状态来存储输入框的金额

  // 处理生成兑换码按钮点击事件
  const handleTransactionClick = (agent) => {
    setShowPopup(true);
    setSelectedAgent(agent); // 设置当前选中的代理
  };

  // 处理弹窗中的确定和取消按钮
  const handleSubmit = async () => {
    // 检查amount是否是一个有效的整数
    if (!/^\d+$/.test(amount)) {
      alert("请输入有效的整数金额");
      return;
    }

    // 将字符串转换为整数
    const amountInt = parseInt(amount, 10);

    try {
      const result = await gpt_agent.agentTransaction(selectedAgent, amountInt);

      if (result && result.code === 0) {
        alert("交易成功");
        setShowPopup(false);
        setAmount(""); // 清空输入框
        refreshData(); // 刷新数据
      } else if (result) {
        // 交易失败，显示错误消息
        alert(result.message || "交易失败");
      }
    } catch (error) {
      console.error("交易处理错误", error);
      alert("交易处理时发生错误");
    }
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
              点数:
              <input
                type="text"
                value={amount} // 将输入框的值绑定到amount状态
                onChange={(e) => setAmount(e.target.value)} // 更新状态以反映输入框的变化
              />
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
                  onClick={() => handleTransactionClick(agent[0])} // 修改为箭头函数
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
