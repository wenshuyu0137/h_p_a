// transactionIn.js
import React from "react";

function TransactionIn({ InRecords, refreshData }) {
  // 函数用于格式化时间字符串
  const formatTime = (timeString) => {
    // 解析时间字符串并创建一个 Date 对象
    const timeObj = new Date(timeString);

    // 减去8小时（8小时 * 每小时60分钟 * 每分钟60秒 * 每秒1000毫秒）
    timeObj.setTime(timeObj.getTime() - 8 * 60 * 60 * 1000);

    // 格式化时间为 'YYYY/MM/DD HH:MM:SS' 格式
    return timeObj.toLocaleString("zh-CN", { hour12: false });
  };

  return (
    <>
      <button className="refresh-button" onClick={refreshData}>
        刷新
      </button>
      <table>
        <thead>
          <tr>
            <th>交易对象</th>
            <th>交易金额</th>
            <th>交易时间</th>
          </tr>
        </thead>
        <tbody>
          {InRecords.map((record, index) => (
            <tr key={index}>
              <td>{record[1]}</td>
              <td>{record[5]}</td>
              <td>{formatTime(record[6])}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default TransactionIn;
