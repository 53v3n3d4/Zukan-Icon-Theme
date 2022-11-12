const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const path = require('path');
const PnpWebpackPlugin = require('pnp-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');
const WorkboxPlugin = require('workbox-webpack-plugin');

module.exports = {
  entry: './src/index.js',

  output: {
    chunkFilename: 'static/js/[id].[chunkhash:8].js',
    filename: 'static/js/[name].[chunkhash:8].js',
    path: path.resolve(__dirname, '../build'),
  },

  plugins: [
    new CleanWebpackPlugin({
      cleanStaleWebpackAssets: false,
    }),
    new HtmlWebpackPlugin({
      title: 'Backlos',
      template: './public/index.html',
    }),
    new MiniCssExtractPlugin({
      chunkFilename: 'static/css/[id].[contenthash:8].css',
      filename: 'static/css/[name].[contenthash:8].css',
    }),
    // https://stackoverflow.com/questions/59019478/how-to-implement-a-custom-service-worker-with-workbox-in-nextjs
    // new WorkboxPlugin.InjectManifest({
    //   swSrc: "./src/registerServiceWorker.js",
    //   swDest: "service-worker.js",
    // }),
    new WorkboxPlugin.GenerateSW({
      // swDest: 'service-worker.js',
      clientsClaim: true,
      skipWaiting: true,
    }),
    new webpack.NormalModuleReplacementPlugin(
      /^mqtt$/, "mqtt/dist/mqtt.js"
    ),
  ],

  resolve: {
    plugins: [
      PnpWebpackPlugin,
    ],
  },

  resolveLoader: {
    plugins: [
      PnpWebpackPlugin.moduleLoader(module),
    ],
  },

  module: {
    rules: [
      {
        include: path.resolve(__dirname, '../src'),
        test: /\.css$/,
        use: [
          // {
          //   loader: MiniCssExtractPlugin.loader,
          //   options: {
          //     publicPath: 'static/css/',
          //   },
          // },
          MiniCssExtractPlugin.loader,
          'css-loader',
        ],
      },
    ],
  },

  optimization: {
    // Bundle splitting
    moduleIds: 'deterministic',
    runtimeChunk: 'single',
    splitChunks: {
      maxInitialRequests: Infinity,
      minSize: 0,
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name(module) {
            // get the name. E.g. node_modules/packageName/not/this/part.js
            // or node_modules/packageName
            const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];

            // npm package names are URL-safe, but some servers don't like @ symbols
            return `npm.${packageName.replace('@', '')}`;
          },
          chunks: 'all',
        },
      },
    },
    // Terser and CssNano
    minimize: true,
    minimizer: [
      new TerserPlugin({
        test: /\.js(\?.*)?$/i,
      }),
      new OptimizeCSSAssetsPlugin({
        cssProcessorOptions: {
          map: {
            inline: false,
            annotation: true,
          },
        },
      }),
    ],
  },

};
