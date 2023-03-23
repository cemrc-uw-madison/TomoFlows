const path = require("path");
const webpack = require("webpack");

module.exports = (env, argv) => {
	const mode = argv.mode || 'development';
	
	return {
		entry: "./src/index.js",
		output: {
			path: path.resolve(__dirname, "./static/js"),
			filename: "[name].js"
		},
		module: {
			rules: [
				{
					test: /\.jsx?$/,
					exclude: /node_modules/,
					use: {
						loader: "babel-loader"
					}
				},
				{
					test: /\.css$/,
					use: [
						"style-loader",
					  	"css-loader"
					]
				},
				{
					test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
					use: {
						loader: 'url-loader',
						options: {
							limit: 10000
						}
					},
					
				}
			]
		},
		optimization: {
			minimize: true
		},
		plugins: [
			new webpack.DefinePlugin({
				'process.env.NODE_ENV' : JSON.stringify(mode)
			})
		]
	}
};
