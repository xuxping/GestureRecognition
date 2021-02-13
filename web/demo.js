// 初始化变量
var audio = null;
var playBtn = null;
$(function () {
     $("#file1").change(function() {
            //获取到input的value，里面是文件的路径
            var filePath = $(this).val();
            var fileFormat = filePath.substring(filePath.lastIndexOf(".")).toLowerCase();
            //转成可以在本地预览的格式
            var src = window.URL.createObjectURL(this.files[0]);
            // 检查是否是图片
            if( !fileFormat.match(/.png|.jpg|.jpeg/) ) {
                error_prompt_alert('上传错误,文件格式必须为：png/jpg/jpeg');
                return;
            }
            $('#test1').attr('src', src);
            // 将图片转成流
            var file = $("#file1")[0].files[0];
            upload(file);
            // 调用接口
            // testapi(files);
        });
 });

function getMedia() {
    let constraints = {
        video: {width: 200, height: 200},
        audio: true
    };
    //获得video摄像头区域
    let video = document.getElementById("video");
    //这里介绍新的方法，返回一个 Promise对象
    // 这个Promise对象返回成功后的回调函数带一个 MediaStream 对象作为其参数
    // then()是Promise对象里的方法
    // then()方法是异步执行，当then()前的方法执行完后再执行then()内部的程序
    // 避免数据没有获取到
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function (MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    });
}

  function takePhoto() {
    //canvas = null;
    //video = null;
    //获得Canvas对象
    let video = document.getElementById("video");
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, 200, 200);
    var strDataURI = canvas.toDataURL("image/jpeg");
    //saveBase64File(strDataURI, '');
    var imgbolog = toblob(strDataURI);
    upload(imgbolog);
    $("#demo2").attr('src', strDataURI);
  }

  function toblob(content) { //下载base64图片
    var base64ToBlob = function(code) {
        let parts = code.split(';base64,');
        let contentType = parts[0].split(':')[1];
        let raw = window.atob(parts[1]);
        let rawLength = raw.length;
        let uInt8Array = new Uint8Array(rawLength);
        for(let i = 0; i < rawLength; ++i) {
            uInt8Array[i] = raw.charCodeAt(i);
        }
        return new Blob([uInt8Array], {
            type: contentType
        });
    };
    let aLink = document.createElement('a');
    return base64ToBlob(content); //new Blob([content]);
};

var upload = function (file) {
    var formData = new FormData();
    var blockSize = 1024 * 1024 * 2;
    var fileData = file.slice(0, blockSize);
    formData.append("filename1", fileData);
    // formData.append("fileName", file.name);
    $.ajax({
        url: "http://47.74.234.157:48703/api/classify",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (result) {
            var result = eval("(" + result + ")");
            // 如果预测成功，网页显示预测结果，然后进行语音播报
            if(result.status == 0) {
                $("#result").text(result.predicts[0]);
                // 调用接口进行语音合成
                tts("手势识别结果是：" + result.predicts[0]);
            }
        }
    });
};

// 合成语音
function tts(text) {
    // let text = document.getElementById('text').value;
    //playBtn.innerText = '准备中';
    // 调用语音合成接口
    // 参数含义请参考 https://ai.baidu.com/docs#/TTS-API/41ac79a6
    audio = btts({
        tex: text,
        tok: '25.c7a17a6e42fb7b16ef8938d79c837f52.315360000.1861685473.282335-14433392',
        spd: 5,
        pit: 5,
        vol: 15,
        per: 4
    }, {
        volume: 0.3,
        autoDestory: true,
        timeout: 10000,
        hidden: false,
        onInit: function (htmlAudioElement) {
        },
        onSuccess: function(htmlAudioElement) {
            audio = htmlAudioElement;
            playBtn.innerText = '播放';
        },
        onError: function(text) {
            alert(text)
        },
        onTimeout: function () {
            alert('timeout')
        }
    });
}

/**
 * 调用手势识别 api
 * @param files 图片，图片类型为 blob 类型
 */
function testapi(files){
    $.ajax({
        url :"http://47.74.234.157:48703/api/classify",
        dataType :'json',
        type : "POST",
        async : false,
        data: files,
        success : function(result) {
            alert(result);
            $("#result").text(result);
        }
    });
};
