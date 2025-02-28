module.exports = {entry:
    {index:'./index/index.jsx'},
    output: {
        filename:'[name].bundle.js',
        path:__dirname
    },
    resolve: {
        extensions:['.js', '.jsx']
    },
    module:{
        rules: [{test:/\.(js|jsx)/, loader:'babel-loader', exclude:/node_modules/}]
    },
    mode: 'development'
}

