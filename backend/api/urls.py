from django.urls import path, re_path

from . import views

# 接口地址按实际情况修改
urlpatterns = [
    # 用户信息
    path('login/', views.login),  # 用户登录
    path('logout/', views.logout),  # 注销
    path('register/', views.register),  # 用户注册
    path("getUserInfo/", views.get_user_info),  # 获取用户信息
    path('userInfo/update/', views.user_info_update),  # 更新用户信息
    path('userInfo/updatePassword/', views.user_pwd_update),  # 更新用户密码
    path('setAvatar/', views.set_avatar),  # 上传用户头像

    # 数据集社区信息
    path("community/getInfo/", views.get_community_info),  # 获取数据集信息
    path("community/deleteOne/", views.delete_community_dataset),  # 删除一个社区数据集
    path("community/deleteAll/",
         views.delete_all_community_dataset),  # 清空社区数据集
    path("community/update/", views.update_community_dataset),  # 更新一个社区数据集
    path("community/uploadDataset/",
         views.upload_dataset_zip),  # 原始未标注数据集压缩包上传

    # 个人数据集信息
    path("myDataset/getInfo/", views.get_user_dataset_info),  # 获取个人数据集信息
    path("myDataset/add/", views.add_user_dataset),  # 增加一条用户数据集
    path("myDataset/deleteOne/", views.delete_user_dataset),  # 删除一个数据集
    path("myDataset/deleteAll/", views.delete_all_user_dataset),  # 清空数据集
    path("myDataset/update/", views.update_user_dataset),  # 更新一个数据集
    path("myDataset/updateStatus/",
         views.update_user_dataset_status),  # 更新一个数据集状态

    # 标注图像
    path('annotateImage/getImageList/',
         views.get_annotate_image_list),  # 获取图片集信息
    path('annotateImage/getInfo/',
         views.get_annotate_image_info),  # 获取当前要标注的图片
    path('annotateImage/update/', views.update_annotate_image_info),  # 更新标注信息
    path('annotateImage/export/', views.export_annotated_dataset),  # 导出图像数据集

    # 标签管理
    path('labels/add/', views.add_labels),  # 添加标签
    path('labels/get/', views.get_labels),  # 获取标签
    path('labels/update/', views.update_labels),  #更新标签
    path('labels/updateColor/', views.update_label_color),  #更新标签颜色
    path('labels/delete/', views.delete_label),  #更新标签颜色

    # 成员管理
    path('addMember/', views.add_member),  # 添加成员
]
