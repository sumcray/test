var xmlhttp;
var winlink = "http://" + window.location.href.substring(7, window.location.href.indexOf(":", 7));
if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
}
else {// code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
function zmove() {
    var x = document.getElementById("xian2");
    var angle = 0, lastTime = null, wz = 0;
    function m(time) {
        if (lastTime != null)
            angle += (time - lastTime) * 0.001;
        lastTime = time;
        wz = 25 + angle * 200;
        if (wz > 55)
            wz = 55;
        x.style.marginLeft = wz + '%';
        if (wz < 55)
            requestAnimationFrame(m);
    }
    requestAnimationFrame(m);
}
function dmove() {
    var x = document.getElementById("xian2");
    var angle = 0, lastTime = null, wz = 0;
    function m(time) {
        if (lastTime != null)
            angle += (time - lastTime) * 0.001;
        lastTime = time;
        wz = 55 - angle * 200;
        if (wz < 25)
            wz = 25;
        x.style.marginLeft = wz + '%';
        if (wz > 25)
            requestAnimationFrame(m);
    }
    requestAnimationFrame(m);
}
function zhu() {
    //document.getElementById("xian2").style.cssText = "margin-left:55%;";
    zmove();
    document.getElementById("login").onclick = deng;
    document.getElementById("res").onclick = '';
    document.getElementById("form1").style.display = "none";
    document.getElementById("form2").style.display = "";
}
function deng() {
    //document.getElementById("xian2").style.cssText = "margin-left:25%;";
    dmove();
    document.getElementById("login").onclick = '';
    document.getElementById("res").onclick = zhu;
    document.getElementById("form2").style.display = "none";
    document.getElementById("form1").style.display = "";
}
function login() {
    var userid = document.getElementById("userid").value;
    var pwd = document.getElementById("pwd_t").value;
    if (userid === '' || pwd === '') {
        alert('请输入账号密码');
        return;
    }
    xmlhttp.open("post", winlink + ":8888/login", true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var res = xmlhttp.responseText;
            if (res === '账号密码错误' || res === '账号不存在')
                alert(res);
            else {
                var json = JSON.parse(res);
                var session = window.sessionStorage;
                session.clear;
                session.setItem("uid", json.id);
                session.setItem("name", json.name);
                session.setItem("userid", json.userid);
                session.setItem("pwd", json.pwd);
                window.location.href = winlink + ":8888/list"
            }
        }
    }
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("userid=" + userid + "&pwd=" + pwd);
}
function regist() {
    var userid = document.getElementById("userid2").value;
    var pwd = document.getElementById("pwd_t2").value;
    var name = document.getElementById("name2").value;
    xmlhttp.open("post", winlink + ":8888/regist", true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var res = xmlhttp.responseText;
            if (res === '账号已存在')
                alert(res);
            else {
                document.getElementById("userid").value = userid;
                document.getElementById("pwd_t").value = pwd;
                var button = document.getElementById("login_x")
                button.onclick();
            }
        }
    }
    if (userid === "" || pwd === "" || name === "") {
        alert("注册信息不能为空");
    } else {
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send("userid=" + userid + "&pwd=" + pwd + "&name=" + name);
    }
}