import request from "@/utils/request";

/**
 * 获取标注数据集的图片列表信息
 */
export function getDatasetImageListApi(annotatedset_id) {
  return request({
    url: "api/annotateImage/getImageList/",
    method: "post",
    data: { annotatedset_id: annotatedset_id },
  });
}

/**
 * 获取当前图像和标注信息
 */
export function getAnnotateImageInfoApi(annotatedset_id, image_id) {
  return request({
    url: "api/annotateImage/getInfo/",
    method: "post",
    data: {
      annotatedset_id: annotatedset_id,
      image_id: image_id,
    },
  });
}

/**
 * 更新当前标注信息
 */
export function updateAnnotateImageInfoApi(
  annotatedset_id,
  image_id,
  cur_label,
  rects
) {
  return request({
    url: "api/annotateImage/update/",
    method: "post",
    data: {
      annotatedset_id: annotatedset_id,
      image_id: image_id,
      label: cur_label,
      rects: rects,
    },
  });
}

/**
 *  导出当前标注数据集
 */
export function exportAnnotateDatasetApi(
  annotatedset_id,
  annotatedset_name,
  annotatedset_type
) {
  return request({
    url: "api/annotateImage/export/",
    method: "POST",
    data: {
      annotatedset_id: annotatedset_id,
      annotatedset_name: annotatedset_name,
      annotatedset_type: annotatedset_type,
    },
    responseType: "blob",
  });
}
