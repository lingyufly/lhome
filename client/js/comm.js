// 检查手机号码格式
function checkPhoneNo(phone){
    var reg = /^1[3|4|5|8]\d{9}$/;
    if((reg.test(phone))){
        return true;
    }else{
        return false;
    }
}