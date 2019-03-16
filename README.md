# 前后端分离生鲜项目

---

## 系统构成:

+ Xadmin后台系统
+ 商品和分类数据
+ Vue前端项目

对于Vue:

+ API借接口
+ Vue组件的交互过程
+ Vue项目组织结构分析

## Django Rest Framework 实现的功能:

1. 通过view实现rest api接口
    + ApiView方式实现api
    + GenericView方式实现api
    + Viewset和router方式实现api和url配置
    + django_filter,SearchFilter,OrderFilter,分页
    + 通用mixins
2. 权限认证
    + Authentication用户认证设置
    + 动态设置permission,Authentication(权限,认证)
    + Validators实现字段验证
3. 序列化和表单验证
    + Serializer(串行)
    + ModelSerializer
    + 动态设置Serializer
4. 登录支付和注册
    + json web token 实现登录
    + 手机注册
    + 支付宝支付
    + 第三方登录
5. 进阶开发
    + django rest framework部分核心源码的解读
    + 文档自动化管理
    + django rest framework的缓存
    + Throttling(节流)对用户和ip进行限速
    
---

## 常见问题:

+ 本地系统中不能重现的发生在远程系统上的bug
+ api借口出错不能及时的发现或者找到错误的位置(错误栈)
+ api文档管理问题
+ 大量的url配置难以维护
+ 接口跟新后不能及时的去更新文档,用户不知道如何和去测试接口,但是写文档会花费大量的时间去维护
+ 防止爬虫,限制用户访问频率
+ 某些页面缓存加速访问

---

## 一些问题的解决方案:

+ pycharm的远程服务器代码调试技巧让大家不仅可以调试支付,第三方登录还可以调试远程服务器的代码来重现服务器上的bug
+ Docker搭建sentry体验错误日志监控系统,让我们不仅可以得到线上的错误栈还能及时在发生系统错误的时候收到邮件通知
+ django rest framework的文档自动化管理工具以及url的注册管理功能来节省写文档的时间
+ django rest framework的自动化文档管理工具可以直接用来测试接口,自动生成js接口代码,shell测试代码和python测试代码
+ django rest framework体统throttle来对api进行访问频率的限制
+ 引入第三方框架来设置某些api的缓存

----

## django进阶知识点:

+ django migrations的原理
+ django信号量
+ django请求到相应的完整过程
+ 独立使用django的Model

## Vue知识点:

+ Vue技术选型分析
+ API接口测试数据填充到Vue组件模板
+ Vue代码结构分析

## 环境搭建

---

`sudo apt-get mysql-sever`

检测MySQL服务是否启动  `ps sux | grep mysqld`

登录 `mysql -uname -ppassword`

---

配置MySQL

远程连接:

```shell
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

# 改变
bind-address = 0.0.0.0

# 注意
# * Basic Setting 中指明了
# pid sock port basedir datadir tmpdir
```

修改配置后要重启服务 `sudo service mysql restart`

增加权限设置

`GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'rootpassword' WITH GRANT OPTION;`

`FLUSH PRIVILEGES;`



Vue 项目环境的搭建

+ nodejs
+  cnpm

Ubuntu安装

```shell
# Using Ubuntu
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
```

插件

```shell
＃在Ubuntu上使用`sudo`或者在debian 
apt-get install -y build-essential上以root身份运行它
```

配置cnpm 镜像

```shell
sudo npm install -g cnpm --registry=https://registry.npm.taobao.org  

# 配置cnpm淘宝镜像
```

以后使用命令的时候不再使用npm而是使用cnpm

打开下载的前端Vue项目,在项目目录打开shell,执行`cnpm install`安装为当前项目安装依赖包,下载的依赖包会放在项目目录的nodejs_models文件夹里面

当依赖包安装完成之后,运行`cnpm run dev`这样这个前端的项目就会运行起来

###　Conda创建虚拟环境

+  列出虚拟环境  `conda env -list`
+ 创建虚拟环境 `conda create -n your_env_name python=X.X `
+ Ubuntu启动虚拟环境 `source activate your_env_name`
+ Ubuntu退出虚拟环境 `source deactivate`
+ 在虚拟环境中正常使用 pip conda 包管理工具(默认针对当前虚拟环境)
+ 指定虚拟环境安装模块 `conda install -n your_env_name [package]`
+ 删除虚拟环境 `conda remove -n your_env_name(虚拟环境名称) --all`
+ 指定删除某个虚拟环境中的某个包 `conda remove --name your_env_name  package_name `
+ **注意**: windows中 启动和退出虚拟环境的命令需要将**source**去掉



---

当前项目需要的模块

首先切换到虚拟环境

```shell
# 速度慢使用豆瓣源 pip install -i https://pypi.douban.com/simple markdowm(包名)
pip install django==1.11.*
pip install markdown
pip install djangorestframework
pip install django-filter
pip install mysqlclient  # django连接mysql的驱动
pip install pillow  # 图片处理的包
```

windows上安装mysqlclient的时候容易出错,出错之后的解决方法是:

打开网址: https://www.lfd.uci.edu/~gohlke/pythonlibs/

## 建立项目

---

在pycharm中操作:

+ 选择建立Django项目
  + location 设置新建的项目的路径
  + Interpreter  设置解释器环境
  + moresettings  设置 app 名字 users   取消选中admin 因为我们要使用xadmin



建立完成之后通过pycharm工具栏上的run  选择 run -- django运行当前环境,检测是否这个项目可以成功的启动

浏览器输入 127.0.0.0:8000 页面显示 It work 表示项目启动成功



### 配置文件

创建数据库

`CREATE DATABASE "django_vue_shop" DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;`

修改数据库驱动

```python
# settings.py


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "django_vue_shop",
        'USER':"root",
        'PASSWORD':"Qq957012678",
        'HOST':"127.0.0.1",
        'OPTIONS':{'init_command':'SET storage_engine=INNODB;'}
    }
}
'''
如果报错 django.db.utils.OperationalError: (1193, "Unknown system variable 'storage_engine'")
'''
# 那么 storage_engine=INNODB 改为 default_storage_engine=INNODB
```





目录结构

```shell
├── apps                        新建的apps包 存放我们建立的app
│   ├── __init__.py
│   └── users					建立的app  users
├── db_tools					是一个目录 存放和数据库操作相关脚本
├── DjangoVue                   项目配置文件
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── extra_apps                 新建的extra_apps存放使用的第三方包
│   └── __init__.py
├── manage.py 
├── media                      新建的目录用来存放媒体文件
└── templates                  新建的目录用来存放模板
```

在配置文件中将apps   以及 extra_apps 两个包添加到项目全局变量

```python
# settings.py

# 放在BASE_DIR变量下面

############-----将创建的apps 和 extra_apps加入到项目变量------#########
import sys
sys.path.insert(0,BASE_DIR)
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
sys.path.insert(0,os.path.join(BASE_DIR,'extra_apps'))
###################################################################

```

### 模型构建

---

#### 分析组成结构

1. 商品分类
   + 生鲜食品    (一级分类)
     + 精品肉类    (二级分类)
       + 猪肉    (三级分类)
       + 牛肉
       + 羊肉
       + ....
     + 海鲜水产
     + ....
