var NODE_JS = !global.JS_MD5_NO_NODE_JS && "object" === typeof process && process.versions && process.versions.node;
var OUTPUT_TYPES = ["hex", "array", "digest", "buffer", "arrayBuffer", "base64"];
var createOutputMethod = function (e) {
    return function (t) {
        return new Md5(!0).update(t)[e]()
    }
}
    , createMethod = function () {
    var e = createOutputMethod("hex");
    NODE_JS && (e = nodeWrap(e)),
        e.create = function () {
            return new Md5
        }
        ,
        e.update = function (t) {
            return e.create().update(t)
        }
    ;
    for (var t = 0; t < OUTPUT_TYPES.length; ++t) {
        var n = OUTPUT_TYPES[t];
        e[n] = createOutputMethod(n)
    }
    return e
};

nodeWrap = function (method) {
    var crypto = eval("require('crypto')")
        , Buffer = eval("require('buffer').Buffer")
        , nodeMethod = function (e) {
        if ("string" === typeof e)
            return crypto.createHash("md5").update(e, "utf8").digest("hex");
        if (null === e || void 0 === e)
            throw ERROR;
        return e.constructor === ArrayBuffer && (e = new Uint8Array(e)),
            Array.isArray(e) || ArrayBuffer.isView(e) || e.constructor === Buffer ? crypto.createHash("md5").update(new Buffer(e)).digest("hex") : method(e)
    };
    return nodeMethod
};


function getHeaders(page) {
    var b = "7b70f5ef9314c619120444d73d7f84b8";
    var sign = createMethod()(page + "&key=" + b);
    // console.log(sign);
    var h = Math.round(9999 * Math.random(1e3));
    // console.log(h);
    var m = Math.round((new Date).getTime() / 1e3).toString();
    // console.log(m);
    var g = "77eb61a077c89105b8f1f371710fadd6";
    var csrf_sign = createMethod()(h + m + g);
    var obj = {'Keep-Mt': h, 'Keep-At': m, 'Keep-Csrf': g, 'Csrf-Sign': csrf_sign, 'sign': sign};
    return obj;
}

console.log("headers=", getHeaders('page=1'));
