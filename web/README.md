# GestureRecognition web 应用

调用方法，用浏览器打开 classify.html 即可。

注意事项：

classify.html 中的 tts 方法中参数tok，如果过期了之后，需要自己在百度 AI 平台申请一个语音合成账号获取对应的

Api Key 和 SecretKey。然后访问 https://openapi.baidu.com/oauth/2.0/token 换取 token。

访问地址如下：

    // appKey = Va5yQRHl********LT0vuXV4
    // appSecret = 0rDSjzQ20XUj5i********PQSzr5pVw2
    
    https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=Va5yQRHl********LT0vuXV4&client_secret=0rDSjzQ20XUj5i********PQSzr5pVw2

tts 方法

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