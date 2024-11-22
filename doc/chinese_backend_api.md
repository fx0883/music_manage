# 项目需求
需要开发一款教外国人学习中国古诗词的app，后端系统使用Django开发。主要功能如下：

1. **古诗词浏览功能**
    - 外国人可浏览古诗词，古诗词每句中每个字都要有拼音、中文注释、译文和赏析。
    - 同时要有各国语言的注释、译文和赏析，但每次仅显示当前所选外语对应的内容，不显示所有外语信息。

2. **古诗词排序功能**
古诗词可根据难易程度排序，也可按其他所需方式排序。

3. **背诵功能**
    - 有背诵古诗词的功能，背诵时会随机出题。
    - 题目是从古诗词中抽取一句话或几个汉字，让使用者填空。

4. **作者信息展示功能**
每个古诗词都要展示其作者的信息和图片，还有创作背景。展示时根据当前语言显示对应信息。




# 数据库模型
数据库模型已经生成，请在chinese/models目录下查看。

# 需要完成的功能
目前打开的目录是当前django项目的根目录，需要根据上面的需求完成相关功能。
1 完成所有需要用到的restful api
2 在views文件夹中实现所有api接口
3 在serializers 文件夹中实现所有api接口的数据序列化
4 在models 文件夹中已经实现所有api接口需要用到的数据库模型
5 在tests.py中实现所有api接口的测试用例
6 所有的api需要有openapi文档, 请参考music/views/permalink_view.py中的写法

类似这样的
class PermalinkToOfficialURLAPIView(APIView):
    """
    API to return the official URL given a permalink_url.
    """

    @extend_schema(
        operation_id='Permalink to Official URL API',
        summary='Retrieve official URL from permalink',
        description='This API accepts a permalink URL and returns the corresponding official URL.',
        request={
            'application/json': OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                'Permalink Request Example',
                value={
                    'permalink_url': 'https://soundcloud.com/nguyengocnhuynhxd/nhu-uoc-nguyen-vuong-phi',
                },
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,  # Define the structure of the 200 response
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






7 所有的api都要定义在chinese/urls.py中
