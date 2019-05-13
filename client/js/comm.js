// 正则-判断手机号码格式
function checkMobile(phone){
    var reg = /^1[3|4|5|8]\d{9}$/;
    return reg.test(phone);
}

// 正则-判断银行卡号(数字16-19)
function checkCard(card) {
	var reg = /^\d{16,19}$/g;
	return reg.test(card);
}