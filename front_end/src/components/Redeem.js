// Redeem.js
import React, { useState } from "react";
import "../styles/redeem.css"; // 引入样式文件

function Redeems({ redeems, refreshData, gpt_agent }) {
  // 函数用于格式化时间字符串
  const formatTime = (timeString) => {
    // 解析时间字符串并创建一个 Date 对象
    const timeObj = new Date(timeString);

    // 格式化时间为 'YYYY/MM/DD HH:MM:SS' 格式
    return timeObj.toLocaleString("zh-CN", { hour12: false });
  };

  const [amount, setAmount] = useState(""); // 新增状态来存储输入框的金额

  const [showPopup, setShowPopup] = useState(false);
  // 处理弹窗中的确定和取消按钮
  const handleGenerateClick = () => {
    setShowPopup(true);
  };

  const handleSubmit = async () => {
    // 检查amount是否是一个有效的整数
    if (!/^\d+$/.test(amount)) {
      alert("请输入有效的整数金额");
      return;
    }

    // 将字符串转换为整数
    const amountInt = parseInt(amount, 10);

    try {
      const result = await gpt_agent.createRedeem(amountInt);

      if (result && result.code === 0) {
        alert("生成成功");
        setShowPopup(false);
        setAmount(""); // 清空输入框
        refreshData(); // 刷新数据
      } else if (result) {
        // 交易失败,显示错误消息
        alert(result.message || "生成失败");
      }
    } catch (error) {
      console.error("生成处理错误", error);
      alert("生成时发生错误");
    }
  };

  const handleCancel = () => {
    setShowPopup(false);
  };

  // 处理生成兑换码按钮点击事件
  const handleUndoClick = async (code) => {
    try {
      const result = await gpt_agent.undoRedeem(code);

      if (result && result.code === 0) {
        alert("撤销成功");
        refreshData(); // 刷新数据
      } else if (result) {
        alert(result.message || "撤销失败");
      }
    } catch (error) {
      console.error("撤销处理错误", error);
      alert("撤销处理时发生错误");
    }
  };

  return (
    <>
      <button className="redeem-generate-button" onClick={handleGenerateClick}>
        生成兑换码
      </button>
      <button className="refresh-button" onClick={refreshData}>
        刷新
      </button>
      {showPopup && (
        <>
          <div className="redeem-popup-backdrop" onClick={handleCancel}></div>
          <div className="redeem-create-popup">
            <label>
              点数:
              <input
                type="text"
                value={amount} // 将输入框的值绑定到amount状态
                onChange={(e) => setAmount(e.target.value)} // 更新状态以反映输入框的变化
              />
            </label>
            <div className="redeem-button-container">
              <button onClick={handleSubmit}>确定</button>
              <button onClick={handleCancel}>取消</button>
            </div>
          </div>
        </>
      )}

      <table>
        <thead>
          <tr>
            <th>兑换码</th>
            <th>价值</th>
            <th>使用状态</th>
            <th>使用者</th>
            <th>时间</th>
            <th className="action-cell">操作</th>
          </tr>
        </thead>
        <tbody>
          {redeems.map((single, index) => (
            <tr key={index}>
              <td>{single[1]}</td>
              <td>{single[2]}</td>
              <td style={{ color: single[5] ? "green" : "red" }}>
                {single[5] ? "未使用" : "已使用"}
              </td>
              <td>{single[6]}</td>
              <td>{formatTime(single[7])}</td>
              <td className="action-cell">
                <button
                  className="undo-button"
                  onClick={() => handleUndoClick(single[1])} // 修改为箭头函数
                >
                  撤回
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default Redeems;
