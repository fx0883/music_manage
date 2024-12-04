(function(django) {
    console.log('Image Auto Title Script initialized'); // 脚本初始化日志
    
    var $ = django.jQuery;  // 使用 django.jQuery 替代 $
    
    // 等待 DOM 加载完成
    $(document).ready(function() {
        console.log('DOM Ready'); // DOM 加载完成日志
        
        // 获取表单字段
        var $imageField = $('#id_image');
        var $titleField = $('#id_title');
        
        // 记录字段是否找到
        console.log('Form fields found:', {
            imageField: $imageField.length > 0,
            titleField: $titleField.length > 0
        });
        
        // 获取预览图容器
        var $previewContainer = $('label').filter(function() {
            return $(this).text() === '图片预览:';
        }).next('.readonly');
        
        console.log('Preview container found:', {
            found: $previewContainer.length > 0,
            text: $previewContainer.text()
        });
        
        // 获取CSRF token
        var csrftoken = $('[name=csrfmiddlewaretoken]').val();
        
        // 设置CSRF token到所有AJAX请求的头部
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        
        // 监听图片文件输入变化
        $imageField.on('change', function() {
            console.log('Image field changed'); // 文件字段变化日志
            
            var filename = this.value.split('\\').pop().split('/').pop();
            // 移除文件扩展名
            filename = filename.replace(/\.[^/.]+$/, "");
            // 直接设置标题，无论是否为空
            $titleField.val(filename);
            console.log('Title updated:', filename); // 标题更新日志
            
            // 如果有文件被选中，显示预览
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $previewContainer.html(
                        `<img src="${e.target.result}" style="max-width: 400px; display: block;" />`
                    );
                    console.log('Preview image updated'); // 预览图更新日志
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
        
        // 监听表单提交事件
        $('form').on('submit', function(e) {
            console.log('Form submitted'); // 表单提交日志
        });
    });
})(django); 