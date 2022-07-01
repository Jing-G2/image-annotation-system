import request from "@/utils/request";

/**
 *  获取个人数据集信息
 */
export function getMyDatasetInfoApi() {
  return request({
    url: "api/myDataset/getInfo/",
    method: "get",
  });
}

/**
 * 根据id增加一个数据集
 * @param {number} datasetInfo 数据集的信息
 */
export function addAnnotatedSetApi(datasetInfo) {
  return request({
    url: "api/myDataset/add/",
    method: "post",
    data: { datasetInfo: datasetInfo },
  });
}

/**
 * 根据id删除一条数据集数据
 * @param {number} id 数据集的id
 */
export function deleteAnnotatedSetApi(id) {
  return request({
    url: "api/myDataset/deleteOne/",
    method: "delete",
    data: { id: id },
  });
}

/**
 * 删除该所有的个人数据集
 */
export function removeAllAnnotatedSetApi() {
  return request({
    url: "api/myDataset/deleteAll/",
    method: "delete",
  });
}

/**
 * 更新数据集信息
 * @param {object} datasetInfo 数据集信息
 */
export function updateAnnotatedSetInfoApi(datasetInfo) {
  return request({
    url: "api/myDataset/update/",
    method: "post",
    data: { datasetInfo: datasetInfo },
  });
}

/**
 * 更新数据集状态
 * @param {object} datasetInfo 数据集信息
 */
export function updateAnnotatedSetStatusApi(id, status) {
  return request({
    url: "api/myDataset/updateStatus/",
    method: "post",
    data: { id: id, status: status },
  });
}
