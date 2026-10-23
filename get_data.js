const CryptoJS = require("F:\\vscode\\code\\js\\crypto-js");

var maxDigits, ZERO_ARRAY, bigZero, bigOne, dpl10, lr10, hexatrigesimalToChar, hexToChar, highBitMasks, lowBitMasks, biRadixBase = 2, biRadixBits = 16, bitsPerDigit = biRadixBits, biRadix = 65536, biHalfRadix = biRadix >>> 1, biRadixSquared = biRadix * biRadix, maxDigitVal = biRadix - 1, maxInteger = 9999999999999998;
hexatrigesimalToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"),
    hexToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"),
    highBitMasks = new Array(0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535),
    lowBitMasks = new Array(0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535);

var BH2imd = ["色", "流感", "这边", "弱", "嘴唇", "亲", "开心", "呲牙", "憨笑", "猫", "皱眉", "幽灵", "蛋糕", "发怒", "大哭", "兔子", "星星", "钟情", "牵手", "公鸡", "爱意", "禁止", "狗", "亲亲", "叉", "礼物", "晕", "呆", "生病", "钻石", "拜", "怒", "示爱", "汗", "小鸡", "痛苦", "撇嘴", "惶恐", "口罩", "吐舌", "心碎", "生气", "可爱", "鬼脸", "跳舞", "男孩", "奸笑", "猪", "圈", "便便", "外星", "圣诞"];
var BH2iemj = {
    "色": "00e0b",
    "流感": "509f6",
    "这边": "259df",
    "弱": "8642d",
    "嘴唇": "bc356",
    "亲": "62901",
    "开心": "477df",
    "呲牙": "22677",
    "憨笑": "ec152",
    "猫": "b5ff6",
    "皱眉": "8ace6",
    "幽灵": "15bb7",
    "蛋糕": "b7251",
    "发怒": "52b3a",
    "大哭": "b17a8",
    "兔子": "76aea",
    "星星": "8a5aa",
    "钟情": "76d2e",
    "牵手": "41762",
    "公鸡": "9ec4e",
    "爱意": "e341f",
    "禁止": "56135",
    "狗": "fccf6",
    "亲亲": "95280",
    "叉": "104e0",
    "礼物": "312ec",
    "晕": "bda92",
    "呆": "557c9",
    "生病": "38701",
    "钻石": "14af6",
    "拜": "c9d05",
    "怒": "c4f7f",
    "示爱": "0c368",
    "汗": "5b7a4",
    "小鸡": "6bee2",
    "痛苦": "55932",
    "撇嘴": "575cc",
    "惶恐": "e10b4",
    "口罩": "24d81",
    "吐舌": "3cfe4",
    "心碎": "875d3",
    "生气": "e8204",
    "可爱": "7b97d",
    "鬼脸": "def52",
    "跳舞": "741d5",
    "男孩": "46b8e",
    "奸笑": "289dc",
    "猪": "6935b",
    "圈": "3ece0",
    "便便": "462db",
    "外星": "0a22b",
    "圣诞": "8e7",
    "流泪": "01000",
    "强": "1",
    "爱心": "0CoJU",
    "女孩": "m6Qyw",
    "惊恐": "8W8ju",
    "大笑": "d"
}



// 等价于函数 b：AES-128-CBC
function aesEncrypt(text, key) {
    return CryptoJS.AES.encrypt(
        CryptoJS.enc.Utf8.parse(text),
        CryptoJS.enc.Utf8.parse(key),
        { iv: CryptoJS.enc.Utf8.parse("0102030405060708"), mode: CryptoJS.mode.CBC }
    ).toString();
}

// 等价于 encryptedString：明文反转 → hex → 裸 RSA（无填充）→ hex
function rsaEncrypt(text, eHex, nHex) {
    const e = BigInt("0x" + eHex);
    const n = BigInt("0x" + nHex);
    const reversed = Buffer.from(text, "utf8").reverse();
    const m = BigInt("0x" + reversed.toString("hex"));
    return ((m ** e) % n).toString(16);
}

function a(len) { // 随机字符串，等价函数 a
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let s = "";
    for (let i = 0; i < len; i++)
        s += chars[Math.floor(Math.random() * chars.length)];
    return s;
}

// e、f、g 直接从 BH2iemj 字典取真实值：

function bxr4S(arr) {
    return arr.map(function (w) { return BH2iemj[w]; }).join("");
}

var e = "010001";
var g = "0CoJUm6Qyw8W8jud";
var f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7";


//var e = bxr4S(["流泪", "强"]);              // RSA 公钥指数
//var g = bxr4S(["爱心", "女孩", "惊恐", "大笑"]); // 第一层 AES 密钥
//var f = bxr4S(BH2imd);                      // RSA 模数（长 hex 串）


function d(text) {
    const i = a(16);
    return {
        encText: aesEncrypt(aesEncrypt(text, g), i),
        encSecKey: rsaEncrypt(i, e, f)
    };
}

// console.log(e)
// console.log(f)
// console.log(g)
//console.log(d('{"csrf_token": "2fce96444837fea541f718efb03eb0b8", "ids": "[26141649]", "level": "exhigh", "encodeType": "aac"}'));