import { getCommunityInfoApi } from "@/api/community";

const state = {
  communityDatasetList: [], // 社区中所有的数据集信息
};
const mutations = {
  /**
   * 数据集社区信息
   */
  SET_COMMUNITY_DATASET_LIST: (state, communityDatasetList) => {
    state.communityDatasetList = communityDatasetList;
  },

  /**
   * 上传压缩包数据集
   */
  ADD_NEW_COMMUNITY_DATASET: (state, newDatasetInfo) => {
    state.communityDatasetList.push(newDatasetInfo);
  },
};

const actions = {
  // 获取数据集社区列表信息
  getCommunityInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getCommunityInfoApi()
        .then((response) => {
          const { data } = response;

          if (!data) {
            reject("验证失败，请再次登录。");
          }

          const { community_dataset_list } = data.dataset_list;
          commit("SET_COMMUNITY_DATASET_LIST", community_dataset_list);
          resolve(data);
        })
        .catch((error) => {
          reject(error);
        });
    });
  },

  // 设置社区数据集列表
  setDatasetList({ commit }, communityDatasetList) {
    commit("SET_COMMUNITY_DATASET_LIST", communityDatasetList);
  },

  // 用户上传压缩包，加入新的数据集
  addNewDataset({ commit }, newDatasetInfo) {
    commit("ADD_NEW_COMMUNITY_DATASET", newDatasetInfo);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
