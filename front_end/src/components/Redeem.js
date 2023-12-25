// Redeem.js
import React, { useState } from "react";
import "../styles/redeem.css"; // 引入样式文件

function Redeems({ redeems, fetchRedeems }) {
  // 函数用于格式化时间字符串
  const formatTime = (timeString) => {
    // 解析时间字符串并创建一个 Date 对象
    const timeObj = new Date(timeString);

    // 格式化时间为 'YYYY/MM/DD HH:MM:SS' 格式
    return timeObj.toLocaleString("zh-CN", { hour12: false });
  };

  const [showPopup, setShowPopup] = useState(false);
  // 处理生成兑换码按钮点击事件
  const handleGenerateClick = () => {
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
      <button className="redeem-generate-button" onClick={handleGenerateClick}>
        生成兑换码
      </button>
      <button className="refresh-button" onClick={fetchRedeems}>
        刷新
      </button>
      {showPopup && (
        <>
          <div className="redeem-popup-backdrop" onClick={handleCancel}></div>
          <div className="redeem-create-popup">
            <label>
              金额: <input type="text" />
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
                <button className="undo-button">退回</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default Redeems;
