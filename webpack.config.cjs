const path = require("path");
const { env, argv } = require("process");

var config = {
  entry: "./app/static/js/app.js",
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "app/static/js/dist"),
  },
  mode: "development",
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: "asset/resource",
      },
    ],
  },
};

module.exports = (env, argv) => {
  if (process.env.MODE === "prod") {
    config.mode = "production";
  }
  return config;
};
