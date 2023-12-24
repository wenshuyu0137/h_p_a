import React, { useEffect, useState } from "react"; // 引入React相关依赖

import "../styles/styles.css"; // 引入样式文件
import Sidebar from "./Sidebar";
import { useAuth } from "../contexts/AuthContext";
import useSidebarState from "../hooks/useSidebarState"; //侧边栏的钩子
import "../styles/slider.css"; // 引入样式文件
import userIcon from "../assets/images/user_icon.png"; // 引入用户图标
import UserInfoDetails from "./UserInfoDetails";
import Tab from "./Tab"; // 引入 Tab 组件
import SubAgentsTable from "./SubAgentsTable"; // 引入 SubAgentsTable 组件

function MainApp() {
  const { gpt_agent } = useAuth(); // 解构

  // 处理页面点击事件
  const handleBodyClick = (event) => {
    if (!event.target.closest("#sidebar")) {
      setSidebarOpen(false);
    }
  };

  const [userInfo, setUserInfo] = useState(null); // 使用状态来存储 userInfo
  const refreshUserInfo = async () => {
    try {
      const response = await gpt_agent.agentGetInfo();
      if (response.code === 0 && response.message) {
        setUserInfo(response.message); // 使用状态设置函数来更新 userInfo
      } else {
        console.error("无效的响应:", response);
      }
    } catch (error) {
      console.error("刷新用户信息失败:", error);
    }
  };

  //侧边栏相关钩子
  const {
    sidebarOpen,
    userInfoDetailsOpen,
    setSidebarOpen,
    handleSidebarToggle,
    toggleUserInfoDetails,
  } = useSidebarState();

  const [activeTab, setActiveTab] = useState("subAgents"); // 激活的选项卡
  const [subAgents, setSubAgents] = useState([]); // 存储下级代理信息

  // 获取下级代理信息
  useEffect(() => {
    const fetchSubAgents = async () => {
      try {
        const response = await gpt_agent.loadAllSubAgents();
        if (response.code === 0) {
          setSubAgents(response.message);
        } else {
          console.error("获取下级代理失败:", response);
        }
      } catch (error) {
        console.error("获取下级代理异常:", error);
      }
    };

    if (activeTab === "subAgents") {
      fetchSubAgents();
    }
  }, [activeTab, gpt_agent]);

  return (
    <div
      className={`main-content${sidebarOpen ? "sidebar-open" : ""}`}
      onClick={handleBodyClick}
    >
      <div className="sidebar-container">
        <button className="toggle-button" onClick={handleSidebarToggle}>
          <i
            className={`fas ${
              sidebarOpen ? "fa-arrow-left" : "fa-arrow-right"
            }`}
          ></i>
        </button>
      </div>

      <Sidebar
        sidebarOpen={sidebarOpen}
        toggleUserInfoDetails={toggleUserInfoDetails}
        userIcon={userIcon}
        gpt_agent={gpt_agent}
      />

      <div className="main-container">
        {/* 选项卡切换组件 */}
        <Tab
          className="tab-title"
          activeTab={activeTab}
          setActiveTab={setActiveTab}
        />

        <div className="tab-content">
          {/* 根据选项卡状态展示内容 */}
          {activeTab === "subAgents" && (
            <SubAgentsTable subAgents={subAgents} />
          )}
          {activeTab === "tab2" && <div>其他选项卡1内容</div>}
          {activeTab === "tab3" && <div>其他选项卡2内容</div>}
        </div>
      </div>

      <div
        className={`flex-1 flex flex-col ${sidebarOpen ? "sidebar-open" : ""}`}
      >
        {userInfoDetailsOpen && (
          <UserInfoDetails
            userInfo={userInfo}
            toggleUserInfoDetails={toggleUserInfoDetails}
            gpt_agent={gpt_agent}
            onRefreshUserInfo={refreshUserInfo}
          />
        )}
      </div>
    </div>
  );
}

export default MainApp;
