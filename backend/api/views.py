import io
import json
import os
import zipfile
import tempfile
import shutil
import time
from django.http.response import FileResponse

import requests

from django.contrib.auth.hashers import check_password, make_password
from django.core import signing
from django.utils.encoding import escape_uri_path

from .models import *
from .utils.tools import *
'''
目前是把所有的接口都放在这
但是为了方便管理和维护，以及更好的逻辑
可以多弄几个app 使每个app的功能更加细化
当然要记得同时更改前端请求的地址
'''
""" -------------------------------------------------------------- """
""" -------------------------用户信息操作-------------------------- """
""" -------------------------------------------------------------- """


# 登录 登录后会在浏览器存储cookie,并且有时长
def login(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = UserInfo.objects.filter(username=username).first()
    if user and check_password(password, user.password):
        token = signing.dumps({"username": username, "id": user.id})
        return ok({"token": token})
    else:
        return error("用户名或密码错误，请仔细检查后重新输入")


# 用户注册
def register(request):
    data = json.loads(request.body)
    username = data['username']
    email = data['email']
    password = data['password']
    if UserInfo.objects.filter(username=username):
        return error("这个昵称太受欢迎了，请换另一个昵称")
    password = make_password(password)  # 密码加密后再存储
    user = UserInfo(username=username, email=email, password=password)
    user.save()
    token = signing.dumps({"username": username, "id": user.id})
    return ok({"token": token})


# 获取用户信息
def get_user_info(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    userId = token['id']
    user = UserInfo.objects.filter(id=userId).first()
    if not user:
        return error("用户信息不存在")
    # 在这里顺便查询数据库，获取用户自定义的标注标签，标注文本，成员信息 并放入响应数据中
    userAvatar = str(request.build_absolute_uri('/')) + "media/avatar/" + str(
        user.avatar) if user.avatar else None
    return ok({
        "name": user.username,
        "email": user.email,
        "roles": [user.roles],  # 用户角色，如果有用户管理就需要
        "avatar": userAvatar,  # 头像地址
    })


# 注销 用户注销后，前端会删除浏览器的cookie,同时会请求这个接口
# 如果有其他业务逻辑的话，可以在这里进行操作，没有的话就不用管他了
def logout(request):
    return ok({})


# 设置用户头像
def set_avatar(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    username = token['username']
    # 是否需要限制头像大小
    avatar = request.FILES.get("avatar")
    # 更新头像前应该把旧头像删除
    # 为了防止头像被覆盖，即不同用户上传的头像名称相同，应考虑存储图片时图片的命名
    UserInfo.objects.filter(username=username).update(avatar=avatar)
    with open(os.path.join(os.getcwd(), 'upload_file/avatar', avatar.name),
              'wb') as fw:
        fw.write(avatar.read())
    # 返回头像的链接地址
    return ok({
        "avatar":
        str(request.build_absolute_uri('/')) + "media/avatar/" + avatar.name
    })


# 更新用户信息
def user_info_update(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    data = json.loads(request.body)
    # 这里只更新用户名，想要更新其他的可以添加
    name = data['name']
    userId = token['id']
    if UserInfo.objects.filter(username=name):
        return error("这个昵称太受欢迎了，请换另一个")
    UserInfo.objects.filter(id=userId).update(username=name)
    token = signing.dumps({"username": name, "id": userId})
    return ok({"token": token})


# 修改密码
def user_pwd_update(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    username = token['username']
    data = json.loads(request.body)
    oldPassword = data['oldPassword']
    newPassword = data['newPassword']
    user = UserInfo.objects.get(username=username)
    if not check_password(oldPassword, user.password):
        return error("输入旧密码不正确，修改密码失败")
    UserInfo.objects.filter(username=username).update(
        password=make_password(newPassword))

    return ok({})


""" -------------------------------------------------------------- """
""" -------------------------社区数据操作-------------------------- """
""" -------------------------------------------------------------- """


# 获取数据集社区信息
def get_community_info(request):
    dataset_list = []
    for dataset in Dataset.objects.all():
        dataset_list.append({
            "id": dataset.id,
            "name": dataset.name,
            "num": dataset.num,
            "publisher": dataset.publisher.username,
            "description": dataset.description,
            "status": dataset.status
        })
    return ok({"dataset_list": dataset_list})


# 删除一个社区数据集
def delete_community_dataset(request):
    id = json.loads(request.body)['id']
    target = Dataset.objects.filter(id=id).first()
    if target:
        if target.status == '无人认领':
            target.delete()
            return ok({})
        else:
            return error("该数据集有人认领，不可以删除")
    return error("该数据集不存在")


# 清空社区数据集
def delete_all_community_dataset(request):
    # canDeleteAll = True
    for target in Dataset.objects.all():
        if target:
            # if target.status == '无人认领':
            target.delete()
            # else:
            # canDeleteAll = False
        else:
            return error("有不存在的数据集")
    # if canDeleteAll == False:
    # return error("有人认领的数据集不可以删除")
    return ok({})


# 更新一个社区数据集
def update_community_dataset(request):
    dataset_info = json.loads(request.body)['datasetInfo']
    Dataset.objects.filter(id=dataset_info['id']).update(
        name=dataset_info['name'], description=dataset_info['description'])
    return ok({})


# 增加一个数据集，原始数据集压缩包上传
def upload_dataset_zip(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    zip_data = request.FILES.get("dataset_zip")

    # 将接受到的zip文件存放到临时文件夹中，保证临时文件夹中没有其他.zip
    if os.path.exists(os.path.join(os.getcwd(), 'tmpfile')):
        shutil.rmtree(os.path.join(os.getcwd(), 'tmpfile'))
    zip_file = zipfile.ZipFile(zip_data)
    zip_file.extractall(path=(os.path.join(os.getcwd(), 'tmpfile')))  # 解压
    zip_file.close()
    # 将上传的图片导入到数据存储文件夹下，返回图片数量和数据集图片存储路径(相对于os.getcwd())
    image_num, image_dir = save_image_to_dir()
    if image_num == 0:
        return error("没有上传有效zip文件")

    zip_file_name = str(zip_data.name)[:str(zip_data.name).rfind('.')]
    Dataset(name=zip_file_name,
            num=image_num,
            publisher=UserInfo.objects.get(id=user_id)).save()  # 添加数据集

    # 添加数据集文件夹下的所有图片
    image_name_list = os.listdir(
        os.path.join(os.getcwd(), 'upload_file', 'dataset', image_dir))
    new_dataset = Dataset.objects.latest()
    for image_name in image_name_list:
        Image(name=image_name,
              dataset=Dataset.objects.get(id=new_dataset.id),
              image=os.path.join(image_dir, image_name)).save()
    return ok({
        'new_dataset_info': {
            "id": new_dataset.id,
            "name": new_dataset.name,
            "num": new_dataset.num,
            "publisher": new_dataset.publisher.username,
            "description": new_dataset.description,
            "status": new_dataset.status
        }
    })


""" -------------------------------------------------------------- """
""" ------------------------用户数据集操作------------------------- """
""" -------------------------------------------------------------- """


# 获取用户标注数据集信息
def get_user_dataset_info(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    dataset_list = []
    for user_dataset in AnnotatedSet.objects.filter(owner=user_id):
        dataset_list.append({
            "id": user_dataset.id,
            "name": user_dataset.name,
            "num": user_dataset.num,
            "description": user_dataset.description,
            "dataset_id": user_dataset.dataset.id,
            "status": user_dataset.status
        })
    return ok({"dataset_list": dataset_list})


# 增加用户标注数据集
def add_user_dataset(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    dataset_info = json.loads(request.body)['datasetInfo']
    AnnotatedSet(name=dataset_info['name'],
                 description=dataset_info['description'],
                 num=dataset_info['num'],
                 dataset=Dataset.objects.get(id=dataset_info['id']),
                 owner=UserInfo.objects.get(id=user_id)).save()
    new_dataset = AnnotatedSet.objects.latest()
    # 添加与原始数据集对应的标签信息文件
    for image in Image.objects.filter(dataset=new_dataset.dataset):
        LabeledImage(annotatedset=new_dataset,
                     image=image,
                     labelinfo={
                         'label': {},
                         'rects': []
                     }).save()
    Dataset.objects.filter(id=dataset_info['id']).update(status='有人认领')
    return ok({})


# 删除一个用户标注数据集
def delete_user_dataset(request):
    id = json.loads(request.body)['id']
    target = AnnotatedSet.objects.filter(id=id).first()
    if target:
        target.delete()
        return ok({})
    return error("该数据集不存在")


# 清空用户标注数据集
def delete_all_user_dataset(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    for target in AnnotatedSet.objects.filter(owner=user_id):
        if target:
            target.delete()
        else:
            return error("有不存在的数据集")
    return ok({})


# 更新一个用户标注数据集
def update_user_dataset(request):
    dataset_info = json.loads(request.body)['datasetInfo']
    AnnotatedSet.objects.filter(id=dataset_info['id']).update(
        name=dataset_info['name'], description=dataset_info['description'])
    return ok({})


# 更新一个用户标注数据集状态
def update_user_dataset_status(request):
    status = json.loads(request.body)['status']
    id = json.loads(request.body)['id']
    AnnotatedSet.objects.filter(id=id).update(status=status)
    return ok({})


""" -------------------------------------------------------------- """
""" -------------------------图像标注操作-------------------------- """
""" -------------------------------------------------------------- """


# 获取标注数据集图片列表
def get_annotate_image_list(request):
    annotatedset_id = json.loads(request.body)['annotatedset_id']
    annotatedSet = AnnotatedSet.objects.get(id=annotatedset_id)
    image_list = []
    for image in Image.objects.filter(
            dataset_id=annotatedSet.dataset_id).all():
        image_list.append(image.id)
    # TODO: 恢复标注进度
    last_image_index = 0  # 上次标注的进度，在图片列表中的序号
    return ok({
        'name': annotatedSet.name,
        'image_list': image_list,
        'annotatedSet_status': annotatedSet.status,
        'last_image_index': last_image_index
    })


# 获取当前要标注的图片info
def get_annotate_image_info(request):
    annotatedset_id = json.loads(request.body)['annotatedset_id']
    image_id = json.loads(request.body)['image_id']
    imageObj = Image.objects.get(id=image_id)
    labeledImage = LabeledImage.objects.filter(
        image_id=image_id, annotatedset_id=annotatedset_id).first()
    image = str(request.build_absolute_uri('/')) + "media/dataset/" + str(
        imageObj.image).replace('\\', '/')
    image_size = cv2.imread(
        os.path.join(os.getcwd(), 'upload_file', 'dataset',
                     str(imageObj.image))).shape
    height, width = image_size[0], image_size[1]
    return ok({
        'labelinfo': labeledImage.labelinfo,
        'name': imageObj.name,
        'image': image,
        'width': width,
        'height': height
    })


# 更新标注信息
def update_annotate_image_info(request):
    annotatedset_id = json.loads(request.body)['annotatedset_id']
    image_id = json.loads(request.body)['image_id']
    label = json.loads(request.body)['label']
    rects = json.loads(request.body)['rects']
    LabeledImage.objects.filter(
        image_id=image_id,
        annotatedset_id=annotatedset_id).update(labelinfo={
            'label': label,
            'rects': rects
        })
    return ok({})


# 标注完成的数据集导出
def export_annotated_dataset(request):
    annotatedset_id = json.loads(request.body)['annotatedset_id']
    annotatedset_name = json.loads(request.body)['annotatedset_name']
    annotatedset_type = json.loads(request.body)['annotatedset_type']

    # 创建一个临时文件夹用来保存标注文件和图片
    temp = tempfile.TemporaryDirectory()
    temp_path = os.path.join(temp.name, 'temp')
    os.makedirs(temp_path)
    # 为所有图片创建一个对应名字的JSON文件，并移动到临时文件夹
    label_list = []
    for labeled_image in LabeledImage.objects.filter(
            annotatedset_id=annotatedset_id).all():
        labelinfo = labeled_image.labelinfo
        if labelinfo['label']['text'] not in label_list:
            label_list.append(labelinfo['label']['text'])
        imgObj = Image.objects.get(id=labeled_image.image_id)
        create_JSON_file(temp_path, str(imgObj.image), labelinfo)

    output_dir = os.path.join(temp.name, annotatedset_name)
    generate_export_dataset(dataset_type=annotatedset_type,
                            input_dir=temp_path,
                            output_dir=output_dir,
                            label_list=label_list)

    # 压缩打包为.zip文件
    annotatedset_zip = zipfile.ZipFile(output_dir + '.zip', 'w',
                                       zipfile.ZIP_DEFLATED)
    for path, dir_name, file_names in os.walk(output_dir):
        related_path = path.replace(output_dir, '')  # 相对路径
        for file_name in file_names:
            print(os.path.join(related_path, file_name))
            annotatedset_zip.write(os.path.join(path, file_name),
                                   os.path.join(related_path, file_name))
    annotatedset_zip.close()
    response = FileResponse(open(output_dir + '.zip', 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
        escape_uri_path(annotatedset_name))

    return response


""" -------------------------------------------------------------- """
""" -------------------------标签数据操作-------------------------- """
""" -------------------------------------------------------------- """


# 添加标注标签
def add_labels(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    label = json.loads(request.body)
    Labels(text=label['text'],
           color=label['color'],
           shortcut=label['shortcut'],
           user_id=user_id).save()
    # 返回所有的标签数据(因为删除标签需要标签id,新添加的标签只有加入数据库才有id,所以需要返回新的所有标签数据)
    # 如果有更好的方法也可以改
    data = Labels.objects.filter(user_id=user_id)
    labels = []
    for label in data:
        labels.append({
            'id': label.id,
            'text': label.text,
            'color': label.color,
            'shortcut': label.shortcut,
        })
    return ok({"labels": labels})


# 获取所有标签
def get_labels(request):
    token = signing.loads((request.META.get('HTTP_ANNOTATE_SYSTEM_TOKEN')))
    user_id = token['id']
    data = Labels.objects.filter(user_id=user_id)
    labels = []
    for label in data:
        labels.append({
            'id': label.id,
            'text': label.text,
            'color': label.color,
            'shortcut': label.shortcut,
        })
    return ok({"labels": labels})


# 更新标注标签
def update_labels(request):
    labelInfo = json.loads(request.body)
    Labels.objects.filter(id=labelInfo['id']).update(
        text=labelInfo['text'],
        color=labelInfo['color'],
        shortcut=labelInfo['shortcut'])
    return ok({})


# 更新标签颜色
def update_label_color(request):
    labelInfo = json.loads(request.body)
    Labels.objects.filter(id=labelInfo['id']).update(color=labelInfo['color'])
    return ok({})


# 删除标注标签
def delete_label(request):
    labelInfo = json.loads(request.body)
    Labels.objects.filter(id=labelInfo['id']).delete()
    return ok({})


""" -------------------------------------------------------------- """
""" -------------------------成员管理操作-------------------------- """
""" -------------------------------------------------------------- """


# 添加成员
def add_member(request):
    member = json.loads(request.body)
    print(member)
    user = UserInfo.objects.filter(username=member['name'])
    if not user.exists():
        return error("该用户不存在")
    return ok({})


# 删除成员
def delete_member(request):
    return ok({})


# 编辑成员信息
def edit_member_info(request):
    return ok({})
