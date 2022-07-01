const getters = {
  sidebar: (state) => state.app.sidebar, //侧边栏
  token: (state) => state.user.token,
  avatar: (state) => state.user.avatar,
  name: (state) => state.user.name,
  email: (state) => state.user.email,
  roles: (state) => state.user.roles,
  myDatasetList: (state) => state.myDataset.myDatasetList,
  communityDatasetList: (state) => state.community.communityDatasetList,
  labels: (state) => state.annotation.labels, //标签信息
};
export default getters;
