django.jQuery(function($) {
    // 添加按钮到表单
    var $fileField = $('#id_file');
    var $categoryField = $('#id_category');
    var $nameField = $('#id_name');
    var $codeField = $('#id_code');
    var $previewField = $('#id_preview_image');
    
    var $applyBtn = $('<input type="button" value="应用" class="default" style="margin-left: 10px;" disabled/>');
    var $clearBtn = $('<input type="button" value="清除" class="default" style="margin-left: 10px;"/>');
    
    $fileField.after($clearBtn);
    $fileField.after($applyBtn);
    
    // 检查按钮状态
    function checkApplyButton() {
        $applyBtn.prop('disabled', !($fileField.val() && $categoryField.val()));
    }
    
    $fileField.on('change', checkApplyButton);
    $categoryField.on('change', checkApplyButton);
    
    // 应用按钮点击事件
    $applyBtn.click(function() {
        var file_path = $fileField.val();
        if (!file_path) return;
        
        $.ajax({
            url: 'apply_font/',
            type: 'POST',
            data: {
                file_path: file_path,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
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
                }
            },
            error: function(xhr) {
                alert('生成预览失败: ' + (xhr.responseJSON?.error || '未知错误'));
            }
        });
    });
    
    // 清除按钮点击事件
    $clearBtn.click(function() {
        var preview_path = $previewField.val();
        
        $.ajax({
            url: 'clear_font/',
            type: 'POST',
            data: {
                preview_path: preview_path,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.success) {
                    $nameField.val('');
                    $codeField.val('');
                    $previewField.val('');
                }
            },
            error: function(xhr) {
                alert('清除失败: ' + (xhr.responseJSON?.error || '未知错误'));
            }
        });
    });
}); 