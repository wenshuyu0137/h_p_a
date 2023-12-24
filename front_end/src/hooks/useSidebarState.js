import { useState } from "react";

function useSidebarState() {
  // 定义会话状态和ID
  const [sidebarOpen, setSidebarOpen] = useState(false); // 侧边栏开关状态
  const [userInfoDetailsOpen, setUserInfoDetailsOpen] = useState(false); // 用户信息详情开关状态

  // 切换侧边栏开关状态
  const handleSidebarToggle = (event) => {
    event.stopPropagation(); // 阻止事件冒泡
    setSidebarOpen(!sidebarOpen); // 切换侧边栏状态
  };

  // 切换用户信息详情开关状态
  const toggleUserInfoDetails = () => {
    setUserInfoDetailsOpen(!userInfoDetailsOpen); // 切换用户信息详情状态
  };

  return {
    sidebarOpen,
    userInfoDetailsOpen,
    setSidebarOpen,
    handleSidebarToggle,
    toggleUserInfoDetails,
  };
}

export default useSidebarState;
