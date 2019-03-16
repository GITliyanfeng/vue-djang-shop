####################
from rest_framework.pagination import PageNumberPagination


# 定制分页 StandarResultsSetPagination 标准结果设置分页
class GoodsSetPagination(PageNumberPagination):
    """
    通过这个设置,我们可以根据前台的page_size参数请求每一页有多少条数据 区间在 10-100
    通过参数p来定位当前的页面是第几页
    """
    page_size = 12
    # 参数的名字  page_size  page
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100
