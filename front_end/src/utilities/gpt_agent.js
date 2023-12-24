class GptAgent {
  constructor(existingToken = "", existingUsername = "", authCallback) {
    // this.hostUrl = "https://www.wenshuyu.chat/agent/";
    this.hostUrl = "http://170.106.187.38:9000/";
    this.userToken = existingToken ? JSON.parse(existingToken) : { token: "" };
    this.username = existingUsername || "";
    this.authCallback = authCallback;
  }

  set_token_and_username(newToken, username) {
    this.userToken["token"] = newToken;
    this.username = username;
    localStorage.setItem("userToken", JSON.stringify({ token: newToken })); //存储token
    localStorage.setItem("username", username); //存储用户名
    this.authCallback(!!newToken); // 使用 !!newToken 来更新 isAuthenticated 状态
  }

  set_logout() {
    localStorage.removeItem("userToken");
    localStorage.removeItem("username");
    this.userToken["token"] = "";
    this.username = "";
    this.authCallback(false); // 更新 isAuthenticated 状态
  }

  handleError(e) {
    console.error("网络连接异常:", e);
    return null;
  }

  async validateToken() {
    const curUrl = this.hostUrl + "api/agent/validate_token";
    try {
      const response = await fetch(curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token: this.userToken.token }),
      });

      const data = await response.json();
      if (data.code === 0) {
        // Token 有效
        this.authCallback(true);
      } else {
        // Token 无效或已过期
        this.authCallback(false);
      }
    } catch (e) {
      // 网络错误或其他异常
      console.error("Error validating token:", e);
      this.authCallback(false);
    }
  }

  async sendEmailCode(username, email) {
    const curUrl = "api/user/email_code";
    const args = {
      username: username,
      email: email,
    };
    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(args),
      });
      const data = await response.json();
      return data;
    } catch (e) {
      return this.handleError(e);
    }
  }

  async agentRegister(
    username,
    password,
    phone,
    email,
    emailCode,
    bossInviteCode
  ) {
    const curUrl = "api/agent/register";
    const args = {
      username,
      password,
      phone,
      email,
      emailCode: `${emailCode}-${Date.now()}`,
      bossInviteCode,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async agentChangePassword(username, password, emailCode) {
    const curUrl = "api/agent/change_pwd";
    const args = {
      username,
      password,
      emailCode: `${emailCode}-${Date.now()}`,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async agentGetInfo() {
    const curUrl = "api/agent/info";
    const args = {
      username: this.username,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      const data = await response.json();
      return data;
    } catch (e) {
      console.error("Network connection error", e);
    }
  }

  async agentLogin(username, password) {
    const curUrl = "api/agent/login";
    const args = {
      username: username,
      password: password,
    };
    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(args),
      });
      const data = await response.json();
      return data;
    } catch (e) {
      return this.handleError(e);
    }
  }

  async loadAllSubAgents() {
    const curUrl = "api/agent/load_all_sub_agent";
    const args = {
      username: this.username,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async agentTransaction(toUsername, quantity, transactionType) {
    const curUrl = "api/agent/transaction";
    const args = {
      fromUsername: this.username,
      toUsername,
      quantity,
      transactionType,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async getTransactionOut() {
    const curUrl = "api/agent/get_trans_b_s";
    const args = {
      senderName: this.username,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async getTransactionIn() {
    const curUrl = "api/agent/get_trans_b_r";
    const args = {
      receiverName: this.username,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async createRedeem(quantity) {
    const curUrl = "api/agent/create_redeem";
    const args = {
      username: this.username,
      quantity,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async getRedeem() {
    const curUrl = "api/agent/get_redeem";
    const args = {
      username: this.username,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }

  async deleteRedeem(codeId) {
    const curUrl = "api/agent/delete_redeem";
    const args = {
      codeId,
    };

    try {
      const response = await fetch(this.hostUrl + curUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Token: this.userToken.token,
        },
        body: JSON.stringify(args),
      });
      return await response.json();
    } catch (e) {
      console.error("Network connection error", e);
      return null;
    }
  }
}

export default GptAgent;
