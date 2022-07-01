const state = {
  labels: [], // 标签信息
  annotatedSetID: 0, //标注数据集id
  annotatedSet_name: "", //标注数据集名
  colorArray: [
    // 预设标签颜色
    "#fa0404",
    "#fd0dad",
    "#8406f3",
    "#d462ee",
    "#ff9b06",
    "#e3fc07",
    "#058f32",
    "#10f0fc",
    "#83fa07",
    "#e6ee66",
    "#c0e97d",
    "#aae77d",
    "#2e0bf3",
    "#0af0e1",
    "#0baff5",
    "#1f74c9",
    "#8985ec",
    "#761616",
  ],
};

const mutations = {
  /**
   *  设置标注标签
   * @param {*} state
   */
  SET_LABELS: (state, data) => {
    state.labels = data;
  },

  /**
   *  设置要标注的数据集的id
   */
  SET_ANNOTATEDSET_INFO: (state, id, name) => {
    state.annotatedSetID = id;
    state.annotatedSet_name = name;
  },
};
const actions = {
  // 设置标注标签
  setLabels({ commit }, data) {
    commit("SET_LABELS", data);
  },

  // 设置要标注的数据集的id
  setAnnotatedSetInfo({ commit }, id, name) {
    commit("SET_ANNOTATEDSET_INFO", id, name);
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
