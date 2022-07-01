from django.db import models


class UserInfo(models.Model):
    """ 存储用户的个人信息 """
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=50,
                             unique=True,
                             null=False,
                             default='')
    avatar = models.ImageField(upload_to='avatar',
                               max_length=255,
                               blank=True,
                               null=True)
    roles = models.CharField(max_length=30, default="管理员")


class Labels(models.Model):
    """ 用户自定义的标签 """
    text = models.CharField(max_length=30, null=True)  # 标签名
    color = models.CharField(
        max_length=40,
        null=True,
    )
    shortcut = models.CharField(max_length=5, null=True)
    user = models.ForeignKey(UserInfo, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class Dataset(models.Model):
    """ 存储包含若干张原始图片的数据集 """
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=100, default="无")
    status = models.CharField(max_length=20, default="无人认领")
    num = models.IntegerField(null=False, default=0)  # 图片数量
    publisher = models.ForeignKey(UserInfo,
                                  null=False,
                                  on_delete=models.PROTECT)  # 发布者
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = "pub_date"

    def __str__(self):
        return self.name


class Image(models.Model):
    """ 存储单张图片信息 """
    name = models.CharField(max_length=50, null=False)
    dataset = models.ForeignKey(Dataset, null=False,
                                on_delete=models.CASCADE)  # 原始数据集
    image = models.ImageField(null=False, max_length=100,
                              upload_to="dataset")  # 最大100K

    def __str__(self):
        return self.name


class AnnotatedSet(models.Model):
    """ 对于某个图片集的标注数据集，领取原始数据集的每个用户都会有一个不同的标注集 """
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, default="无")
    status = models.CharField(max_length=20, default="未标注")
    num = models.IntegerField(null=False, default=0)  # 图片数量
    dataset = models.ForeignKey(Dataset, null=False,
                                on_delete=models.PROTECT)  # 原始数据集ID
    owner = models.ForeignKey(UserInfo, null=False, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pub_date']
        get_latest_by = "pub_date"


class LabeledImage(models.Model):
    """ 对于单张图片的标注信息表 """
    annotatedset = models.ForeignKey(AnnotatedSet,
                                     null=False,
                                     on_delete=models.CASCADE)  # 标注数据集
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    labelinfo = models.JSONField(null=False, default=dict)  # 标注文件用JSON格式进行存储


class AnnotateText(models.Model):
    '''
    用户上传的文本
    使用用户的id作为外键 主要作用就是查找该用户所有的标注文本, 以及在其注销账号时, 删除所有数据时用
    其他的情况, 如更改, 删除每一条数据都可以直接使用 id
    '''
    text = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, default="无")
    # text = models.TextField(max_length=1000) mysql 不支持Textfield
    # description = models.TextField(max_length=1000, default="无")
    status = models.CharField(max_length=20, default="未标注")
    user = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


# 标注数据
class AnnotateData(models.Model):
    # annotate_data = models.
    pass
