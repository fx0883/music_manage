(function($) {
    console.log('Font Info Script initialized'); // 脚本初始化日志

    // 等待 DOM 加载完成
    $(document).ready(function() {
        console.log('DOM Ready'); // DOM 加载完成日志
        
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
            console.log('Apply button clicked'); // 应用按钮点击日志
            var file_path = $fileField.val();
            if (!file_path) return;
            
            console.log('Sending apply request:', { file_path }); // AJAX 请求日志
            $.ajax({
                url: 'apply_font/',
                type: 'POST',
                data: {
                    file_path: file_path,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    console.log('Apply request succeeded:', response); // 请求成功日志
                    if (response.success) {
                        $nameField.val(response.font_name);
                        $codeField.val(response.font_code);
                        
                        // 创建预览图文件
                        var blob = new Blob(
                            [new Uint8Array([...response.preview_data].map(c => c.charCodeAt(0)))],
                            {type: 'image/png'}
                        );
                        var file = new File([blob], response.font_code + '_preview.png', {type: 'image/png'});
                        
                        // 更新预览图字段
                        let container = new DataTransfer();
                        container.items.add(file);
                        $previewField[0].files = container.files;
                        console.log('Preview image updated'); // 预览图更新日志
                    }
                },
                error: function(xhr) {
                    console.error('Apply request failed:', xhr); // 请求失败日志
                    alert('生成预览失败: ' + (xhr.responseJSON?.error || '未知错误'));
                }
            });
        });
        
        // 清除按钮点击事件
        $clearBtn.on('click', function() {
            console.log('Clear button clicked'); // 清除按钮点击日志
            var preview_path = $previewField.val();
            
            console.log('Sending clear request:', { preview_path }); // 清除请求日志
            $.ajax({
                url: 'clear_font/',
                type: 'POST',
                data: {
                    preview_path: preview_path,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    console.log('Clear request succeeded:', response); // 清除成功日志
                    if (response.success) {
                        $nameField.val('');
                        $codeField.val('');
                        $previewField.val('');
                    }
                },
                error: function(xhr) {
                    console.error('Clear request failed:', xhr); // 清除失败日志
                    alert('清除失败: ' + (xhr.responseJSON?.error || '未知错误'));
                }
            });
        });
    });
})(django.jQuery); 