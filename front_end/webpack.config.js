const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.js", // 入口文件
  output: {
    // 输出配置
    path: path.join(__dirname, "/build"),
    filename: "bundle.js",
    publicPath: "/agent/",
  },
  module: {
    // 加载器配置
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.(png|svg|jpg|gif)$/,
        use: ["file-loader"],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./public/index.html", // 模板文件
    }),
  ],
  devServer: {
    host: "0.0.0.0", // 可以让外部设备访问您的服务器
    static: {
      directory: path.join(__dirname, "build"),
    },
    historyApiFallback: {},
    compress: true,
    port: 9000,
    open: true,
  },
};
