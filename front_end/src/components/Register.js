import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../styles/before.css"; // 引入样式文件

const RegistrationSchema = Yup.object().shape({
  username: Yup.string().required("Required"),
  password: Yup.string().min(6, "Too Short!").required("Required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
  phoneNumber: Yup.string().required("Required"),
});

function Register() {
  const navigate = useNavigate();
  const [isTimerActive, setIsTimerActive] = useState(false);
  const [timer, setTimer] = useState(60);

  const sendVerificationCode = (username, email) => {
    setIsTimerActive(true);
    setTimer(60);
    // 发送验证码的逻辑
    // 发送验证码的逻辑，包括用户名和邮箱
    axios
      .post("https://www.wenshuyu.chat/api/agent/email_code", {
        username,
        email,
      })
      .then((response) => {
        const { code, message } = response.data;
        // 根据后端返回的code做出相应的处理
        if (code === 0) {
        } else {
          alert(message || "登录失败，原因未知。");
        }
      })
      .catch((error) => {
        // 如果网络请求出错，设置网络错误消息
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

    // 构造要发送到后端的数据
    const postData = {
      username: values.username,
      password: values.password,
      phone: values.phoneNumber, // 确保这里的键与后端期望的键匹配
      email: values.email,
      email_code: emailCodeWithTimestamp, // 验证码字段，确保与后端期望的一致
      boss_invite_code: values.inviteCode,
    };

    axios
      .post("https://www.wenshuyu.chat/api/agent/register", postData)
      .then((response) => {
        const { code, message } = response.data;
        // 根据后端返回的code做出相应的处理
        if (code === 0) {
          alert("注册成功");
          navigate("/login"); //跳转到登录
        } else {
          // 如果后端返回错误
          alert(message || "Registration Failed");
        }
        setSubmitting(false);
      })
      .catch((error) => {
        // 处理请求错误
        alert("Registration Failed: " + error.message);
        setSubmitting(false);
      });
  };

  return (
    <div>
      <h2>Register</h2>
      <Formik
        initialValues={{
          username: "",
          password: "",
          confirmPassword: "",
          email: "",
          phoneNumber: "",
          validateCode: "", // 添加验证码字段
          inviteCode: "", //邀请码
        }}
        validationSchema={RegistrationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, values, isValid }) => (
          <Form>
            <div className="form-control">
              <label htmlFor="username" className="label">
                用户名
              </label>
              <Field type="text" name="username" />
              <ErrorMessage
                name="username"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <label htmlFor="password" className="label">
                密码
              </label>
              <Field type="password" name="password" />
              <ErrorMessage
                name="password"
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

            <div className="form-control">
              <label htmlFor="phoneNumber" className="label">
                手机号
              </label>
              <Field type="text" name="phoneNumber" />
              <ErrorMessage
                name="phoneNumber"
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
              <label htmlFor="inviteCode" className="label">
                邀请码
              </label>
              <Field type="text" name="inviteCode" />
              <ErrorMessage
                name="inviteCode"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control">
              <button type="submit" disabled={isSubmitting}>
                注册
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Register;
