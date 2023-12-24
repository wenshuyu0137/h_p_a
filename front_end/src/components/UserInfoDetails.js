import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/userInfo.css"; // 引入用户信息相关样式

function UserInfoDetails({
  userInfo,
  toggleUserInfoDetails,
  gpt_agent,
  onRefreshUserInfo,
}) {
  useEffect(() => {
    onRefreshUserInfo();
  }, []);
  const navigate = useNavigate();

  function handleLogout() {
    gpt_agent.set_logout();
    navigate("/login");
  }

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center"
      onClick={(e) => e.stopPropagation()}
    >
      <div className="bg-white p-4 rounded">
        <h3 className="text-lg font-bold mb-2">用户详情</h3>
        <div className="user-info">
          {userInfo ? (
            <>
              <p>
                <span className="info-key">上级代理:</span>{" "}
                <span className="info-value">{userInfo[9]}</span>
              </p>
              <p>
                <span className="info-key">代理等级:</span>{" "}
                <span className="info-value">{userInfo[7]} </span>
              </p>

              <p>
                <span className="info-key">当前余额:</span>{" "}
                <span className="info-value">{userInfo[5]} </span>
              </p>

              <p>
                <span className="info-key">邀请码:</span>{" "}
                <span className="info-value">{userInfo[1]} </span>
              </p>
            </>
          ) : (
            <p>用户信息加载中...</p>
          )}
        </div>

        <button
          className="mt-4 py-2 px-4 bg-blue-600 text-white rounded mr-2"
          onClick={onRefreshUserInfo}
        >
          刷新
        </button>

        <button
          className="mt-4 py-2 px-4 bg-red-600 text-white rounded mr-2"
          onClick={handleLogout}
        >
          退出登录
        </button>

        <button
          onClick={toggleUserInfoDetails}
          className="user-info-close-button"
        >
          <i className="fas fa-times user-info-close-icon"></i>
        </button>
      </div>
    </div>
  );
}

export default UserInfoDetails;
