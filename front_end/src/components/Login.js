import React from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import "../styles/before.css"; // 引入样式文件

const LoginSchema = Yup.object().shape({
  username: Yup.string().required("Required"),
  password: Yup.string().required("Required"),
});

function Login() {
  const navigate = useNavigate();
  const { gpt_agent } = useAuth(); // 解构

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const data = await gpt_agent.agentLogin(values.username, values.password);
      if (data["code"] === 0) {
        gpt_agent.set_token_and_username(data["token"], values.username);
        navigate("/app");
      } else {
        alert("登录失败，请检查您的用户名和密码。");
        setSubmitting(false);
      }
    } catch (error) {
      // 处理登录过程中的异常
      alert("登录过程中出现错误: " + (error.message || "未知错误"));
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <Formik
        initialValues={{ username: "", password: "" }}
        validationSchema={LoginSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="form-control field-container">
              <label htmlFor="username" className="label">
                用户名
              </label>
              <Field type="text" name="username" className="input-field" />
              <ErrorMessage
                name="username"
                component="div"
                className="error-message"
              />
            </div>

            <div className="form-control field-container">
              <label htmlFor="password" className="label">
                密码
              </label>
              <Field type="password" name="password" className="input-field" />
              <ErrorMessage
                name="password"
                component="div"
                className="error-message"
              />
            </div>

            {/* 登录按钮 */}
            <button type="submit" className="before_button">
              登录
            </button>

            {/* 注册和忘记密码按钮 */}
            <div className="form-control aux-button-container">
              <button
                type="button"
                className="aux-button"
                onClick={() => navigate("/register")}
              >
                注册
              </button>
              <button
                type="button"
                className="aux-button"
                onClick={() => navigate("/forgot-password")}
              >
                忘记密码
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Login;
