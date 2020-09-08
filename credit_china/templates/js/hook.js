// hook系统btoa，base64加密方法
(function () {
    'use strict';

    function hook(object, attr) {
        var func = object[attr];
        object[attr] = function () {
            console.log('hooked', object, attr, arguments);
            var ret = func.apply(object, arguments);
            debugger
            console.log('result', ret);
            return ret
        }
    }

    hook(window, 'btoa')
})();


//Hook window.eval
window.__cr_eval = window.eval;
var myeval = function (src) {
    console.log('==========eval begin length=' + src.length + '.caller=' + (myeval.caller && myeval.caller.name) + '===========');
    console.log('>>>>>>>>>> eval injected' + document.location + '<<<<<<<<<<');
    console.log(src);
    console.log('========== eval end ==========');
    return window.__cr_eval(src)
};
// 注意：这一句和下一句就是常用的小花招了
var _myeval = myeval.bind(null);
_myeval.toString = window.__cr_eval.toString; // 防止网站检测是不是hook，确保还是原生的native函数
Object.defineProperty(window, 'eval', {value: _myeval});


//Hook Function
window.__cr_fun = window.Function;
var myfun = function () {
    var args = Array.prototype.slice.call(arguments, 0, -1).join(','), src = arguments[arguments.length - 1];
    console.log(src);
    console.log('=====Function end=====');
    return window.__cr_fun.apply(this, arguments)
};
// 小花招
myfun.toString = function () {
    return window.__cr_fun + ""
};
Object.defineProperty(window, 'Function', {value: myfun});


//Hook json
var my_stringify = JSON.stringify;
JSON.stringify = function (params) {
    console.log('hook json', params);
    // debugger
    return my_stringify(params)
};

var my_parse = JSON.parse;
JSON.parse = function (params) {
    console.log('解析json', params);
    // debugger
    return my_parse(params)
};


//Hook cookie
var cookie_cache = document.cookie;
Object.defineProperty(document, 'cookie', {
    get: function () {
        console.log('Geeting cookie');
        return cookie_cache;
    },
    set: function (val) {
        console.log('Setting cookie', val);
        // if (val.indexOf('__zp_stoken__') != -1){
        //     debugger;
        // }  BOSS直聘cookie参数
        var cookie = val.split(';')[0];
        var ncookie = cookie.split('=');
        var flag = false;
        var cache = cookie_cache.split("; ");
        cache = cache.map(function (a) {
            if (a.split('=')[0] === ncookie[0]) {
                flag = true;
                return cookie;
            }
            return a;
        })
        cookie_cache = cache.join("; ");
        if (!flag) {
            cookie_cache += cookie + '; ';
        }
        this._value = val;
        return cookie_cache;
    },
});


//Hook window.attr  可以hook，window对象属性的属性，(_t是window的属性，ccc是_t的属性)
var window_flag_1 = '_t';
var window_flag_2 = 'ccc';

var key_value_map = {};
var window_value = window[window_flag_1];

Object.defineProperty(window, window_flag_1, {
    get: function () {
        console.log('Getting', window, window_flag_1, '=', window_value);
        debugger;
        return window_value;
    },
    set: function (val) {
        console.log('Setting', window, window_flag_1, '=', val);
        debugger;
        window_value = val;
        key_value_map[window[window_flag_1]] = window_flag_1;
        set_obj_attr(window[window_flag_1], window_flag_2);
    },
});

function set_obj_attr(obj, attr) {
    var obj_attr_value = obj[attr];
    Object.defineProperty(obj, attr, {
        get: function () {
            console.log('Getting', key_value_map[obj], attr, '=', obj_attr_value);
            debugger
            return obj_attr_value;
        },
        set: function (val) {
            console.log('Setting', key_value_map[obj], attr, '=', val);
            debugger
            obj_attr_value = val;
        },
    });
}


//Hook websocket
WebSocket.prototype.senda = WebSocket.prototype.send;
WebSocket.prototype.send = function (data) {
    console.log('Hook WebSocket', data);
    return this.senda(data);
};


//Hook decode
(function () {
    for (var p in window) {
        var s = p.toLowerCase();
        if (s.indexOf('encode') != -1 || s.indexOf('encry') != -1) {
            console.log('Waring! Detect encode function.\n', window[p])
        }
        if (s.indexOf('decode') != -1 || s.indexOf('decry') != -1) {
            console.log('Waring! Detect decode function.\n', window[p])
        }
    }
})();


