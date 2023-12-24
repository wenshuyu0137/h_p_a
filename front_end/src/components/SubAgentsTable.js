// SubAgentsTable.js
import React from "react";
import "../styles/sub_agents_table.css"; // 确保样式文件已正确导入

function SubAgentsTable({ subAgents }) {
  return (
    <table>
      <thead>
        <tr>
          <th>用户名</th>
          <th className="action-cell">操作</th>
        </tr>
      </thead>
      <tbody>
        {subAgents.map((agent, index) => (
          <tr key={index}>
            <td>{agent[0]}</td>
            <td className="action-cell">
              <button className="transaction-button">发起交易</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default SubAgentsTable;