2. 导航栏
   + 首页
   + 生鲜食品  (其实是以一级类中的一部分)
   + 粮油副食
   + ....

---

点开生鲜食品这个类别后,跳转到这个分类的列表页:(组成)

1. 左侧栏  (选中分类下面的分类详情)
   + 精品肉类
     + 猪肉
     + 羊肉
     + ...
   + 海鲜水产
     + ...
   + ...
2. 中上侧栏  价格过滤条件
3. 中上侧栏下方的按价格排序按钮  实现商品的价格排序
4. 下册 分页

---

点开单个商品进入商品详情页(组成)

1. 左侧商品轮播图
2. 右侧商品信息
   + 商品名
   + 是否免运费
   + 市场价格
   + 售价
   + 销量
   + 购买数量input框
3. 下侧商品详情    富文本
4. 右侧热卖商品    列表

---

用户登录之后(组成)

+ 会员中心
  1. 个人资料  (可编辑)
     + 出生日期
     + 姓名
     + 性别
     + 电子邮件
     + 手机号
  2. 我的订单
     + 订单列表  (可以取消订单)
       + 订单号
       + 下单时间
       + 订单金额
       + 订单状态
     + 点击订单号--进入订单详情(组成)
       + 订单号
       + 下单时间
       + 订单金额
       + 订单状态    未支付会在这里显示立即支付它的按钮
       + 商品列表
         + 订单中的商品的列表
  3. 收货地址(组成,同样结构的表格)
     + 配送区域   三级联动
     + 收货人姓名
     + 详细地址
     + 手机号
     + 确认修改和删除的按钮
  4. 收藏
     + 商品名称
     + 价格
     + 操作 删除
  5. 留言
     + 我的留言列表  删除按钮 查看上传文件按钮
     + 发布一个留言
       + 留言类型(单选)
         + 留言
         + 投诉
         + 询问
         + 售后
         + 求购
       + 主题  (input)
       + 内容  ( text)
       + 上传文件按钮
       + 提交按钮
+ 导航栏购物城mini显示
  + 购物车内的商品
  + 删除按钮
  + 去结算按钮
+ 购物车
  + 商品列表
  + 删除按钮
  + 清空购物车
  + 添加收货人地址
  + 结算按钮

#### 分析需要那些app  归类

+ users                  记录用户信息
+ goods                 记录商品信息
+ trade                   交易相关信息  购物车  订单
+ user_operation   记录用户操作  收藏

在Toos中 打开 run manage task  运行 manage  使用manage命令来创建app

`startapp appname`

将创建完成的app移动到apps包中

#### 各个模型的构建

---

##### user中的模型

```python
# users/models.py

from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# 需要更改配置文件 AUTH_USER_MODEL
class UserProfile(AbstractUser):
    '''
    用户
    '''
    GENDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女'),
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    gender = models.CharField(max_length=6, verbose_name='性别', choices=GENDER_CHOICES, default='male', )
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='电子邮箱')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    '''
        储存获取到的短信验证码,用来对比验证
        可以储存在非关系型数据库中--Redis
    '''
    code = models.CharField(max_length=10, verbose_name='短信验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
```

在settings中配置更改后的User表

```python
# settings.py

# UserProfile  加在settings 文件中

AUTH_USER_MODEL = 'users.UserProfile'
```

##### goods中的模型

```python
# apps/models.py

from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class GoodsCategory(models.Model):
    """
    商品分类
        分类有三个等级
        通过一个表来定义分类的从属关系,而不是定义三个model将三个等级写死
    """
    CATEGORY_TYPES = (
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类'),
    )
    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别code', help_text='类别code')
    desc = models.CharField(max_length=200, default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPES, verbose_name='分类等级', help_text='分类等级')
    # parent_category自己指向自己 这里要用到self
    parent_category = models.ForeignKey('self', null=True, verbose_name='父类别', related_name='sub_cat')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''
    品牌
    '''
     category = models.ForeignKey(GoodsCategory, verbose_name='商品分类', null=True, blank=True)
    name = models.CharField(max_length=30, default='', verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(max_length=200, default='', verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brands/images/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '宣传品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    '''
        定义商品模型
    '''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品分类', )
    name = models.CharField(max_length=200, default='', verbose_name='商品名')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一标识', )
    click_num = models.IntegerField(default=0, verbose_name='商品点击量')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售量')
    fav_num = models.IntegerField(default=0, verbose_name='商品收藏量')
    goods_num = models.IntegerField(default=0, verbose_name='商品库藏量')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='销售价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品简述')
    goods_desc = UEditorField(max_length=500, verbose_name=u'商品详述', imagePath='goods/images/', filePath='goods/files/',
                             width=1000, height=300,
                             default='')
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销')
    good_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='商品主图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    '''
        详情页轮播图管理
    '''
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='images')
    image = models.ImageField(upload_to='', verbose_name='图片', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', )

    class Meta:
        verbose_name = '详情页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图')
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords

```

将第三方app    DjangoUeditor  放到 extra_app包中

配置app

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'users',
    'goods',
    'trade',
    'user_operation',
]
```

##### trade中的模型

```python
# trade/models.py

