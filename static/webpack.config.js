const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
	filename: 'main.js',
	path: path.resolve(__dirname, 'dist')
    },
    devServer: {
	contentBase: './dist'
    },
    devtool: '#eval-source-map',
    module: {
    	rules: [
    	{
    		test: /\.(js|jsx)$/,
    		exclude: /node_modules/,
    		use: {
    			loader: "babel-loader"
    		}
    	}
    	]
    }
};



