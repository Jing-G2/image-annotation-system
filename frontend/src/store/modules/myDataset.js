import {} from "@/api/myDataset";

const state = {
  myDatasetList: [],
};

const mutations = {
  /**
   * 领取标注任务，添加到个人数据集
   */
  SET_MY_DATASET_LIST: (state, myDatasets) => {
    state.myDatasetList = myDatasets;
  },
};

const actions = {
  // 领取标注任务，添加到个人数据集
  setMyDatasetList({ commit }, myDatasets) {
    commit("SET_MY_DATASET_LIST", myDatasets);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