from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    goods_num = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品:{}({})件".format(self.goods.name, self.goods_num)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ('success', '成功'),
        ('cancel', '取消'),
        ('cancel', '待支付'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    order_sn = models.CharField(unique=True, max_length=30, verbose_name='订单号')
    nonce_str = models.CharField(max_length=50, null=True, blank=True, verbose_name='随机码')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付宝单号')
    pay_status = models.CharField(max_length=10, choices=ORDER_STATUS, verbose_name='订单状态')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name='收货地址')
    singer_name = models.CharField(max_length=20, default="", verbose_name='签收人')
    singer_mobile = models.CharField(max_length=11, verbose_name='联系电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name='订单信息')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    goods_num = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)

```



##### user_preation中的模型

```python
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    """
    用户的收藏
    """
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    msg_type = models.IntegerField(choices=MESSAGE_CHOICES, default=1, verbose_name='留言类型',
                                   help_text='留言类型:1-留言,2-投诉,3-询问,4-售后,5-求购')
    subject = models.CharField(max_length=100, default="", verbose_name='留言主题', help_text='留言主题')
    message = models.TextField(default="", verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(upload_to="message", verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='用户')
    district = models.CharField(max_length=100, default="", verbose_name='区域')
    address = models.CharField(max_length=100, default="", verbose_name='详细地址')
    singer_name = models.CharField(max_length=100, default="", verbose_name='签收人')
    singer_mobile = models.CharField(max_length=11, default="", verbose_name='签收人')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

```

#### Django migration操作

---

在 manage Task中输入

`makemigrations`  在每个app的migrations文件夹下生成数据库的变动文件000X_initial.py

输入`migrate` 将变动文件中的变动应用到数据库

`migrate [appname]`会指定那个app应用数据库变动,如果不指定appname,那么会应用所有的app



执行完成`migrate`之后查看数据库生成的表

```shell
mysql> show tables;
+------------------------------------+
| Tables_in_django_vue_shop          |
+------------------------------------+
| auth_group                         |
| auth_group_permissions             |
| auth_permission                    |
| django_content_type                |
| django_migrations                  |
| django_session                     |
| goods_banner                       |
| goods_goods                        |
| goods_goodscategory                |
| goods_goodscategorybrand           |
| goods_goodsimage                   |
| trade_ordergoods                   |
| trade_orderinfo                    |
| trade_shoppingcart                 |
| user_operation_useraddress         |
| user_operation_userfav             |
| user_operation_userleavingmessage  |
| users_userprofile                  |
| users_userprofile_groups           |
| users_userprofile_user_permissions |
| users_verifycode                   |
+------------------------------------+
21 rows in set (0.00 sec)

```

auth以及django开头的表是django自带的表

剩余的以appname_modelname[小写]命名的是我们model定义的表

不再生成auth_user表,而是生成users_userprofile表

**数据表改变的时候的坑**

每次修改model中的某些字段之后,通过`makemigrations`会在相应的migrations目录生成一个变化文件,文件内容包含模型的变化,然后通过`migrate`命令执行变化,Django是通过检查数据库中的` django_migrations `表,这个表中定义了--**哪个app**--**在什么时候-**-应用了**哪一个变化文件**,通过对比这个表,django才能确定哪些变化文件是需要执行的,哪些变化文件已经执行过了,不用再执行了.

**注意:**尽量不要使用手动sql修改表,和使用migrate混用,容易在ORM操作的时候发生错误





#### 将xadmin植入到当前系统

---

将配置好的xadmin文件复制到extra_app中,并且在setting中添加app

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'users.apps.UsersConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',
    'crispy_forms',  # xadmin需要的
    'xadmin',

]

```



安装xadmin的依赖包

```shell
pip install django-crispy-forms django-reversion django-formtools future httplib2 six

# 还有两个针对excel文件的导入导出的
pip install xlwt xlsxwriter
```

从完整源码中的app中将相应的adminx.py复制到对应的app中



当完成这些操作之后 执行 数据库 `makemigrations`     `migrate`

生成数据表

```shell
| xadmin_bookmark                    |
| xadmin_log                         |
| xadmin_usersettings                |
| xadmin_userwidget                  |
+------------------------------------+
```

为xadmin配置访问路由

```python
# urls.py
from django.conf.urls import url
import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
]
```

通过manage Task创建超级用户

`createsuperuser`

```shell
Username:  admin
电子邮箱:  1@1.com
Password:  admin123
Password (again):  admin123
```

更改中文显示

```python
# settings.py

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False
```

在每个app的目录下的apps.py中

```python
# 添加
verbose_name = '中文名字'
```

根据错误栈,调试bug

#### 通过脚本的方式导入数据

首先按照模型的定义的ImageFiled中的upload_to参数设计media目录的结构

向media中存入图片

在db_tools目录下创建脚本文件用来导入数据

**旨在:**通过脚本的方式单独操作models



```python
# 独立使用django的models

import os
import sys

# 获取当前脚本的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 通过当前脚本的路径找到上级目录的路径
sys.path.append(pwd + '../')
# 　如果我们要单独操作model,那么必须将model创建到项目的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoVue.settings")
import django

django.setup()
# 注意导入model必须在配置好django环境变量以及django.setup()之后,否则导入不成功

# 导入需要操作的model
from goods.models import GoodsCategory

# 测试导入是否成功
# all_categories = GoodsCategory.objects.all()
# 导入数据
from db_tools.data.category_data import row_data


def main():
    # 遍历数据,生成对象
    for lev_1_cat in row_data:
        # 实例化一个GoodsCategory对象
        lev_1_instance = GoodsCategory()
        lev_1_instance.code = lev_1_cat['code']
        lev_1_instance.name = lev_1_cat['name']
        lev_1_instance.category_type = 1
        lev_1_instance.save()

        for lev_2_cat in lev_1_cat['sub_categorys']:
            lev_2_instance = GoodsCategory()
            lev_2_instance.code = lev_2_cat['code']
            lev_2_instance.name = lev_2_cat['name']
            lev_2_instance.category_type = 2
            lev_2_instance.parent_category = lev_1_instance
            lev_2_instance.save()

            for lev_3_cat in lev_2_cat['sub_categorys']:
                lev_3_instance = GoodsCategory()
                lev_3_instance.code = lev_3_cat['code']
                lev_3_instance.name = lev_3_cat['name']
                lev_3_instance.category_type = 3
                lev_3_instance.parent_category = lev_2_instance
                lev_3_instance.save()
    print('Done')


if __name__ == '__main__':
    main()

```

检查数据库中是否添加了数据

`select * from goods_goodscategory limit 5;`

| id | name         | code | desc | category_type | is_tab | add_time|parent_category_id |
| ----| -------------- | ------| ------| --------------- | --------|---------------------------- | -------------------- |
|  1 | 生鲜食品     | sxsp |      |             1 |      0 | 2018-11-26 09:07:39.671820 |               NULL |
|  2 | 精品肉类     | jprl |      |             2 |      0 | 2018-11-26 09:07:39.683163 |                  1 |
|  3 | 羊肉         | yr   |      |             3 |      0 | 2018-11-26 09:07:39.686753 |                  2 |
|  4 | 禽类         | ql   |      |             3 |      0 | 2018-11-26 09:07:39.694651 |                  2 |
|  5 | 猪肉         | zr   |      |             3 |      0 | 2018-11-26 09:07:39.701729 |                  2 |

```python
# bd_tools/import_goods_data.py


#####

# 独立使用django的models

import os
import sys

# 获取当前脚本的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 通过当前脚本的路径找到上级目录的路径
sys.path.append(pwd + '../')
# 　如果我们要单独操作model,那么必须将model创建到项目的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoVue.settings")
import django

django.setup()
# 注意导入model必须在配置好django环境变量以及django.setup()之后,否则导入不成功

# 导入需要操作的model
from goods.models import Goods, GoodsCategory, GoodsImage

# 测试导入是否成功
# all_categories = GoodsCategory.objects.all()
# 导入数据
from db_tools.data.product_data import row_data


def main():
    for goods_detail in row_data:
        goods_instance = Goods()
        goods_instance.name = goods_detail['name']
        goods_instance.market_price = float(goods_detail['market_price'].replace("￥", "").replace('元', ''))
        goods_instance.shop_price = float(goods_detail['sale_price'].replace("￥", "").replace('元', ''))
        goods_instance.goods_brief = goods_detail['desc'] if goods_detail['desc'] is not None else ""
        goods_instance.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
        goods_instance.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

        # 由于是外键,需要获取category外键对象
        category_name = goods_detail["categorys"][-1]
        category = GoodsCategory.objects.filter(name=category_name)

        if category:
            goods_instance.category = category[0]
        goods_instance.save()

        # 还有轮播图
        for goods_images in goods_detail['images']:
            # 生成GoodImage对象
            goods_image_instance = GoodsImage()
            # 循环遍历生成对象,为goodsimage对象添加数据
            goods_image_instance.image = goods_images
            # 在一个循环中,图片所对应的商品外键是当前商品的实例
            goods_image_instance.goods = goods_instance
            goods_image_instance.save()
    print('Done')


if __name__ == '__main__':
    main()

```

检查数据:

`select id,name,category_id from goods_goods limit 5;`

| id | name                                        |category_id |
|----|------------------------------------------------------------|-------------|
|  1 | 新鲜水果甜蜜香脆单果约800克                                 |          20 |
|  2 | 田然牛肉大黄瓜条生鲜牛肉冷冻真空黄牛                        |           7 |
|  3 | 酣畅家庭菲力牛排10片澳洲生鲜牛肉团购套餐                    |          15 |
|  4 | 日本蒜蓉粉丝扇贝270克6只装                                  |          20 |
|  5 | 内蒙新鲜牛肉1斤清真生鲜牛肉火锅食材                         |           7 |

5 rows in set (0.00 sec)



`select id,image,goods_id from goods_goodsimage limit 5;`

| id | image                        | goods_id |
|----|------------------------------------|----------|
|  1 | goods/images/1_P_1449024889889.jpg |        1 |
|  2 | goods/images/1_P_1449024889264.jpg |        1 |
|  3 | goods/images/1_P_1449024889726.jpg |        1 |
|  4 | goods/images/1_P_1449024889018.jpg |        1 |
|  5 | goods/images/1_P_1449024889287.jpg |        1 |

5 rows in set (0.00 sec)

#### 配置media

虽然数据导入了,但是需要通过配置settings来解决页面图片无法显示的问题

```python
# settings.py


# 配置media    MEDIA_URL   MEDIA_ROOT 配置完成之后还需要配置urls.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

```python
# urls.py

from django.conf.urls import url
# from django.contrib import admin
import xadmin
from DjangoVue.settings import MEDIA_ROOT  # media
from django.views.static import serve      # media

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}), # media
]