//检测是否有加密函数
(function () {
    'use strict';
    !function () {
        'use strict';
        var source = ['alert', 'decodeData', 'String.fromCharCode', 'fromCharCode', 'base64decode', 'md5', 'decode', 'btoa', 'JSON.stringify', 'MD5', 'RSA', 'AES', 'CryptoJS', 'encrypt', 'strdecode', "encode", 'decodeURIComponent', '_t'];
        console.log("开始测试是否有解密函数");
        let realCtx, realName;

        function getRealCtx(ctx, funcName) {
            let parts = funcName.split(".");
            let realCtx = ctx;
            for (let i = 0; i < parts.length - 1; i++) {
                realCtx = realCtx[parts[i]];
            }
            return realCtx;
        }

        function getRealName(funcName) {
            let parts = funcName.split(".");
            return parts[parts.length - 1];
        }

        function test(ctx) {
            for (let i = 0; i < source.length; i++) {
                let f = source[i];
                let realCtx = getRealCtx(ctx, f);
                let realName = getRealName(f);
                let chars = realCtx[realName];
                if (chars != undefined) {
                    console.log("发现可疑函数：", f);
                    console.log(chars);
                    console.log("---------------------");
                } else {
                    console.log("未发现：", f);
                }
            }
        }

        test(window);
    }();
})();


//检测是否有加密函数，打印出加密函数的返回值，直接hook结果
(function () {
    'use strict';
    var source = ['alert', 'decodeData', 'String.fromCharCode', 'fromCharCode', 'base64decode', 'md5', 'decode', 'btoa', 'JSON.stringify', 'MD5', 'RSA', 'AES', 'CryptoJS', 'encrypt', 'strdecode', "encode", 'decodeURIComponent', '_t'];
    console.log("开始测试是否有解密函数");
    let realCtx, realName;

    function getRealCtx(ctx, funcName) {
        let parts = funcName.split(".");
        let realCtx = ctx;
        for (let i = 0; i < parts.length - 1; i++) {
            realCtx = realCtx[parts[i]];
        }
        return realCtx;
    }

    function getRealName(funcName) {
        let parts = funcName.split(".");
        return parts[parts.length - 1];
    }

    function hook(ctx, funcName, level, originFunc) {
        ctx[funcName] = function (a) {
            console.log("level:" + level + " function:" + funcName, a);
            debugger;
            console.log(originFunc.toString());
            console.log(originFunc.toString);
            return originFunc(a);
        };
    }

    function test(ctx, level) {
        for (let i = 0; i < source.length; i++) {
            let f = source[i];
            let realCtx = getRealCtx(ctx, f);
            let realName = getRealName(f);
            let chars = realCtx[realName];
            hook(realCtx, realName, level, chars);
        }
    }

    test(window, 1);
})();


//检测是否有加密函数，打印出加密函数的返回值，更直观的看出加密函数内部调用的函数名
(function () {
    'use strict';
    var source = ['alert', 'decodeData', 'String.fromCharCode', 'fromCharCode', 'base64decode', 'md5', 'decode', 'btoa', 'JSON.stringify', 'MD5', 'RSA', 'AES', 'CryptoJS', 'encrypt', 'strdecode', "encode", 'decodeURIComponent', '_t'];
    console.log("开始测试是否有解密函数");
    let realCtx, realName;

    function getRealCtx(ctx, funcName) {
        let parts = funcName.split(".");
        let realCtx = ctx;
        for (let i = 0; i < parts.length - 1; i++) {
            realCtx = realCtx[parts[i]];
        }
        return realCtx;
    }

    function getRealName(funcName) {
        let parts = funcName.split(".");
        return parts[parts.length - 1];
    }

    function hook(ctx, funcName, level, originFunc) {
        ctx[funcName] = function (a) {
            console.log("level:" + level + " function:" + funcName, a);
            let regexp = / [\S]*\(.*\)\;/g;
            let match = originFunc.toString().match(regexp)
            console.log(match);
            debugger;
            return originFunc(a);
        };
    }

    function test(ctx, level) {
        for (let i = 0; i < source.length; i++) {
            let f = source[i];
            let realCtx = getRealCtx(ctx, f);
            let realName = getRealName(f);
            let chars = realCtx[realName];
            hook(realCtx, realName, level, chars);
        }
    }

    test(window, 1);
})();