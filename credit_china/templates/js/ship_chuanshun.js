var pako = require('pako');

var utils = {
    gzip: function (t) {
        // var e, i = atob(t).split("").map((function (t) {
        var e, i = new Buffer.from(t, "base64").toString("binary").split("").map((function (t) {
                return t.charCodeAt(0)
            }
        )), n = new Uint8Array(i), r = pako.inflate(n), o = "";
        for (e = 0; e < r.length / 8192; e++)
            o += String.fromCharCode.apply(null, r.slice(8192 * e, 8192 * (e + 1)));
        return o += String.fromCharCode.apply(null, r.slice(8192 * e)),
            decodeURIComponent(escape(o))
    }
};

function getResponse(data) {
    var result = JSON.parse(utils.gzip(data));
    return result;
};


console.log(getResponse('H4sIAAAAAAAAAIuOVjIxNDY3MzCxtFTSUYry8PdzV3B39HP3CPVXiAz1M7O0AAo/2bH25aRFL7Ysf7F/AljE0MhAz9zYxMjCXMfYQM/C0MjY3FjHRM9cJ680J0fH0MxCz0BHCajM1NLEyMzC0tTSwAAo4B+flJ+Tn58LNNHcQAmkwBSozhhEmEAxSKOJAZAAG6SkhIxiYwGPDMM+rgAA'));