```

重启以下项目

----



### 开始前后端分离

---

#### 前后端分离的优缺点

**问题一:**为什么出现前后端分离?

1. 为了,安卓,ios的移动端,pc端的多端适配
2. SPA开发模式的开始流行
3. 前后端开发职责划分不清,Templates谁来写?
4. 开发效率,旧的开发模式容易出现前端后端等待
5. 前端经常出现配合后端,能力受限
6. 后台开发语言和模板高度耦合,不利于框架的切换重构

**缺点:**

1. 增加前端学习门槛,后端满足数据规范增加门槛
2. 文档维护
3. 前端工作量增加
4. SEO难度增加,爬虫很难获取到数据
5. 需要单独增加ssr
6. 后端开发模式迁移增加成本

#### restful api

Representational State Transfer  资源状态转移

是目前,前后端分离的**标准**,而**非框架**

解释:

​	请求方式对应的是操作方法

​	url对应的是一组数据

​	两者相结合对应的是一中动作,或者说行为

例如:

​	请求方式是post    url对应的数据是 people

​	两者结合:   创建一个peopel

​	请求方式是get   url对应的数据是people

​	两者结合:   获取一个people	

常用动词:

+ GET                     获取所有,或者某个
+ PUT                     更新所有
+ POST                   创建
+ DELETE               删除
+ PATCH                  更新部分
+ HEAD
+ OPTIONS

过滤:

+ ?limit=10                            指定返回记录的数量
+ ?offset=10                          指定返回记录开始的位置
+ ?page=2&per)page=100    指定第几页以及每一页的记录数
+ ?sortby=name&order=asc  指点返回记录按照哪个属性排序,以及排的方式
+ ?animal_type_id = 1           指定筛选条件

**优点:**

+ 轻量的,遵循HTTP协议  post  get  put  delete 请求方式
+ 面向**资源**,每一个url对应的相应的资源(名词)
+ 数据描述简单,一般通过json或者xml数据通信

状态码:

+ 200    OK  服务器成功返回用户的数据
+ 201    CREATED   [POST/PUT/PATCH]  用户新建或者修改数据成功
+ 202    Accepted     [*]  表示一个请求已经进入后台排队(异步任务)
+ 204    NO  CONTENT   [DELETE]  用户删除数据成功
+ 400   INVALID  REQUEST  - [POST/PUT/PATCH]  用户请求错误,服务器没有进行新建或修改数据的操作
+ 401   Unauthorized  [*]  表示用户没有权限(令牌,用户名,密码错误)
+ 403  Forbidden   [*]  表示用户得到授权(与401错误相对),但是访问是被禁止的
+ 406  Not Acceptable   [GET]  用户请求的格式不可得
+ 410   Gone   用户请求的资源被永久删除
+ 422  Unprocesable entity   [POST/PUT/PATCH] 创建一个对象的时候,发生一个验证错误
+ 500   INTERNAL SEVER ERROR  [*]  服务器错误,用户无法判断请求是否成功

### Vue的几个概念

---

+ 前端工程化
+ 数据双向绑定
+ 组件化开发
+ webpack      是个js第三方的工具  将我们的前端项目转换为html css js
+ vue,vuex,vue-router,axios    Vue全家桶 
  + vuex  组件间通信
  + vue-router  路径和组件相关联,前端内部自己实现跳转
  + axios   Vue中用来替代ajax的工具,存在的原因(不推荐使用原生ajax的dom操作)
+ ES6,babel
  + ES6   js的语法标准
  + babel   一个将ES6转换成ES5的转换器,用来适配不支持ES6的浏览器

### 本项目的前端vue结构

---

+ .babelrc    babel配置文件

+ node_modules  第三方包

+ src  前端项目的源码
  + api  
  + axiso
  + components
  + router
  + static
  + store
  + styles
  + views  所有组件

## djangorestframework 开始

CBV   模式编程     class  base  view



序列化的几种方式

```python
# 原生django的 view 方式一

from django.views.generic.base import View
from goods.models import Goods


