import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsisV } from "@fortawesome/free-solid-svg-icons";
import "../styles/slider.css";

function Sidebar({
  sidebarOpen, //打开侧边栏
  toggleUserInfoDetails, //打开用户信息
  userIcon, //用户的图标
  gpt_agent,
}) {
  return (
    <div
      id="sidebar"
      className={`fixed top-0 left-0 w-64 bg-white p-4 h-full transition-transform duration-300 ease-in-out ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <div className="flex flex-col justify-between h-full">
        {/* 用户信息详情按钮 */}
        <div className="mt-auto">
          <button
            className="w-full text-center pb-4"
            onClick={toggleUserInfoDetails}
          >
            <img
              src={userIcon}
              alt="用户头像"
              style={{ width: "64px", height: "64px" }}
            />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
