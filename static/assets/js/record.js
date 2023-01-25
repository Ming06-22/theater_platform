function Delete()
{
    result = confirm("請問你確定要刪除此筆訂單嗎?");
    if (result == true) {
        alert("訂單已刪除！");
        let check = true;
        const request = new XMLHttpRequest();
        request.open("POST", "/delete_order");
        request.send();
    }
    else {
        alert("刪除訂單失敗");
    }
}
function Change()
{
    result = confirm("請問你確定要更改此筆訂單嗎?");
    if (result == true) {
        alert("訂單已更改！");
        const request = new XMLHttpRequest();
        request.open("POST", "/check_record_revise");
        request.send();
    }
    else {
        alert("更改訂單失敗");
    }
}