class GoodsListView(View):
    def get(self,request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            json_dict = {}
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            # json_dict['add_time'] = good.add_time  时间对象在dump的时候会出错
            # json_dict['goods_front_image'] = good.goods_front_image  image对象在dump的时候会出错
            json_list.append(json_dict)
        import json
        from django.http import HttpResponse
        return HttpResponse(json.dump(json_list),content_type='application/json')
    # 缺点,需要每个字段的获取数据,重组成字典,工足量大,代码量大,复用性低
            
```



```python
# 原生django的 view 方式二  使用model_to_dict 直接生成字典

from django.views.generic.base import View
from goods.models import Goods
from djang.forms.models import model_to_dict
import json
from django.http import HttpResponse

class GoodsListView(View):
    def get(self,request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            json_list.append(model_to_dict(good))
    	return Httpresponse(json.dump(json_list),content_type='application/json')
# 省去了重组字典的操作,但是还是会发生某些字段无法被dump的问题

```

```python
# 原生django的 view 方式二  使用 serializers 直接序列化
from django.views.generic.base import View
from goods.models import Goods
from django.core import serializers  # 串行器
from django.http import JsonResponse
import json

class GoodsListView(View):
    def get(self,request):
        goods = Goods.objects.all()
        json_data = serializers.seralize('json',goods)
        json_data = json.loads(json_data)
        return JsonResponse(json,safe=Falses)

# 存在的问题  model  pk 这两个字段和 其他字段分级,不再是同一级别,而且对于图片文件类别的字段,还需要后期添加域名,以及例如/media/这种操作,并不简单

```



以上原生的方式,虽然可以成功的返回json数据,但是还无法满足restful的要求,例如属于检测,认证,等一些列操作,都需要自己手写脚本来完成,工作量大,开发成本高.而通过djangorestframework可以很简单的完成这些操作来降低开发成本

#### 跟根据官方文档学习  django restframework

---

+ 杀手级别的 Web browsable API
+ 提供了 Authentication policies    OAuth1  和 OAuth2
+ Serialization  可以序列化ORM数据以及non-ORM数据
+ regular function-based view   FBV
+ 文档和强大的社区支持

版本  py5.6  django1.11

除了曾经装过的模块外,还需要安装

```shell
pip install django-guardian
pip install coreapi
```

使用restframework前需要的配置

```python
# settings.py中
INSTALLED_APPS = [
    ...,
    'rest_framework',
    ...,
]
# urls.py  中
from django.conf.urls import include

urlpatterns = [
    ...,
    # 调试api的时候登录url
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    ...,
]
```



在urls引入文档

```python
# urls.py

from rest_framework.documentation import include_docs_urls


# 文档路由 --- 一定不可以携带终止$符号  title  可以自定义
url(r'^docs/', include_docs_urls(title='document')),
```



实现第一个api

```python
# views.py

from django.shortcuts import render
from goods.models import Goods

########rest_framework########
from django.http import Http404
from rest_framework.views import APIView  # 这个view其实继承django的View
from rest_framework.response import Response
from rest_framework import status
from goods.serializer import GoodsSerializer


##############################

# Create your views here.

class GoodsListView(APIView):
    """
    例出所有的good或者创建一个good
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()
        # 需要自定义GoodsSerializer,类似于form对象
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)
```

同目录下的Serializer脚本

```python
# serializer.py

from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    # 映射Goods下的字段 类似 django form的功能
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0, )
    # 当然,还可以添加其他Goods中有的字段
```

路由定义

```python
# urls.py

from goods.views import GoodsListView

# 商品列表
url(r'^goods/$', GoodsListView.as_view(),name='goods-list'),
```

访问路由

如果遇到 error  `_str__ returned non-string (type NoneType)`

十有八九是users的model中的UserProfile 的 `__str__`方法返回的name为空,可以设置成为返回username  或者 进入xadmin后台页面,退出登录



rest framework 会自动补全 Filed 以及 image字段,是根据settings中的`MEDIA_ROOT`配置补全的

它会自动检索settings中的`MEDIA_ROOT`变量,将其用来补全

简单在goods 的 app 中 实现的方法

+ views.py中使用APIView类
+ serializer.py脚本中使用serializer.ModelSerializer类

##### 使用APIView实现

```python
# goods/views.py

from django.shortcuts import render
from goods.models import Goods

########rest_framework########
from django.http import Http404
from rest_framework.views import APIView  # 这个view其实继承django的View
from rest_framework.response import Response
from rest_framework import status
from goods.serializer import GoodsSerializer


##############################

# Create your views here.

class GoodsListView(APIView):
    """
    例出所有的good或者创建一个good
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()
        # 需要自定义GoodsSerializer,类似于form对象
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)

    # 这个post方法是用来接收前端post请求的时传递过来的数据
    def post(self, request, format=None):
        # 将数据传入到串行器中生成Serializer实例,为什么能够时候request.data直接获取数据呢?因为djangorestframework对request进行了二次封装
        serializer = GoodsSerializer(data=request.data)
        # 这里的数据验证是根据GoodsSerializer中定义的字段映射的属性进行验证
        if serializer.is_valid():
            # 如果验证成功,将前端传递过来的数据保存到串行器,这里的save会调用GoodsSerializer中定义的create方法
            serializer.save()
            # 数据创建成功之后要返回201  post 创建数据成功的状态码
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 如果数据验证不通过,返回错误信息,和400状态吗
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

##### serializers.Serializer 与 serializers.ModelSerializer
```python
# goods/serializer.py

from rest_framework import serializers
from goods.models import Goods, GoodsCategory


# 使用serializers.Serializer通过自定义字段来自定义 串行器
class GoodsSerializer_1(serializers.Serializer):
    # 映射Goods下的字段 类似 django form的功能
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0, )
    goods_front_image = serializers.ImageField()
    add_time = serializers.DateTimeField()

    # 创建对象的接口--对应的是GoodListView中的post方法
    def create(self, validated_data):
        # 此处的validated_data是将上面定义的字段映射从Serializer中获取数据后,打包成字典
        return Goods.objects.create(**validated_data)
        # 创建一个新的good

data
class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 既然Serializer和form是对应的,那么一定有一个ModelSerializer,来简化操作
class GoodsSerializer(serializers.ModelSerializer):
    # 简化操作后,直接指明映射的模型是哪一个,就可以自动形成映射关系
    category = GoodsCategorySerializer()  # 在这里实例化category对象来赋值给category,来替换仅仅能序列化为id的外键category

    # ,通过fields参数来控制哪些字段被映射
    class Meta:
        model = Goods
        # 所有字段都被序列化了出来,但是外键关联都序列化为相应的id,可以通过Serializer的嵌套实现将外键id找到对应的对象
        '''
        fields = (
        "category", "name", "goods_sn", "click_num", "sold_num", "fav_num", "goods_num", "market_price", "shop_price",
        "goods_brief", "goods_desc", "ship_free", "is_new", "is_hot", "goods_front_image", "add_time",)
        '''
        # 如果本身就是返回所有的值,可以使用__all__参数
        fields = "__all__"

```

##### mixins,generics.GenericAPIView 以及 generics.ListAPIView对其的简化
上面的serializer.py脚本中

通过使用 ModelSerializer类 来 简化 Serializer 类 使代码更加的简洁

那么在views.py中  也可以简化代码  使用  mixins 和 GenericAPIView 来实现此项功能

```python
# goods/views.py

from rest_framework import mixins
from rest_framework import generics

from goods.serializer import GoodsSerializer
from goods.models import Goods


class GoodsListView(mixins.ListModelMixin,
                    # mixins.CreateModelMixin, # 如果有post请求的创建方法,添加这个继承
                    generics.GenericAPIView,
                    ):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
	# 实现了将APIView中的get方法和mixins.ListModelMixin,中的list方法绑定
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


```

再次简化,简化到不用在手写get方法

```python
# goods/views.py
# 	其实ListAPIView封装了get方法,直接继承generics中的ListAPIView简化代码

# 继承generics.ListAPIView
class GoodsListView(generics.ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
# 将上面的5行代码缩减到三行

```

##### 简单快速的实现分页

通过更改配置文件实现对restframework的分页

在res_framework源码中找到settings.py脚本,通过脚本中的`__inin__`中的default变量可以找到restframework的默认配置(其实就在这个脚本的最上面,死一个字典类型的数据)

当然我们不会直接在源码上更改,而是引入django的settings.py中进行配置将rest_framework的默认配置覆盖掉

关于分页的默认配置就在这个位置

```python
# Generic view behavior
    'DEFAULT_PAGINATION_CLASS': None, # 配置为 rest_framework.pagination.PageNumberPagination 其实就是pagination脚本下的一个类
    'DEFAULT_FILTER_BACKENDS': (),
        
     # Pagination
    'PAGE_SIZE': None, # 定义了每一个页面的大小
```

在django的settings文件中的配置

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,
}
```

##### 定制分页

定制分页代码书写的位置也是在views视图中

```python
# goods/views.py
#################
from rest_framework import generics
#################
from goods.serializer import GoodsSerializer
from goods.models import Goods
####################
from rest_framework.pagination import PageNumberPagination
##################





