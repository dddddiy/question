"use strict";


const path = require("path");

module.exports = {
  dev: {
    // Paths
    assetsSubDirectory: "static",
    assetsPublicPath: "/",
    proxyTable: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    },

    // Various Dev Server settings
    host: "0.0.0.0", // can be overwritten by process.env.HOST
    port: 8080, // can be overwritten by process.env.PORT, if port is in use, a free one will be determined
    autoOpenBrowser: false,
    errorOverlay: true,
    notifyOnErrors: true,
    poll: false, // https://webpack.js.org/configuration/dev-server/#devserver-watchoptions-

    /**
     * Source Maps
     */

    // https://webpack.js.org/configuration/devtool/#development
    devtool: "cheap-module-eval-source-map",

    cacheBusting: true,

    cssSourceMap: true
  },

  build: {
    // Template for index.html
    index: path.resolve(__dirname, "../dist/index.html"),

    // Paths
    assetsRoot: path.resolve(__dirname, "../dist"),
    assetsSubDirectory: "static",
    assetsPublicPath: "/",
    proxyTable: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      }
    },
    /**
     * Source Maps
     */

    productionSourceMap: false,
    devtool: "#source-map",

    productionGzip: false,
    productionGzipExtensions: ["js", "css"],

   
    bundleAnalyzerReport: process.env.npm_config_report
  }
};
