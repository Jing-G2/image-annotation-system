import request from "@/utils/request";

/**
 *  获取数据集社区信息
 */
export function getCommunityInfoApi() {
  return request({
    url: "api/community/getInfo/",
    method: "get",
  });
}

/**
 * 根据id删除一条数据集数据
 * @param {number} id 数据集的id
 */
export function deleteCommunityDatasetApi(id) {
  return request({
    url: "api/community/deleteOne/",
    method: "delete",
    data: { id: id },
  });
}

/**
 * 删除该社区所有的数据集
 */
export function removeAllCommunityDatasetApi() {
  return request({
    url: "api/community/deleteAll/",
    method: "delete",
  });
}

/**
 * 更新数据集信息
 * @param {object} datasetInfo 数据集信息
 */
export function updateCommunityDatasetInfoApi(datasetInfo) {
  return request({
    url: "api/community/update/",
    method: "post",
    data: { datasetInfo: datasetInfo },
  });
}