# 定制分页 StandarResultsSetPagination 标准结果设置分页
class GoodsSetPagination(PageNumberPagination):
    """
    通过这个设置,我们可以根据前台的page_size参数请求每一页有多少条数据 区间在 10-100
    通过参数p来定位当前的页面是第几页
    """
    page_size = 10
    # 参数的名字  page_size  p
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


# 继承generics.ListAPIView
class GoodsListView(generics.ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
```

通过视图中配置分页之后,setting配置文件中的关于分页的配置可以被注释掉了,已经不需要那种简单的配置,而是调用views脚本中的定制分页配置规则

##### 通过viewset配合router将view再次打包减少代码

```python
# goods/views.py
############
from rest_framework import mixins
from rest_framework import viewsets
#################
from goods.serializer import GoodsSerializer
from goods.models import Goods
####################
from rest_framework.pagination import PageNumberPagination
##################


# 继承generics.ListAPIView
class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    GenericViewSet继承 GenericAPIView 以及 ViewSetMixin
    而GenericAPIView中没有定义get post等方法,所以使用GenericViewSet的时候需要自己定义get post等等的方法  只不过这个配置是在urls重构的时候配置的
    所以我们还要继承mixins.ListModelMixin,来完成定义get的方法
    而且需要注意的是  使用 viewset 需要对urls.py重构
    APIView提供get post等方法  mixins提供 list create等行为 两者互相绑定才能实现请求对应动作  在重构urls的时候配置
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
```

```python
# urls.py 部分

from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from DjangoVue.settings import MEDIA_ROOT
from django.views.static import serve
# 引入自定义的viewset(将以前的view改写的)-------------重构部分
from goods.views import GoodsListViewSet

# 引入文档
from rest_framework.documentation import include_docs_urls

# 配置动作---重构部分
goods_list = GoodsListViewSet.as_view({
    'get': 'list',  # 将get请求绑定到list 方法之上 也就是 apiview中的get请求绑定到mixin的list方法上面
})

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 开始配置路由
    # 文档路由 --- 一定不可以携带终止$符号
    url(r'^docs/', include_docs_urls(title='b')),
    # 商品列表
    url(r'^goods/$', goods_list, name='goods-list'),# 配置viewset路由--重构部分
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
```

以上操作基本实现了viewset的使用,这样做的好处是返回的数据`previous`变量将被补齐,----上一个数据的网址

-----

viewset是配合router使用的,为什么要结合router?

因为当我们的接口多了的时候,那么urls.py中关于 请求方式和操作行为绑定的配置也会越来越多,整个urls.py文件就会边的非常的庞大冗杂,所以使用router集中对绑定进行配置,降低整个urls.py文件的复杂程度

```python
# urls.py  使用router对路由重构


from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from DjangoVue.settings import MEDIA_ROOT
from django.views.static import serve
# viewset
from goods.views import GoodsListViewSet
#############-------router配置--------##############
# router
from rest_framework.routers import DefaultRouter
# 实例化router并对router配置
router = DefaultRouter()
# 将goods对应的viewset注册入router的urls中,使router分配接口路由
router.register(r'goods', GoodsListViewSet)

# 以后只要将接口的路由和访问数据的viewset注册入router就可以了,下面的 urlpatterns 就不用在多余的配置了

##################---------#############################
# 引入文档
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 开始配置路由
    # 文档路由 --- 一定不可以携带终止$符号
    url(r'^docs/', include_docs_urls(title='b')),
    # 商品列表
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

```

##### 如何选择viewset?

viewset是有分级的,理清分级才可以明确选择使用那个viewset

1. `GenericViewSet`最高级 [viewset]                      ----------django-rest-framework
   1. 继承了GenericAPIView[APIView]                 ----------django-rest-framework
      1. 继承了 APIView[View]                            ----------django-rest-framework
         1. 继承了 View                                     ----------django



1. Mixins
   + CreateModelMixin
   + ListModelMixin
   + UpdateModelMixin
   + DestoryModelMixin
   + RetrieveModelMixin

使用viewset的结果是本身应该在views.py文件中对APIView中的请求方式和Mixin中的行为进行绑定,想在挪到urls.py文件中通过router的注册实现请求方式和行为之间的绑定



viewset源码中主要重写了as_view的方法,使as_view方法中可以配置请求和行为之间的绑定

增加了initialize_request方法,可以让我们来对请求绑定自定义action

同样,在viewset模块中也有已经和Mixin组合后写好的的封装viewset  ReadOnlyViewSet  或者 ModelViewSet

可以通过自己的需求选择使用哪viewset,**注意**:虽然源码中已经组合,但是仅仅是继承上的组合,也就是说在Views.py文件中自定义的viewset可以少写一个或者两个继承,并没有在内部将请求方式和行为进行绑定,我们还是需要在urls.py的router中进行手动注册

##### djang-rest-framework 对 django自带request和response做了什么封装

---

**request**

对django中的HttpRequest进行了二次封装

`request.data`  将 django中的`request.POST` 或者是 `request.FILES` 的数据放到 drf 的 `request.data`里面

+ 它包括files或者non-files的内容
+ 解析了不仅仅是POST请求,还包括PUT和PATCH

?后面的参数会解析到`request.query-params`中

`.parsers`前台用户向后台发送数据的数据类型,框架不仅仅能解析JsonParser还可以解析FormParser,MultiPartParser或者FileUploadParser

---

**response**

Arugements:

+ data  返回的数据
+ status Http状态
+ template_name  当返回html的时候,指明渲染的模板是什么
+ headers  返回头
+ content_type  返回的数据类型

##### drf 中的过滤操作

-------

```python
# goods/views.py
# 在视图中定义的viewset中重写get_queryset(self)方法,并且不再使用queryset=Goods.objects.all()属性
# 注意 如果报错 basename.....那是因为路由注册的时候没有命名,router.register(r'goods', GoodsListViewSet, basename='goods-list')

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsSetPagination
    # 自定义返回数据的过滤方式,有了这个之后
    # queryset = Goods.objects.all() 这
    # 个指明queryset的属性就不需要了
    def get_queryset(self):
        return Goods.objects.filter(shop_price__gt=100)
```

上面的方法,证明可以通过 `get_queryset(self)`这个方法来对数据执行,过滤,那么意味着可以在这里添加更加高级的业务逻辑,来执行更高级的过滤效果:

**通过前台传递参数来控制过滤**

```python
# goods/views.py

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsSerializer
    pagination_class = GoodsSetPagination
    def get_queryset(self):
        querset = Goods.objects.all()  # 注意all并不是真的将所有数据取了粗来,不必担心数据太大的问题
        # 现在通过前台输入price_min参数来控制过滤
        price_min = self.request.query_params.get('price_min', 0)
        if price_min:
            querset = querset.filter(shop_price__gt=int(price_min))
        return querset
```

这样的话,前端页面发送请求的时候加上`price_min=xxx`参数,就能筛选想要的结果

发现一个问题:

​	当我们的需要过滤的字段过多的时候,就会有大量的判断,所以django-filter模块封装好了过滤的操作

使用方法相当简洁

##### 使用djiang-filter对结果过滤

---

+ DjangoFilterBacked 精确到某一个字段过滤
+ SearchFilter搜索过滤
+ OrderingFilter排序过滤

`pip install django-filter`

首先需要将这个模块假如到django 配置文件的app中

INSTALLED_APP = [`'django_filters',`]

```python
# goods/views.py

class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
    # 过滤条件
    filter_backends = (DjangoFilterBackend,)
    # 配置可用于过滤的字段
    filter_fields = ('name', 'shop_price',)

```

这样前端页面就可以通过name  shop_price两个字段传递参数进行过滤了

**注意:**过滤和搜索不是一个概念,上面的过滤是精确过滤,只有完全匹配到的才能返回结构,否则返回null

所以上面的过滤不能达到我们模糊搜索,以及价格区间过滤的效果,还需要改进

可以查看`django-filter`的官网`https://django-filter.readthedocs.io/en/master/`

这个文档中有详细的关于这个模块的解释



为了不加大views.py脚本的内容复杂度,我们单独在当前的app下创建一个`filters.py`脚本用来定制我们的过滤操作

```python
# 模糊过滤和范围过滤
# goods/filters.py

import django_filters
from goods.models import Goods


# 需要去view视图的viewset中定义filter_class = 这个类  而且 filter_backends 还是使用 DjangoFilterBackend
class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
        自定义商品过滤规则类
    """
    # 对于数字类型的过滤规则 参数 field_name:所操作的字段名  lookup_expr : 查询方式 gte 大于等于
    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # contains 是模糊查询 i开头是忽略大小写  如果不指定lookup_expr参数,那么就必须完全匹配
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Goods
        # 这里定义了变量之后,viewset中的filter_fields就可以干掉了
        fields = ['price_max', 'price_min', 'name']
```

```python
# goods/views.py
from goods.filters import GoodsFilter
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
    # 过滤条件
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter
```

自定义规则过滤就按照上面的方式即可

前端页面的参数`?price_max=200&price_min=100&name=牛肉` 在价格区间100-200，name中包含‘牛肉’的范围内过滤



----

模糊搜索  **注意**  搜索  search 而不是 过滤

这里使用的是django_restframework中的filter,而不再是django-filter中的filter

```python
# goods/views.py
from rest_framework import filters
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsSetPagination
    # 过滤条件,模糊查询
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = GoodsFilter
    # 注意这里定义模糊搜索的字段是model中定义的字段,前端发送的变量名
    """
    这里写字段名的时候可以增加特殊符号产生特殊效果
    ^name  意味着 从name中模糊搜索必须从头匹配
    =name                         精确过滤
    @name                         全文搜索
    $name                         正则搜索
    """
    search_fields = ('name', 'goods_desc', 'goods_brief')
```

前端页面对字段查询的参数 `?search=牛肉`将会在上面`search_fields`参数中查询，一般来说只要有一个匹配就可以被返回，除了设置了特殊符号



---

`OrderingFilter`排序

```python
# goods/views.py
# 使用django-restframework的filter配置可排序字段

from rest_framework import filters
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
    # 过滤条件,模糊查询,配置排序字段
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    # 注意这里定义模糊搜索的字段是model中定义的字段,前端发送的变量名
    search_fields = ('name', 'goods_desc', 'goods_brief')
    # 设置可排序字段
    ordering_fields = ('sold_num', 'add_time',)
```

前端叶页面请求排序的参数`?ordering=-sold_num` 负号是倒序的意思，不添加负号就是正序



---

##### 前后端分离项目的跨域问题

Vue项目是按照组件的形式编写的,所以,如果想要找到 查询到的数据是如何映射到Vue中的,就要找到相关的主键

src目录是Vue项目的源码

src/views目录是所有组件存放的目录,我们可以从中找到head目录,那个目录中的head.vue就是head组件

```javascript
      getMenu() {//获取菜单
        getCategory({
          params: {}
        }).then((response) => {
          console.log(response)
          this.allMenuLabel = response.data
        })
          .catch(function (error) {
            console.log(error);
          });
      },
```

`getMenu()`函数中的`getCategory()`函数就是当前组件获取商品分类的函数,通过查找这个函数的定义位置,可以找到这个函数是如何请求到商品的分类信息的

```javascript
//获取商品类别信息
export const getCategory = params => {
  if('id' in params){
    return axios.get(`${host}/categorys/`+params.id+'/');
  }
  else {
    return axios.get(`${host}/categorys/`, params);
  }
};
```

追寻到以上信息,发现跟组件交互的接口全部在api目录下的api.js文件中

在接口文件的顶部定义了一个host,全局都在用追个host

`let host = 'http://shop.projectsedu.com';`如果我们直接将这个host改为`127.0.0.1:8000`那么就会出现跨域问题

数据获取不到,控制台报错 net::error_connection_refused 这是因为我们没有开启后台服务

更改之后,发现报错,报跨域,所以需要通过服务器设置来解决跨域问题

github上搜索`django-cors-headers`这里有答案

首先安装`pip install django-cors-headers`

**安装完成之后:**

首先将`corsheaders`配置到django的app中

将以下中间件配置到django中间件中

​	 `'corsheaders.middleware.CorsMiddleware'`尽量放在CSRF中间件之前,或者直接将其放在首位

在settings.py配置文件中配置

`CORS_ORIGIN_ALLOW_ALL=True`

重启后台服务,这样跨域问题将会得到解决

发现数据可以填充到页面中了,那么数据是如何填充到页面中去的呢?

`getCategory`函数通过api接口请求数据,函数的结果赋值给`this.allMenuLabel`

```html
<li class="first" v-for="(item,index) in allMenuLabel" @mouseover="overChildrenmenu(index)" @mouseout="outChildrenmenu(index)"> <h3 style="background:url(../images/1449088788518670880.png) 20px center no-repeat;"> 
    <router-link :to="'/app/home/list/'+item.id">
     {{item.name}}
    </router-link> </h3> 
   <div class="J_subCata" id="J_subCata" v-show="showChildrenMenu ===index" style=" left: 215px; top: 0px;"> 
    <div class="J_subView"> 
     <div v-for="list in item.sub_cat"> 
      <dl> 
       <dt> 
        <router-link :to="'/app/home/list/'+list.id">
         {{list.name}}
        </router-link> 
       </dt> 
       <dd> 
        <router-link v-for="childrenList in list.sub_cat" :key="childrenList.id" :to="'/app/home/list/'+childrenList.id">
         {{childrenList.name}} 
        </router-link> 
       </dd> 
      </dl> 
      <div class="clear"></div> 
     </div> 
    </div> 
   </div>
</li>
```

发现返回的`allMenuLabel`被绑定到上述的列表中了

---

##### 登录注册问题

由于使用django-restframework就意味着我们的项目是跨域的跨站点的项目,所以无法使用django的csrf-token进行认证

因此restframework提供了自己的认证方式

+ BsciAuthentication
+ SessionAuthentication
+ TokenAuthentication

使用方式:

+ 配置url

```python
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns += [url(r'^api-token-auth/', obtain_auth_token),]

```

+ 配置文件

```python
# 注册app
'rest_framework.authtoken'
# 配置文件添加
# django_rest_framework的配置
REST_FRAMEWORK = {
    # 配置进行登录注册认证的方式  基于BasicAuthentication和SessionAuthentication
    # 类似于django中间件,但是只在登录的时候验证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}
```

+ 执行迁移文件的生成以及提交迁移

结果:会在数据库中生成`authtoken_token`表

字段:

+ key
+ token
+ id ---- 外键指向user

当用户发出post登录请求的时候会生成一个token<如果当前用户没token>

token的使用是放在httpheader中的  会在header中存放`Authorization: Token xxxxxxxxxxxxxxxxxxxx`格式,会伴随着以后的请求,在后台进行验证

当请求头中携带 这个参数[正确]的时候,后台会根据toke取出相应的用户放在`request`上下文中,然后继续时候其他的验证方式验证用户

后台可以通过request.auth将用户请求中的toke取出来

request.data将用户请求的时候携带的参数取出来[get参数,post参数,files参数]

token认证失败会返错误信息`{'detail':'认证令牌无效。'}`

**吭**:token设置之后,如果携带错误的token去访问公共数据,那么会出现认证失败的情况`{'detail':'认证令牌无效。'}`,或者token过期了,由于前后端分离,前端页面的请求一般全局配置token,所以我们要通过其他途经,将公共信息的token认证解除

**方式:**单独对某些个ViewSet配置token认证----将全局的token从配置文件中移除,在views.py中导入`TokenAuthentication`通过在定义的ViewSet中配置`authentication_classes=(TokenAuthentication,)`**注意元组**,来单独对某个viewset配置token认证

---

##### JWT认证(json,web,token)

为什么?

http请求,没有状态,当一个用户通过一个请求去执行登录后,下一个请求 后台 不知道用户的登录状态,无法对用户是否登录进行判断,就需要再次验证,一次一次的去验证,也就是说需要用户一次一次的登录或者储存用户的username和password后台给登录,这样对用户来说是不友好的,对服务来说,重复的登录将对服务造成很大的负担,以及储存用户的username和password会出现用户资料的安全问题,所以需要一个方式既安全又方便的去保存用户的的登录状态



传统token存放在cookies中,可以被JavaScript截获[xss攻击]可以通过设置过期时间来降低损失

也可以通过设置cookies的时候设置httpOnly以及secure选项来禁止cookies被js读取而且只能通过HTTPS传输,可以避免一些xss攻击,但是避免不了xsrf攻击

还有就是token储存在数据库中,请求携带token,后台通过token表查找用户ID,再通过用户ID找用户,之后再进行用户名和密码的匹配,多次访问数据库,无形的增加了后台服务器的压力

需求:不将token进行储存,如果toke的生成是有某个固定的规律,比如通过对称加密算法来将用户ID加密形成token,那么服务端只需要解码token就可以获得用户的真实ID,**过程:**`服务器根据用户id加密形成token传给客户端,客户端请求携带token到服务端,服务端解码token找到用户id<对称加密加密解密是同一个秘钥>都在服务端进行`

**JWT**:是一开放个标准,定义了一种简洁,自包含的用于通信双方使用json对象传递安全信息的方法,可以使用HMAC算法或者RSA的公钥秘钥对进行签名,具备两个特点:

+ 简洁  可以通过get,post请求参数或者httpheader发送数据,数据量小,传输速度快
+ 自包含  载体中包含用户所有的登录信息,而不再是部分,不需要回数据库表查询,效率提高

JWT**的组成部分**

+ header  [使用base64对当前编码]
  +  typ: token类型
  +  alg: 采用的加密算法
+ payload 负载 存放用户的信息 可以存放用户的id等等信息 [使用base64编码]
  + iss  签发者
  + exp  过期时间
  + sub  面向的用户
  + and  接收方
  + iat  签发时间
  + ...查看JWT规范
+ signature  签名 
  + 它需要使用编码后的header,payload以及我们提供的一个秘钥,然后使用header中指明的算法(HS256)进行签名,作用是保证JWT没有被篡改

结果可能是这个样子

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`.`eyJpZCI6IjU3ZmVmMTY0ZTU0YWY2NGZmYzUzZGJkNSIsInhzcmYiOiI0ZWE1YzUwOGE2NTY2ZTc2MjQwNTQzZjhmZWIwNmZkNDU3Nzc3YmUzOTU0OWM0MDE2NDM2YWZkYTY1ZDIzMzBlIiwiaWF0IjoxNDc2NDI3OTMzfQ`.`PA3QjeyZSUh7H0GfE0vJaKW4LjKJuC3dVLQiY4hii8s`

分别是:

+ header   :　`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`
+ payload  : `eyJpZCI6IjU3ZmVmMTY0ZTU0YWY2NGZmYzUzZGJkNSIsInhzcmYiOiI0ZWE1YzUwOGE2NTY2ZTc2MjQwNTQzZjhmZWIwNmZkNDU3Nzc3YmUzOTU0OWM0MDE2NDM2YWZkYTY1ZDIzMzBlIiwiaWF0IjoxNDc2NDI3OTMzfQ`
+ signature: `PA3QjeyZSUh7H0GfE0vJaKW4LjKJuC3dVLQiY4hii8s`

过程 header[base46],payload[base64]使用header提供的算法对这两个数据签名生成signature,最后通过秘钥解密

整个过程不会被保存,不会创建表,所以效率提高,数据安全



对比传统session_ID的模式,jwt储存更多信息,储存本地化到客户端,减少了服务器压力储存压力,增强了计算压力(不算问题)

场景:多子域名   --- 多后台服务器  如果实现在不同的子域名服务器上实现同步登录状态保存,那么使用session模式就需要在这些服务器中同步session,也就是说将session储存在同一个数据库上其他服务器都从这个数据库上获取session验证

当时JWt不会出现这种问题,因为状态信息储存在客户端,客户端将状态信息发送到服务器,不管是哪个服务器,都只需要对数据进行算法上的运算,最终对比客户端传过来的数据即可



---

##### 使用django-restframework-jwt

github链接:`https://github.com/GetBlimp/django-rest-framework-jwt`

配置:

首先直接将`'rest_framework_jwt.authentication.JSONWebTokenAuthentication',`添加到rest-framework的登录验证中

路由:

`from rest_framework_jwt.views import obtain_jwt_token`

配置url `url(r'^api-token-auth/', obtain_jwt_token),`

使用浏览器模拟发送登录请求的结果是:`{'token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTQ0NjgxNDUzLCJlbWFpbCI6IjFAMS5jb20ifQ.LJfi6T4ehVgSMrMUAFA2EFOfW3I9NQo2fmzfqBh5IrI'}`

使用base64解码:

`eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9`----->   header:`{"typ":"JWT","alg":"HS256"}`

`eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTQ0NjgxNDUzLCJlbWFpbCI6IjFAMS5jb20ifQ`---->payload:`{"user_id":1,"username":"admin","exp":1544681453,"email":"1@1.com"}`

看到payload中储存了**用户的id,用户名,失效时间,用户的电子邮箱**

`LJfi6T4ehVgSMrMUAFA2EFOfW3I9NQo2fmzfqBh5IrI`--->signature  无法使用base64解码

上面的token将被存在header中,贯穿整个请求相应过程,在header储存的方式和传统rest-framework自带的token有些不同

`Authorization:JWT xxxxxxxxxxxxxxxxxxxxxxx`  就是将Token换成了JWT





