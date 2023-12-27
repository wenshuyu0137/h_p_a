import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // 导入 useNavigate
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../styles/before.css"; // 引入样式文件

const ForgotPasswordSchema = Yup.object().shape({
  username: Yup.string().required("Required"),
  newPassword: Yup.string().min(6, "Too Short!").required("Required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("newPassword"), null], "Passwords must match")
    .required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
});

function ForgotPassword() {
  const navigate = useNavigate(); // 使用 useNavigate
  const [isTimerActive, setIsTimerActive] = useState(false);
  const [timer, setTimer] = useState(60);

  const sendVerificationCode = (username, email) => {
    setIsTimerActive(true);
    setTimer(60);
    // 发送验证码的逻辑
    // 发送验证码的逻辑,包括用户名和邮箱
    axios
      .post("https://www.helloprompt.chat/api/agent/email_code", {
        username,
        email,
      })
      .then((response) => {
        const { code, message } = response.data;
        // 根据后端返回的code做出相应的处理
        if (code === 0) {
        } else {
          alert(message || "登录失败,原因未知。");
        }
      })
      .catch((error) => {
        // 如果网络请求出错,设置网络错误消息
        alert(
          "网络请求错误: " + (error.response?.data?.message || error.message)
        );
      });

    // 开始60秒的倒计时
    const interval = setInterval(() => {
      setTimer((prevTimer) => {
        if (prevTimer === 1) {
          clearInterval(interval);
          setIsTimerActive(false);
          return 60;
        } else {
          return prevTimer - 1;
        }
      });
    }, 1000);
  };

  const handleSubmit = (values, { setSubmitting }) => {
    const timestamp = Math.floor(Date.now() / 1000);
    const emailCodeWithTimestamp = `${values.validateCode}-${timestamp}`;
    const postData = {
      username: values.username,
      password: values.newPassword,
      email_code: emailCodeWithTimestamp,
    };

    axios
      .post("https://www.helloprompt.chat/api/agent/change_pwd", postData)
      .then((response) => {
        const { code, message } = response.data;
        if (code === 0) {
          alert("密码修改成功");
          navigate("/login"); //跳转到登录
        } else {
          alert(message || "Password change failed");
        }
        setSubmitting(false);
      })
      .catch((error) => {
        alert("Password change failed: " + error.message);
        setSubmitting(false);
      });
  };

  return (
    <div>
      <h2>Forgot Password</h2>
      <Formik
        initialValues={{
          username: "",
          newPassword: "",
          confirmPassword: "",
          email: "",
          validateCode: "",
        }}
        validationSchema={ForgotPasswordSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, values, isValid }) => (
          <Form>
            <div className="form-control">
              <label htmlFor="username" className="label">
                Username
              </label>
              <Field type="text" name="username" />
              <ErrorMessage
                name="username"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <label htmlFor="newPassword" className="label">
                新密码
              </label>
              <Field type="password" name="newPassword" />
              <ErrorMessage
                name="newPassword"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <label htmlFor="confirmPassword" className="label">
                确认密码
              </label>
              <Field type="password" name="confirmPassword" />
              <ErrorMessage
                name="confirmPassword"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control email-verification-container">
              <label htmlFor="email" className="label">
                邮箱
              </label>

              <Field
                type="email"
                name="email"
                className="input-field email-input"
                placeholder="请输入邮箱"
              />

              <button
                type="button"
                disabled={!isValid || isTimerActive}
                onClick={() =>
                  sendVerificationCode(values.username, values.email)
                }
                className="button-send-code"
              >
                {isTimerActive ? `重新发送 (${timer})` : "发送验证码"}
              </button>
              <ErrorMessage
                name="email"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <label htmlFor="validateCode" className="label">
                验证码
              </label>
              <Field type="text" name="validateCode" />
              <ErrorMessage
                name="validateCode"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <button type="submit" disabled={isSubmitting}>
                重置密码
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default ForgotPassword;
