(function(django) {
    console.log('Font Info Script initialized'); // 脚本初始化日志
    
    var $ = django.jQuery;  // 使用 django.jQuery 替代 $
    
    // 等待 DOM 加载完成
    $(document).ready(function() {
        console.log('DOM Ready'); // DOM 加载完成日志
        
        // 获取当前页面的完整URL路径
        var currentPath = window.location.pathname;
        // 获取基础admin路径
        var adminPath = currentPath.split('/chinese/fontinfo/')[0] + '/chinese/fontinfo';
        // 构建完整的API路径
        var applyFontUrl = adminPath + '/apply_font/';
        var clearFontUrl = adminPath + '/clear_font/';
        
        console.log('API URLs:', {
            currentPath: currentPath,
            adminPath: adminPath,
            applyFontUrl: applyFontUrl,
            clearFontUrl: clearFontUrl
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
        
        // 获取表单字段
        var $fileField = $('#id_file');
        var $categoryField = $('#id_category');
        var $nameField = $('#id_name');
        var $codeField = $('#id_code');
        var $previewField = $('#id_preview_image');
        
        // 记录字段是否找到
        console.log('Form fields found:', {
            fileField: $fileField.length > 0,
            categoryField: $categoryField.length > 0,
            nameField: $nameField.length > 0,
            codeField: $codeField.length > 0,
            previewField: $previewField.length > 0
        });
        
        // 创建按钮
        var $applyBtn = $('<input type="button" value="应用" class="button" style="margin-left: 10px;" disabled/>');
        var $clearBtn = $('<input type="button" value="清除" class="button" style="margin-left: 10px;"/>');
        
        console.log('Buttons created'); // 按钮创建日志
        
        // 添加按钮到表单
        $fileField.parent().append($applyBtn).append($clearBtn);
        console.log('Buttons appended to form'); // 按钮添加到表单日志
        
        // 获取预览图容器
        var $previewContainer = $('label').filter(function() {
            return $(this).text() === '预览图:';
        }).next('.readonly');
        
        console.log('Preview container found:', {
            found: $previewContainer.length > 0,
            text: $previewContainer.text()
        });
        
        // 检查按钮状态
        function checkApplyButton() {
            var fileValue = $fileField.val();
            var categoryValue = $categoryField.val();
            console.log('Button state check:', { 
                fileValue: fileValue, 
                categoryValue: categoryValue 
            }); // 按钮状态检查日志
            $applyBtn.prop('disabled', !(fileValue && categoryValue));
        }
        
        // 绑定事件
        $fileField.on('change', function() {
            console.log('File field changed:', $fileField.val()); // 文件字段变化日志
            checkApplyButton();
        });
        
        $categoryField.on('change', function() {
            console.log('Category field changed:', $categoryField.val()); // 分类字段变化日志
            checkApplyButton();
        });
        
        // 应用按钮点击事件
        $applyBtn.on('click', function() {
            console.log('Apply button clicked');
            
            // 获取文件输入框中的文件
            var fileInput = $fileField[0];
            if (!fileInput.files || !fileInput.files[0]) {
                console.error('No file selected');
                return;
            }

            // 创建 FormData 对象
            var formData = new FormData();
            formData.append('font_file', fileInput.files[0]);
            formData.append('csrfmiddlewaretoken', csrftoken);
            
            console.log('Sending apply request to:', applyFontUrl);
            
            $.ajax({
                url: applyFontUrl,
                type: 'POST',
                data: formData,
                processData: false,  // 不处理数据
                contentType: false,  // 不设置内容类型
                success: function(response) {
                    console.log('Apply request succeeded:', response);
                    if (response.success) {
                        $nameField.val(response.font_name);
                        $codeField.val(response.font_code);
                        
                        // 创建预览图文件
                        var blob = new Blob(
                            [new Uint8Array([...response.preview_data].map(c => c.charCodeAt(0)))],
                            {type: 'image/png'}
                        );

                        // 创建预览图的 URL
                        var imageUrl = URL.createObjectURL(blob);
                        
                        // 直接替换 readonly div 的内容
                        $previewContainer.html(
                            `<img src="${imageUrl}" style="max-width: 400px; display: block;" />`
                        );

                        // 保存 blob 和文件名，供后续表单提交时使用
                        $previewContainer.data('previewBlob', blob);
                        $previewContainer.data('previewFilename', response.font_code + '_preview.png');
                        
                        console.log('Preview image updated');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Apply request failed:', {
                        status: status,
                        error: error,
                        response: xhr.responseText
                    });
                    alert('生成预览失败: ' + (xhr.responseJSON?.error || '未知错误'));
                }
            });
        });
        
        // 清除按钮点击事件
        $clearBtn.on('click', function() {
            console.log('Clear button clicked'); // 清除按钮点击日志
            $nameField.val('');
            $codeField.val('');
            $previewField.val('');
            // 恢复原始的"无预览图"文本
            $previewContainer.html('无预览图');
            // 清除保存的 blob 数据
            $previewContainer.removeData('previewBlob');
            $previewContainer.removeData('previewFilename');
        });
        
        // 监听表单提交事件，在提交时处理预览图
        $('form').on('submit', function(e) {
            var previewBlob = $previewContainer.data('previewBlob');
            var previewFilename = $previewContainer.data('previewFilename');
            
            if (previewBlob && previewFilename) {
                // 创建文件对象
                var file = new File([previewBlob], previewFilename, {type: 'image/png'});
                
                // 更新预览图字段
                let container = new DataTransfer();
                container.items.add(file);
                $previewField[0].files = container.files;
            }
        });
    });
})(django); 